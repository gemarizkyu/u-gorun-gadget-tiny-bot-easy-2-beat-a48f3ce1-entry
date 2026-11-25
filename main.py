# Dip-Bounce Bot: a tiny mean-reversion bot for agent-fun/bars-replay/v1.
#
# Idea (from the dev window in this kit): hourly Solana prices mean-revert
# over a few hours. Momentum (buying strength) loses on the dev window, while
# buying a sharp 6-hour dip and holding it for a few bars wins: a dip of
# 3% or more, bought at the next bar's open and sold 4 bars later, averaged
# about +1% per round trip before costs on the dev data, with a 58-73% win
# rate. The bot therefore:
#   - stays in cash unless a symbol has dipped hard in the last 6 bars,
#   - buys the deepest dips (up to 4 symbols, 25% of equity each),
#   - exits after 4 bars, or sooner on a 3% stop-loss,
#   - never chases strength, never shorts, never uses leverage.
# Every decision comes only from the bars the harness sends in the hello /
# batch messages: no wall clock, no randomness, no network, no outside data,
# so the two replay runs match byte for byte.
#
# Guardrails: the competition needs at least 8 trades and at most 25%
# drawdown. The bot observes the first 24 bars before trading at all: the
# dev window shows dips in the opening hours of an unestablished trend keep
# falling, while the same dip a day in bounces. If the window then stays
# quiet (no deep dip for a long time) the bot loosens the dip threshold
# after bar 48 so it still clears the trade count instead of sitting idle.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

# --- strategy parameters (validated on the kit's dev window) ---
LOOKBACK_BARS = 6        # dip measured over the last 6 hourly bars
HISTORY_BARS = 24        # observe a full day of bars before trading: dips in
                         # the first hours of an unestablished trend keep
                         # falling, so no entry is taken before bar 24
DIP_BPS = 300            # buy when the 6-bar return is -3% or worse
DIP_BPS_RELAXED = 150    # quiet-window fallback after RELAX_AFTER_BARS
RELAX_AFTER_BARS = 48    # loosen the threshold once past this bar ...
RELAX_MIN_TRADES = 6     # ... if fewer than this many fills have happened
HOLD_BARS = 4            # exit a position 4 bars after the buy filled
STOP_BPS = 300           # exit early if the position is down 3% from entry
TOP_N = 4                # most symbols held at once
MAX_ALLOC_BPS = 9000     # use at most 90% of equity for new buys
MAX_SLIPPAGE_BPS = 1000  # 10%: wide enough for normal hourly gaps
BPS = 10_000

# Each symbol's closes by batch seq, as ints; entry info for held positions,
# recorded from the fills the harness reports: symbol -> (fill bar, fill price).
# Counting the hold from the fill bar (not the decision bar) matches the
# backtest that validated the parameters.
closes = {}
entries = {}  # symbol -> (fill seq, fill price)
filled_trades = 0


def trailing_return(symbol, seq, bars_back):
    """Close now vs close `bars_back` batches ago, in bps (int), or None."""
    hist = closes.get(symbol)
    if hist is None or seq - bars_back < 0:
        return None
    now = hist[seq]
    then = hist[seq - bars_back]
    if now is None or then is None or then == 0:
        return None
    return (now - then) * BPS // then


def on_batch(state, batch):
    global filled_trades
    # Fold this batch's fills in first: a buy that filled records its entry
    # (fill bar and fill price, which the stop-loss and the hold count use),
    # a sell that filled clears it, and every fill counts toward the
    # quiet-window fallback below.
    for fill in batch.get("fills", []):
        if fill.get("status") != "filled":
            continue
        filled_trades += 1
        symbol = fill.get("symbol")
        if fill.get("side") == "buy":
            # NOTE: the fill's decided_bar / fill_bar are millisecond
            # timestamps, NOT bar indexes: the hold is counted from this
            # batch's seq, which is the fill bar's index (the fill is
            # reported in the batch whose bars it filled at).
            entries[symbol] = (state.seq, int(fill.get("price", "0")))
        elif fill.get("side") == "sell":
            entries.pop(symbol, None)
    # While warming up every order would be rejected: just watch the bars.
    if state.warming_up:
        return []
    seq = state.seq
    for symbol in state.hello["symbols"]:
        sym = symbol["symbol"]
        closes.setdefault(sym, {})[seq] = state.close(sym)
    orders = []
    # --- exits: time-based, then stop-loss ---
    for symbol, holding in list(state.positions.items()):
        entry_seq, entry_price = entries.get(symbol, (seq, state.close(symbol)))
        close = state.close(symbol)
        if close is None or entry_price is None or entry_price == 0:
            continue
        gain_bps = (close - entry_price) * BPS // entry_price
        if seq - entry_seq >= HOLD_BARS or gain_bps <= -STOP_BPS:
            # The entry is cleared only when the harness reports the sell
            # as filled; a rejected sell keeps its entry and its hold count.
            orders.append(
                {"side": "sell", "symbol": symbol, "qty": holding.qty,
                 "max_slippage_bps": MAX_SLIPPAGE_BPS}
            )
    # --- entries: deepest 6-bar dips first ---
    # No entries before HISTORY_BARS: the bot needs a full day of bars to
    # tell a dip that bounces from the start of a waterfall.
    dip_bps = DIP_BPS
    if seq >= RELAX_AFTER_BARS and filled_trades < RELAX_MIN_TRADES:
        dip_bps = DIP_BPS_RELAXED
    candidates = []
    if seq < HISTORY_BARS:
        return orders
    for symbol in state.hello["symbols"]:
        sym = symbol["symbol"]
        if sym in state.positions:
            continue
        ret = trailing_return(sym, seq, LOOKBACK_BARS)
        if ret is not None and ret <= -dip_bps:
            candidates.append((ret, sym))
    # Deepest dip first; ties keep the universe order (sort is stable).
    candidates.sort(key=lambda item: item[0])
    slots = min(TOP_N, len(candidates))
    if slots:
        budget = min(state.cash, state.equity * MAX_ALLOC_BPS // BPS)
        per_symbol = min(budget // slots, state.equity * state.hello["caps"]["max_weight_bps"] // BPS)
        min_notional = int(state.hello["fees"]["min_notional_quote_units"])
        if per_symbol >= min_notional:
            for _, sym in candidates[:slots]:
                # The entry (fill bar and fill price) is recorded when the
                # harness reports the buy as filled, in the next batch.
                orders.append(
                    {"side": "buy", "symbol": sym, "notional_quote_units": per_symbol,
                     "max_slippage_bps": MAX_SLIPPAGE_BPS}
                )
    return orders


makefun_bars.run(on_batch)
