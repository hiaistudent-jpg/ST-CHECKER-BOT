from flask import Flask, jsonify
from threading import Thread
import requests
import urllib3
import time
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── Configuration — set via Replit Secrets/Env Vars ─────────────────────────
# BASE_URL      → your Replit HTTPS link  (e.g. https://xxx.riker.replit.dev)
# BASE_URL_PORT → external port           (80 for HTTP, 443 for HTTPS)
BASE_URL      = os.environ.get('BASE_URL', '').strip().rstrip('/')
BASE_URL_PORT = int(os.environ.get('BASE_URL_PORT', '80'))
_INTERNAL_PORT = 8080
# ──────────────────────────────────────────────────────────────────────────────

app = Flask('')
start_time = time.time()


@app.route('/')
def home():
    uptime_seconds = int(time.time() - start_time)
    hours   = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f'''
    <html>
    <head><title>Bot Status</title></head>
    <body style="font-family:Arial;text-align:center;margin-top:50px;background:#1a1a2e;color:#eee;">
        <h1>🤖 Bot is Running!</h1>
        <p>✅ Status: <b style="color:#00ff88">Online</b></p>
        <p>⏱️ Uptime: <b>{hours}h {minutes}m {seconds}s</b></p>
        <p>🔄 Auto-ping: Active</p>
        <p>🌐 Base URL: <b style="color:#88aaff">{BASE_URL or "auto-detect"}</b></p>
        <p>🔌 Port: <b>{BASE_URL_PORT}</b></p>
    </body>
    </html>
    '''


@app.route('/ping')
def ping():
    return jsonify({'status': 'alive', 'uptime': int(time.time() - start_time)})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


def _get_self_url():
    if BASE_URL:
        url = BASE_URL if BASE_URL.startswith('http') else f'http://{BASE_URL}'
        if BASE_URL_PORT not in (80, 443):
            url = f'{url}:{BASE_URL_PORT}'
        return url

    for var in ('REPLIT_DEV_DOMAIN', 'REPLIT_DOMAINS'):
        val = os.environ.get(var, '')
        if val:
            domain = val.split(',')[0].strip()
            return f'https://{domain}'

    slug  = os.environ.get('REPL_SLUG', '')
    owner = os.environ.get('REPL_OWNER', '')
    if slug and owner:
        return f'https://{slug}.{owner}.repl.co'

    return f'http://localhost:{_INTERNAL_PORT}'


def self_ping():
    url = _get_self_url()
    print(f"[KEEP-ALIVE] Ping target → {url}/ping  (port {BASE_URL_PORT})")
    while True:
        try:
            time.sleep(270)
            r = requests.get(f'{url}/ping', timeout=10, verify=False)
            print(f"[KEEP-ALIVE] Ping OK — {r.status_code}")
        except Exception as e:
            print(f"[KEEP-ALIVE] Ping failed: {e}")


def run():
    app.run(host='0.0.0.0', port=_INTERNAL_PORT, debug=False, use_reloader=False)


def keep_alive():
    server_thread = Thread(target=run, daemon=True)
    server_thread.start()

    ping_thread = Thread(target=self_ping, daemon=True)
    ping_thread.start()
