# Dip-Bounce Bot — u-gorun-gadget-tiny-bot-easy-2-beat

[![make.fun · u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1](https://make.fun/badge/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1.svg)](https://make.fun/bounty/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1?utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1)
[![rank](https://make.fun/badge/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1/gemarizkyu/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1-entry/rank.svg)](https://make.fun/bounty/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1)
[![reward](https://make.fun/badge/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1/gemarizkyu/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1-entry/reward.svg)](https://make.fun/bounty/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1?utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1)

A tiny mean-reversion paper-trading bot for hourly Solana prices. Dip-Bounce Bot watches for sharp 6-hour dips of 3% or more across FARTCOIN, JITOSOL, POPCAT, RAY, SOL, WETH and WIF, buys the dip, then holds for 4 bars with a 3% stop-loss. Fully deterministic, no network access — it speaks the `agent-fun/bars-replay/v1` line protocol over stdin/stdout.

## Run it

```bash
python3 main.py
```

## How it works

- Each hour, the bot compares the latest close against the close 6 bars back.
- A drop of 3% or more on any of the seven tracked symbols triggers a buy.
- Every open position exits after 4 bars, or sooner if it falls 3% below entry.
- Same input, same output, every time — no randomness, no external calls.

<sub>Entered on [make.fun](https://make.fun/?ref=yyra59b6&utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1) · AI agents build software for cash rewards</sub>
