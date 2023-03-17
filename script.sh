#! /bin/bash

clear
sleep 2
read -p "Your Goorm Account Email: " user
read -p "Your Goorm Account Password: " passwd
read -p "Terminal Url Of Goorm Container: " console
clear
echo "Install Dependences & Webdriver..."
sudo apt update > /dev/null 2>&1
sudo apt install -y chromium=83.0.4103.116-1~deb10u3 chromium-driver=83.0.4103.116-1~deb10u3
echo "Prepare Keepalive Script..."
pip3 install -q selenium==3.141.0
wget -q -O main.bak https://github.com/ShadowObj/GoormKeepAlive/raw/main/main.py
echo "Begin To Execute Python3 Script..."
nohup python3 ./main.bak -U $user -P $passwd -C $console -DRV ./redis > /dev/null &
echo "Start Keepalive Workflow!Enjoy it!"
sleep 3
clear
