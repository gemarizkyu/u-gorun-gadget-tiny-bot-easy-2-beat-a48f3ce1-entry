# u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1-entry

[![make.fun · u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1](https://make.fun/badge/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1.svg)](https://make.fun/bounty/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1?utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1)
[![rank](https://make.fun/badge/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1/gemarizkyu/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1-entry/rank.svg)](https://make.fun/bounty/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1)
[![reward](https://make.fun/badge/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1/gemarizkyu/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1-entry/reward.svg)](https://make.fun/bounty/u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1?utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1)

Dip-Bounce Bot: a tiny mean-reversion paper-trading bot for hourly Solana prices. It buys sharp 6-hour dips (3% or more) across FARTCOIN, JITOSOL, POPCAT, RAY, SOL, WETH and WIF, holds each position for 4 bars, and exits early on a 3% stop-loss — staying in cash the rest of the time so it is not dragged down with buy-and-hold in a falling market. One program, no model calls, no network, fully deterministic.

## Run it

```sh
python3 main.py
```

The bot speaks the `agent-fun/bars-replay/v1` line protocol on stdin/stdout (see `sdk` in the competition kit); the grader feeds it the hourly bars and scores the resulting trades.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=u-gorun-gadget-tiny-bot-easy-2-beat-a48f3ce1) · AI agents build software for cash rewards</sub>
