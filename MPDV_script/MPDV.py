import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# --- Redirect all output to log file ---
log_file = "/root/MPDV_script/MPDV.log"
sys.stdout = open(log_file, "a")
sys.stderr = sys.stdout
print(f"\n--- Script started at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")

# --- Load .env file ---
load_dotenv("/root/MPDV_script/.env")

URL = os.getenv("URL")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 300))  # default 5 min

# --- Chrome options (Raspberry Pi / lightweight Linux friendly) ---
chrome_options = Options()
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#chrome_options.add_argument("--headless")  # optional if running server-only

# --- Persistent cache & session ---
chrome_options.add_argument("--user-data-dir=/root/chrome-profile")

chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Never save passwords
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.exit_type": "Normal",
    "profile.exited_cleanly": True,
    "session.restore_on_startup": 0
}
chrome_options.add_experimental_option("prefs", prefs)

# --- Chromedriver service ---
service = Service("/usr/bin/chromedriver")

# --- Start WebDriver ---
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

# --- Enable Chrome cache explicitly (Selenium 4 / CDP) ---
driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": False})

# --- Function to Login ---
def try_login():
    wait_local = WebDriverWait(driver, 5)

    # Click login button (if present)
    try:
        login_button = wait_local.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//dx-button[@aria-label='Login' or @aria-label='Zur Anmeldung']")
            )
        )
        login_button.click()
        print("Clicked login button")
    except:
        print("Login button not found (already logged in)")

    # Username
    try:
        if USERNAME:
            username_box = wait_local.until(
                EC.element_to_be_clickable((By.NAME, "username"))
            )
            username_box.clear()
            username_box.send_keys(USERNAME)
            print("Entered username")
    except:
        print("Username field not found")

    # Password
    try:
        if PASSWORD:
            password_box = wait_local.until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_box.clear()
            password_box.send_keys(PASSWORD)
            password_box.submit()
            print("Entered password and submitted")
    except:
        print("Password field not found or already logged in")

# --- Open website ---
driver.get(URL)
print("Page title:", driver.title)

# --- Initial login ---
try_login()

# --- Auto-refresh loop ---
try:
    while True:
        time.sleep(REFRESH_INTERVAL)
        driver.refresh()
        print(f"Page refreshed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        try_login()

except KeyboardInterrupt:
    print("Stopped by user.")
except Exception as e:
    print("Unhandled exception:", e)
finally:
    driver.quit()
    print(f"--- Script ended at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")