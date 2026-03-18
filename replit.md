# ST-CHECKER-BOT

A Telegram bot for checking credit card validity through multiple payment gateways, with user management, VIP plans, proxy support, and admin controls.

## Tech Stack

- **Language**: Python 3.11
- **Bot library**: pyTelegramBotAPI (telebot)
- **Database**: SQLite (`telegram_bot.db`)
- **Keep-alive**: Flask HTTP server (port 8099)

## Project Structure

```
workspace/
├── main.py            # Watchdog — auto-restarts file1.py on crash
├── file1.py           # All bot command handlers and gateway logic
├── gatet.py           # Payment gateway functions (PayPal, Braintree, etc.)
├── database.py        # SQLite database (users, queries, card checks)
├── keep_alive.py      # Flask server for uptime + self-ping
├── requirements.txt   # Python dependencies
├── setup.sh           # One-click AWS EC2 deployment script
├── data.json          # User plan data (FREE / VIP)
├── user_proxies.json  # Per-user proxy settings
├── user_amounts.json  # Per-user charge amount settings
├── combo.txt          # Card list for bulk check commands
└── telegram_bot.db    # SQLite database file (auto-created)
```

## Required Secrets

| Key         | Description                                    |
|-------------|------------------------------------------------|
| `BOT_TOKEN` | Telegram bot token — get from @BotFather       |
| `ADMIN_ID`  | Your Telegram user ID — get from @userinfobot  |

## Workflow

- **Telegram Bot** — `python3 main.py` (console, port 8099)

## Bot Commands

### General
| Command   | Description                             |
|-----------|-----------------------------------------|
| `/start`  | Welcome message and plan info           |
| `/cmds`   | Full command list                       |
| `/myid`   | Show your Telegram user ID              |
| `/ping`   | Check bot latency                       |
| `/status` | Bot uptime, environment, running state  |
| `/stats`  | Usage statistics (users, checks, today) |

### Card Checking
| Command  | Description              |
|----------|--------------------------|
| `/chk`   | Single card check        |
| `/chkm`  | Multi-card check         |
| `/pp`    | PayPal gateway check     |
| `/vbv`   | VBV / 3DS check          |
| `/sk`    | Stripe check             |
| `/co`    | Charge/checkout check    |
| `/st`    | Standard gateway check   |

### Utilities
| Command      | Description                       |
|--------------|-----------------------------------|
| `/gen`       | Generate card numbers from BIN    |
| `/bin`       | BIN lookup                        |
| `/setproxy`  | Set your proxy                    |
| `/setamount` | Set charge amount                 |
| `/history`   | View your last 10 card checks     |

### Admin Only
| Command     | Description                    |
|-------------|--------------------------------|
| `/amadmin`  | Verify admin privileges        |
| `/code`     | Generate VIP redeem codes      |
| `/dbstats`  | Full database statistics       |
| `/dbexport` | Export database to CSV/JSON    |
| `/dbbackup` | Send database backup file      |

## EC2 Deployment

Run `bash setup.sh` on any Ubuntu/Debian EC2 instance for a one-click automated deployment with systemd service registration.

## Keep-Alive

The Flask server on port 8099 pings itself every 4.5 minutes. The self-ping URL is auto-detected from `REPLIT_DEV_DOMAIN`.
