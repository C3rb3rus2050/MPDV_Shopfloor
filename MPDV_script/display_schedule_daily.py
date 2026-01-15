import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/root/MPDV_script/.env")

# Map weekdays to environment variables
days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def time_to_minutes(t):
    h, m = map(int, t.split(":"))
    return h*60 + m

while True:
    now = datetime.now()
    weekday_index = now.weekday()  # 0=Monday, 6=Sunday
    day_name = days[weekday_index]

    # Read today's on/off times
    off_time = os.getenv(f"{day_name}_OFF", "23:00")
    on_time = os.getenv(f"{day_name}_ON", "07:00")

    off_minutes = time_to_minutes(off_time)
    on_minutes = time_to_minutes(on_time)
    current_minutes = now.hour*60 + now.minute

    # Handle display power
    if off_minutes <= current_minutes < on_minutes:
        os.system("vcgencmd display_power 0")
        print(f"Display OFF ({day_name}) at {now.strftime('%H:%M:%S')}")
    else:
        os.system("vcgencmd display_power 1")
        print(f"Display ON ({day_name}) at {now.strftime('%H:%M:%S')}")

    time.sleep(60)  # Check every minute
