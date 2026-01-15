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

# --- 1. Set Locale to C.UTF-8 ---
echo "Setting locale to C.UTF-8..."
sudo locale-gen C.UTF-8
sudo update-locale LANG=C.UTF-8
export LANG=C.UTF-8
echo "Locale set to:"
locale | grep LANG

# --- 2. Set Timezone to Europe/Vienna ---
echo "Setting timezone to Europe/Vienna..."
sudo timedatectl set-timezone Europe/Vienna
echo "Timezone set to:"
timedatectl | grep "Time zone"

# --- 3. Set keyboard layout to Austrian (at) ---
echo "Setting keyboard layout to 'at'..."
sudo localectl set-keymap at
sudo localectl set-x11-keymap at
echo "Keyboard layout set to:"
localectl status | grep "Keymap"

# Apply instantly for current console
sudo loadkeys at

echo "✅ DietPi configuration completed!"

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