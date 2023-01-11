#! /bin/bash

clear
read -p "Your Goorm Account Email: " user  
read -sp "Your Goorm Account Password:" passwd 
echo "Install Dependences..."
sudo apt update > /dev/null 2>&1
sudo apt install -y firefox firefox-geckodriver python3 python3-pip > /dev/null 2>&1
echo "Install Python3 Modules..."
pip3 install -q selenium
wget -q -O main.py https://github.com/ShadowObj/GoormKeepAlive/raw/main/main.py
echo "Begin To Execute Python3 Script..."
nohup python3 main.py -U $user -P $passwd > /dev/null &
echo "Start Keepalive Workflow!Enjoy it!"
sleep(2)
clear
