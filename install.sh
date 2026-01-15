# System Update install dependencies

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


# Add Docker's official GPG key:
apt-get update
apt-get install ca-certificates curl -y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

sudo rm -r Proxmox_Scripts/

reboot now