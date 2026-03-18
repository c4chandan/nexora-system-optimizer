import os
import shutil
import subprocess
import psutil
import time
from datetime import datetime

BASE_DIR = os.getcwd()
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "cleanup_log.txt")

TEMP_PATHS = [
    os.environ.get('TEMP'),
    r"C:\Windows\Temp"
]

def log(message):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def safe_delete(folder):
    if not folder or not os.path.exists(folder):
        log(f"Skipped: {folder}")
        return

    log(f"Scanning: {folder}")
    count = 0

    for item in os.listdir(folder):
        path = os.path.join(folder, item)

        try:
            if os.path.isfile(path):
                os.remove(path)
                count += 1
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
                count += 1

            if count % 50 == 0 and count != 0:
                log(f"...deleted {count} items")

        except:
            log(f"Error deleting: {path}")

    log(f"Finished: {folder} | Deleted: {count}")

def run_cmd(cmd, name):
    log(f"Running: {name}")
    subprocess.run(cmd, shell=True)
    log(f"Completed: {name}")

def basic_cleanup():
    log("=== BASIC CLEANUP START ===")

    for path in TEMP_PATHS:
        safe_delete(path)

    run_cmd("ipconfig /flushdns", "Flush DNS")

    log("=== BASIC CLEANUP COMPLETE ===")

def full_cleanup():
    log("=== FULL CLEANUP START ===")

    basic_cleanup()

    run_cmd("DISM /Online /Cleanup-Image /RestoreHealth", "DISM")
    run_cmd("sfc /scannow", "SFC")

    log("=== FULL CLEANUP COMPLETE ===")

def monitor_ram():
    log("=== RAM MONITOR STARTED ===")

    while True:
        ram = psutil.virtual_memory().percent
        log(f"RAM Usage: {ram}%")

        if ram > 80:
            log("High RAM → Running cleanup")
            basic_cleanup()

        time.sleep(60)

def game_mode():
    log("=== GAME MODE START ===")

    apps = ["OneDrive.exe", "Teams.exe", "Skype.exe"]

    for app in apps:
        subprocess.run(f"taskkill /f /im {app}", shell=True)
        log(f"Closed: {app}")

    subprocess.run("powercfg /setactive SCHEME_MIN", shell=True)

    log("Game Mode Enabled")

def analyze_logs():
    log("=== ANALYZING LOGS ===")

    if not os.path.exists(LOG_FILE):
        log("No logs found")
        return

    errors = 0

    with open(LOG_FILE, "r") as f:
        for line in f:
            if "Error" in line:
                errors += 1

    log(f"Errors Found: {errors}")

def auto_game_mode():
    log("=== AUTO GAME MODE START ===")

    keywords = ["steam", "epic", "game"]

    while True:
        for p in psutil.process_iter(['name']):
            name = (p.info['name'] or "").lower()

            if any(k in name for k in keywords):
                log(f"Game detected: {name}")
                game_mode()
                time.sleep(300)

        time.sleep(10)