#!/bin/bash
# ============================================================
#   ST-CHECKER-BOT — Auto Update Script
#   Called by webhook_listener.py on every git push
# ============================================================

BOT_DIR="$HOME/st-checker-bot"
LOG_FILE="$BOT_DIR/update.log"
SERVICE_NAME="st-checker-bot"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

log "===== UPDATE TRIGGERED ====="

cd "$BOT_DIR" || { log "ERROR: Cannot cd to $BOT_DIR"; exit 1; }

# ── 1. Git pull ───────────────────────────────────────────────
log "Pulling latest code from GitHub..."
git_output=$(git pull origin main 2>&1)
git_status=$?
log "Git output: $git_output"

if [ $git_status -ne 0 ]; then
    log "ERROR: git pull failed (exit $git_status). Aborting."
    exit 1
fi

if echo "$git_output" | grep -q "Already up to date"; then
    log "Already up to date — no restart needed."
    exit 0
fi

# ── 2. Install new dependencies ───────────────────────────────
if [ -f "requirements.txt" ]; then
    log "Installing dependencies..."
    source venv/bin/activate 2>/dev/null || true
    pip install -r requirements.txt -q
    log "Dependencies installed."
fi

# ── 3. Restart bot ────────────────────────────────────────────
if command -v systemctl &>/dev/null && systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
    log "Restarting via systemd..."
    sudo systemctl restart "$SERVICE_NAME"
    sleep 3
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log "Bot restarted successfully via systemd."
    else
        log "ERROR: systemd restart failed."
        exit 1
    fi
else
    log "Restarting via screen..."
    screen -S "$SERVICE_NAME" -X quit 2>/dev/null || true
    sleep 2
    source venv/bin/activate 2>/dev/null || true
    screen -dmS "$SERVICE_NAME" bash -c \
        "cd $BOT_DIR && source venv/bin/activate && python3 main.py 2>&1 | tee bot.log"
    sleep 3
    if screen -list | grep -q "$SERVICE_NAME"; then
        log "Bot restarted successfully via screen."
    else
        log "ERROR: screen restart failed."
        exit 1
    fi
fi

log "===== UPDATE COMPLETE ====="
