<div align="center">

# 🤖 ST-CHECKER-BOT

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram)](https://core.telegram.org/bots)
[![Platform](https://img.shields.io/badge/Platform-Replit%20%7C%20AWS%20EC2-orange?style=for-the-badge)](https://replit.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A powerful Telegram bot for checking credit card validity across multiple payment gateways — with VIP plans, proxy support, BIN lookup, and one-click cloud deployment.**

</div>

---

## ✨ Features

- 💳 **Multi-Gateway Checking** — PayPal, Braintree 3DS (VBV), Stripe Charge, Stripe Checkout, SK checker
- 📦 **Mass Card Checking** — Bulk check hundreds of cards from a file
- 🔍 **BIN Lookup** — Instant card brand, type, bank, and country info
- 🎰 **Card Generator** — Generate valid card numbers from any BIN
- 🌐 **Proxy Support** — Per-user HTTP/SOCKS5 proxy configuration
- 👥 **User Plans** — FREE and VIP tier management with redeem codes
- 📊 **Live Statistics** — Real-time usage stats, daily breakdowns, gateway performance
- ⚡ **Uptime System** — Auto-restart watchdog + Flask keep-alive server
- 🔐 **Admin Panel** — Full admin controls, DB export, backup, and user management
- 🚀 **Easy Deployment** — One-click AWS EC2 setup with systemd auto-start

---

## 📸 Preview

```
Bot Start On ✅
Admin ID: xxxxxxxxxx

/ping  → 🏓 Pong! Latency: 42ms
/status → 🤖 Bot Online | Uptime: 2h 15m | Mode: Polling
/stats  → 📊 Total Users: 120 | Checks Today: 540 | Live: 38
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/hiaistudent-jpg/ST-CHECKER-BOT.git
cd ST-CHECKER-BOT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
export BOT_TOKEN="your_bot_token_here"
export ADMIN_ID="your_telegram_user_id"
```

> 💡 Get your **BOT_TOKEN** from [@BotFather](https://t.me/BotFather)
> Get your **ADMIN_ID** from [@userinfobot](https://t.me/userinfobot)

### 4. Run the Bot

```bash
python3 main.py
```

---

## 🤖 Commands

### 🔵 General
| Command | Description |
|---------|-------------|
| `/start` | Welcome message and plan info |
| `/cmds` | Full list of all commands |
| `/myid` | Show your Telegram user ID |
| `/ping` | Check bot response latency |
| `/status` | Bot uptime, environment and mode |
| `/stats` | Global usage statistics |

### 💳 Card Checking
| Command | Description | Usage |
|---------|-------------|-------|
| `/chk` | Single card check | `/chk 4111111111111111\|12\|25\|123` |
| `/chkm` | Mass card check | `/chkm` (attach cards) |
| `/pp` | PayPal gateway | `/pp 4111...\|12\|25\|123` |
| `/vbv` | Braintree 3DS check | `/vbv 4111...\|12\|25\|123` |
| `/vbvm` | Braintree 3DS mass check | `/vbvm` |
| `/st` | Stripe charge $1 | `/st 4111...\|12\|25\|123` |
| `/sk` | SK key card checker | `/sk sk_live_xxx` |
| `/skm` | SK key mass checker | `/skm sk_live_xxx` |
| `/skchk` | SK key live/dead check | `/skchk sk_live_xxx` |
| `/co` | Stripe checkout | `/co <url>` |

### 🛠️ Utilities
| Command | Description | Usage |
|---------|-------------|-------|
| `/gen` | Generate cards from BIN | `/gen 411111` or `/gen 411111 20` |
| `/bin` | BIN lookup | `/bin 411111` |
| `/setproxy` | Set your proxy | `/setproxy http://ip:port` |
| `/removeproxy` | Remove proxy | `/removeproxy` |
| `/proxycheck` | Test your proxy | `/proxycheck` |
| `/setamount` | Set charge amount | `/setamount 2` |
| `/setsk` | Set Stripe SK key | `/setsk sk_live_xxx` |
| `/history` | Your last 10 checks | `/history` |

### 👑 Admin Only
| Command | Description |
|---------|-------------|
| `/amadmin` | Verify admin privileges |
| `/code` | Generate VIP redeem codes |
| `/dbstats` | Full database statistics |
| `/dbexport` | Export database to CSV/JSON |
| `/dbbackup` | Send DB backup file |

---

## ☁️ Deployment

### 🟢 Replit (Recommended for beginners)

1. Fork this repo or import to [Replit](https://replit.com)
2. Go to **Secrets** and add:
   - `BOT_TOKEN` → your bot token
   - `ADMIN_ID` → your Telegram ID
3. Click **Run** — the bot starts automatically
4. The keep-alive server (port 8099) pings itself every 4.5 minutes to stay online

### 🟠 AWS EC2 (One-Click Setup)

Run this single command on any **Ubuntu/Debian** EC2 instance:

```bash
bash setup.sh
```

This script automatically:
- ✅ Updates system packages
- ✅ Installs Python 3, pip, git, screen
- ✅ Creates a Python virtual environment
- ✅ Installs all bot dependencies
- ✅ Registers a **systemd service** (auto-starts on reboot)
- ✅ Starts the bot immediately

**Useful EC2 commands after setup:**
```bash
# Check bot status
sudo systemctl status st-checker-bot

# View live logs
journalctl -u st-checker-bot -f

# Restart bot
sudo systemctl restart st-checker-bot
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ Yes | Telegram bot token from @BotFather |
| `ADMIN_ID` | ✅ Yes | Your Telegram numeric user ID |
| `BASE_URL` | ❌ Optional | Custom domain for keep-alive ping |
| `BASE_URL_PORT` | ❌ Optional | Port for keep-alive (default: 80) |

> **Security Tip:** Never hardcode tokens in your code. Always use environment variables or secret managers.

---

## 📁 Project Structure

```
ST-CHECKER-BOT/
├── main.py              # Watchdog — auto-restarts bot on crash
├── file1.py             # All bot command handlers
├── gatet.py             # Payment gateway functions
├── database.py          # SQLite database layer
├── keep_alive.py        # Flask uptime server (port 8099)
├── requirements.txt     # Python dependencies
├── setup.sh             # One-click AWS EC2 installer
├── data.json            # User plan data (FREE / VIP)
├── user_proxies.json    # Per-user proxy settings
├── user_amounts.json    # Per-user charge amounts
├── combo.txt            # Cards list for bulk check commands
└── telegram_bot.db      # SQLite database (auto-created)
```

---

## 📦 Requirements

```
pyTelegramBotAPI
flask
requests
urllib3
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. The author is not responsible for any misuse of this tool. Always comply with the terms of service of any payment gateway you interact with.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ by [hiaistudent-jpg](https://github.com/hiaistudent-jpg)

⭐ **Star this repo if you found it useful!**

</div>
