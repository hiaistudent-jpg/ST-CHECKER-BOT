"""
ST-CHECKER-BOT — GitHub Webhook Listener
Listens on port 9000 for GitHub push events and runs update.sh
"""

import hashlib
import hmac
import json
import logging
import os
import subprocess
from flask import Flask, request, jsonify

# ── Config ────────────────────────────────────────────────────────────────────
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "").encode()
PORT           = int(os.environ.get("WEBHOOK_PORT", 9000))
BOT_DIR        = os.path.expanduser("~/st-checker-bot")
UPDATE_SCRIPT  = os.path.join(BOT_DIR, "update.sh")
LOG_FILE       = os.path.join(BOT_DIR, "webhook.log")
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def verify_signature(payload: bytes, sig_header: str) -> bool:
    """Verify GitHub HMAC-SHA256 signature."""
    if not WEBHOOK_SECRET:
        logger.warning("WEBHOOK_SECRET not set — skipping signature check.")
        return True
    if not sig_header or not sig_header.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(WEBHOOK_SECRET, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig_header)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Webhook listener is running"}), 200


@app.route("/webhook", methods=["POST"])
def webhook():
    # ── Signature check ───────────────────────────────────────
    sig = request.headers.get("X-Hub-Signature-256", "")
    if not verify_signature(request.data, sig):
        logger.warning("Unauthorized webhook request — invalid signature.")
        return jsonify({"error": "Unauthorized"}), 401

    # ── Parse event ───────────────────────────────────────────
    event = request.headers.get("X-GitHub-Event", "unknown")
    try:
        payload = request.get_json(force=True) or {}
    except Exception:
        payload = {}

    branch = payload.get("ref", "")
    logger.info(f"Event: {event} | Branch: {branch}")

    if event != "push" or branch != "refs/heads/main":
        logger.info("Ignored — not a push to main.")
        return jsonify({"status": "ignored"}), 200

    pusher = payload.get("pusher", {}).get("name", "unknown")
    commits = len(payload.get("commits", []))
    logger.info(f"Push by '{pusher}' — {commits} commit(s). Running update.sh...")

    # ── Run update script ─────────────────────────────────────
    try:
        result = subprocess.Popen(
            ["bash", UPDATE_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=BOT_DIR
        )
        logger.info(f"update.sh started (PID {result.pid})")
        return jsonify({"status": "update triggered", "pid": result.pid}), 200
    except Exception as e:
        logger.error(f"Failed to run update.sh: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    logger.info(f"Webhook listener starting on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=False)
