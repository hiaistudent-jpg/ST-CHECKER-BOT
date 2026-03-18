import subprocess
import sys
import os
import time
import requests
from keep_alive import keep_alive

keep_alive()

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_ID  = os.environ.get('ADMIN_ID', '')

def tg_notify(text):
    """Send a plain Telegram message from watchdog (no bot object needed)."""
    if not BOT_TOKEN or not ADMIN_ID:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_ID, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"[WATCHDOG] Notify failed: {e}")

print("Starting the bot...")
restart_count = 0

while True:
    try:
        result = subprocess.run([sys.executable, "file1.py"])
        exit_code = result.returncode

        if exit_code == 0:
            print("[WATCHDOG] Bot stopped cleanly (exit 0). Restarting in 5s...")
        else:
            restart_count += 1
            print(f"[WATCHDOG] Bot crashed (exit {exit_code}). Restart #{restart_count} in 5s...")
            import datetime
            _now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tg_notify(
                f"<b>╔══════════════════════╗\n"
                f"║  🔴  BOT CRASHED!     ║\n"
                f"╚══════════════════════╝\n\n"
                f"⚠️ Bot exited unexpectedly!\n\n"
                f"💥 Exit Code   : <code>{exit_code}</code>\n"
                f"🔄 Restart No  : <code>#{restart_count}</code>\n"
                f"⏰ Time        : <code>{_now}</code>\n\n"
                f"♻️ <b>Auto-restarting in 5 seconds...</b>\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"[⌤] YADISTAN - 🍀</b>"
            )

    except Exception as e:
        restart_count += 1
        print(f"[WATCHDOG] Error running bot: {e}. Restarting in 5s...")
        import datetime
        _now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tg_notify(
            f"<b>╔══════════════════════╗\n"
            f"║  ⚠️  BOT ERROR!       ║\n"
            f"╚══════════════════════╝\n\n"
            f"🛑 Watchdog caught an error:\n"
            f"<code>{str(e)[:200]}</code>\n\n"
            f"🔄 Restart No : <code>#{restart_count}</code>\n"
            f"⏰ Time       : <code>{_now}</code>\n\n"
            f"♻️ <b>Auto-restarting in 5 seconds...</b>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"[⌤] YADISTAN - 🍀</b>"
        )

    time.sleep(5)
