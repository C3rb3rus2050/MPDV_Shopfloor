#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo apt autoremove -y

sudo apt update --fix-missing -y

sudo apt install chromium-chromedriver -y
sudo apt install chromium -y
sudo apt install chromium-browser -y
sudo apt install chromium-driver -y
sudo apt install python3-selenium -y
sudo apt install python3-dotenv

apt update --fix-missing -y



# --- Set locale, timezone, keyboard ---
echo "Starting DietPi configuration..."

# --- VARIABLES ---
# Change these to your desired settings
LOCALE="C.UTF-8"
TIMEZONE="Europe/Vienna"
KEYBOARD_LAYOUT="at"

# --- UPDATE SYSTEM (optional but recommended) ---
# echo "Updating system..."
# sudo apt update && sudo apt upgrade -y

# --- SET LOCALE ---
echo "Setting locale to $LOCALE..."
sudo sed -i "s/^# *$LOCALE/$LOCALE/" /etc/locale.gen
sudo locale-gen
sudo update-locale LANG=$LOCALE

# --- SET TIMEZONE ---
echo "Setting timezone to $TIMEZONE..."
sudo timedatectl set-timezone "$TIMEZONE"

# --- SET KEYBOARD LAYOUT ---
echo "Setting keyboard layout to $KEYBOARD_LAYOUT..."
sudo sed -i "s/XKBLAYOUT=.*/XKBLAYOUT=\"$KEYBOARD_LAYOUT\"/" /etc/default/keyboard
sudo dpkg-reconfigure -f noninteractive keyboard-configuration
sudo setupcon

# --- RESTART SERVICES TO APPLY CHANGES ---
echo "Restarting system services to apply changes..."
sudo systemctl restart keyboard-setup
sudo systemctl restart console-setup

echo "Done! Locale: $LOCALE, Timezone: $TIMEZONE, Keyboard: $KEYBOARD_LAYOUT"



CONFIG_FILE="/boot/firmware/config.txt"

# Replace dtoverlay line
sudo sed -i 's/^dtoverlay=vc4-kms-v3d/dtoverlay=vc4-fkms-v3d/' "$CONFIG_FILE"

# Replace hdmi_blanking line
sudo sed -i 's/^hdmi_blanking=1/hdmi_blanking=2/' "$CONFIG_FILE"

echo "config.txt updated successfully."

chmod +x /root/MPDV_script/MPDV.py
chmod +x /root/MPDV_script/display_schedule_daily.py

cd MPDV_script

sudo mv display_schedule_daily.service /etc/systemd/system/
sudo mv selenium_startup.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable display_schedule_daily.service
sudo systemctl start display_schedule_daily.service

sudo systemctl daemon-reload
sudo systemctl enable selenium_startup.service
sudo systemctl start selenium_startup.service

#reboot now