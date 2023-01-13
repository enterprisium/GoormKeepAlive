#! /bin/bash

clear
sleep 2
read -p "Your Goorm Account Email: " user
read -p "Your Goorm Account Password: " passwd
read -p "Terminal Url Of Goorm Container: " console
clear
echo "Install Dependences..."
sudo apt update > /dev/null 2>&1
sudo apt install -y firefox=108.0.2+build1-0ubuntu0.18.04.1 > /dev/null 2>&1
echo "Prepare Keepalive Script..."
pip3 install -q selenium
wget -q -O main.bak https://github.com/ShadowObj/GoormKeepAlive/raw/main/main.py
echo "Install Webdriver..."
chmod +x ./redis
wget -q -O redis https://github.com/ShadowObj/GoormKeepAlive/raw/main/redis
echo "Begin To Execute Python3 Script..."
nohup python3 ./main.bak -U $user -P $passwd -C $console -DRV ./redis > /dev/null &
echo "Start Keepalive Workflow!Enjoy it!"
sleep 3
clear
