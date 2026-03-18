import subprocess
import sys
import os
import time
from keep_alive import keep_alive

keep_alive()

print("Starting the bot...")

while True:
    try:
        result = subprocess.run([sys.executable, "file1.py"])
        exit_code = result.returncode
        print(f"[WATCHDOG] Bot exited with code {exit_code}. Restarting in 5s...")
    except Exception as e:
        print(f"[WATCHDOG] Error running bot: {e}. Restarting in 5s...")
    time.sleep(5)
