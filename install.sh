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

cd
rm install.sh

cd MPDV_script

wget --content-disposition "https://data.amhs.at/f/53b5311b3e2b4d35b9d5/?dl=1"

sudo pcmanfm --set-wallpaper="/root/MPDV_script/AMK_Logo.jpg"

reboot now