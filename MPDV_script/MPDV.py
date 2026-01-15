import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# --- Load .env file ---
load_dotenv("/root/MPDV_script/.env")

URL = os.getenv("URL")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 300))  # default 5 min

# --- Chrome options for Raspberry Pi
chrome_options = Options()
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Never save passwords
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
}
chrome_options.add_experimental_option("prefs", prefs)

# --- Chromedriver service ---
service = Service("/usr/bin/chromedriver")

# --- Start WebDriver ---
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

# --- Function to Login ---
def try_login():
    wait = WebDriverWait(driver, 5)

    # Click "Login" or "Zur Anmeldung" button
    try:
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//dx-button[@aria-label='Login' or @aria-label='Zur Anmeldung']")
            )
        )
        login_button.click()
    except:
        print("No login button found or already logged in")

    # Fill in username
    try:
        if USERNAME:
            username_box = wait.until(
                EC.element_to_be_clickable((By.NAME, "username"))
            )
            username_box.clear()
            username_box.send_keys(USERNAME)
    except:
        print("No username field found")

    # Fill in password
    try:
        if PASSWORD:
            password_box = wait.until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_box.clear()
            password_box.send_keys(PASSWORD)
            password_box.submit()
    except:
        print("No password field found or already logged in")

# --- Open website ---
driver.get(URL)
print("Page title:", driver.title)

# --- Initial login attempt ---
try_login()

# hide mouse cursor
#driver.execute_script("""
#    document.body.style.cursor = 'none';
#""")

# --- Auto-refresh loop ---
try:
    while True:
        time.sleep(REFRESH_INTERVAL)
        driver.refresh()
        print(f"Page refreshed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Try login again after refresh
        try_login()

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    driver.quit()
