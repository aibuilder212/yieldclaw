# 🦞 YieldClaw

> **Self-hosted. Grok-smart. Built in public. 100% yours.**

YieldClaw is a community-built extension for the [OpenClaw](https://github.com/OpenClaw) autonomous agent framework. It connects OpenClaw's local execution engine + n8n automation + Grok 4.1 Fast intelligence to scan Raydium and Kamino LP pools on Solana, detect real yield edges, flag impermanent loss risk, and alert you instantly via Telegram — all running on your own infrastructure.

**No custody. No subscriptions. No black boxes. Fork it and own it.**

> ⚠️ **INDEPENDENT COMMUNITY PROJECT** — Not affiliated with, endorsed by, or connected to OpenClaw core developers, xAI, Raydium, or any other named project.

---

## ⚠️ Disclaimer

YieldClaw is an **informational monitoring and alerting tool only**. It does NOT execute trades, hold funds, or provide financial advice. All alerts are for educational purposes only. DeFi carries significant risk. You are solely responsible for your own financial decisions. See [docs/DISCLAIMER.md](docs/DISCLAIMER.md).

---

## What It Does (Phase 1 – Alerts Only)

- Scans Raydium CLMM + CPMM pools every 4 minutes via Raydium REST API v3
- Calculates live APY, fee yield, TVL change, and estimated IL for tracked positions
- Grok 4.1 Fast reasons over scan results and sends human-readable alerts
- Fires alerts to your Telegram bot
- Logs every scan to a public Railway-hosted agent log page

## What It Does NOT Do

- Execute swaps (Phase 2, user-approved only, never automatic)
- Hold or touch your funds (you always sign txs)
- Require a paid subscription (free and open-source forever)

---

## Stack

| Layer | Tool | Why |
|---|---|---|
| Agent execution | OpenClaw (local) | Self-hosted, unstoppable, forkable |
| Workflow orchestration | n8n | Reliable, visual, battle-tested |
| Intelligence | Grok 4.1 Fast | Built for agentic tool-calling + finance |
| Data source | Raydium API v3 | Real pool data, no middlemen |
| Alerts | Telegram Bot API | Instant, free, runs on mobile |
| Hosting | Railway (or self-host) | Simple, cheap, always-on |

---

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- n8n (self-hosted or n8n.cloud)
- OpenClaw installed locally
- Telegram bot token (get from @BotFather)
- xAI API key (console.x.ai)

### Install

```bash
git clone https://github.com/aibuilder212/yieldclaw.git
cd yieldclaw
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
# Fill in: XAI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
```

### Import n8n Workflow

1. Open your n8n instance
2. Import `workflows/raydium-lp-scanner.json`
3. Set credentials in n8n credential manager
4. Activate the workflow

---

## Project Structure

```
yieldclaw/
├── README.md
├── LICENSE
├── .env.example
├── /workflows/
│   └── raydium-lp-scanner.json
├── /agents/
│   ├── yieldclaw-agent.json
│   └── grok-system-prompt.md
├── /scripts/
│   ├── raydium_fetch.py
│   ├── il_calculator.py
│   └── alert_formatter.py
├── /docs/
│   ├── SETUP.md
│   ├── ARCHITECTURE.md
│   ├── DISCLAIMER.md
│   └── ROADMAP.md
└── /dashboard/
    └── agent-log.html
```

---

## Roadmap

| Phase | Status | Features |
|---|---|---|
| Phase 1 | 🔨 Building now | Raydium scan → Grok reasoning → Telegram alerts |
| Phase 2 | Planned | Kamino + multi-pool, IL dashboard, WhatsApp |
| Phase 3 | Future | User-approved swap hooks (you sign every tx) |

---

## Built in Public

30-day live build on X: [@aibuilder212](https://x.com/aibuilder212)

**#YieldClaw #BuildInPublic #Solana #AgentFi**

---

## License

MIT — fork it, build on it, ship it. Give credit, don’t rug people.
