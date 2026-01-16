import os
import time
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/root/MPDV_script/.env")

LOG_FILE = "/root/MPDV_script/hdmi_scheduler.log"
LOG_ENABLED = os.getenv("LOG_ENABLED", "false").lower() == "true"

days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def time_to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

def log(message):
    if not LOG_ENABLED:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def set_hdmi(state):
    subprocess.run(
        ["vcgencmd", "display_power", "1" if state else "0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

last_state = None

while True:
    now = datetime.now()
    day_name = days[now.weekday()]

    on_time = os.getenv(f"{day_name}_ON", "00:00")
    off_time = os.getenv(f"{day_name}_OFF", "00:00")

    on_minutes = time_to_minutes(on_time)
    off_minutes = time_to_minutes(off_time)
    current_minutes = now.hour * 60 + now.minute

    # Schedule logic (supports overnight)
    if on_minutes == off_minutes:
        should_be_on = False
    elif on_minutes < off_minutes:
        should_be_on = on_minutes <= current_minutes < off_minutes
    else:
        should_be_on = current_minutes >= on_minutes or current_minutes < off_minutes

    if should_be_on != last_state:
        set_hdmi(should_be_on)
        log(f"HDMI {'ON' if should_be_on else 'OFF'} ({day_name})")
        last_state = should_be_on

    time.sleep(60)
