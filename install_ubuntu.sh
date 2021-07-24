#!/bin/bash
echo "Installing the requirements ... "

appending source list required for the application 
sudo echo "deb http://archive.ubuntu.com/ubuntu bionic main universe" >> /etc/apt/sources.list
sudo echo "deb http://archive.ubuntu.com/ubuntu bionic-security main universe" >> /etc/apt/sources.list
sudo echo "deb http://archive.ubuntu.com/ubuntu bionic-updates main universe" >> /etc/apt/sources.list

echo "Updating source lists"
sudo apt update 

echo "Installing python"
sudo apt install -y python3-pip
sudo apt-get install -y libcairo2-dev libgirepository1.0-dev

echo "Updating requirements file"
pw=$(pwd | tr -d '\r')

cd $pw
pip3 freeze > requirements.txt

echo "Installing application requirements"
pip3 install -r requirements.txt
pip3 install discord
pip3 install web3
pip3 install python-crontab

echo "Giving user permissions to the bot directory"
sudo chown -R $name:$name $pw

# Replace the fake path in cronjobs by your actual path
echo "Updating files with your path"
sed -i 's/\/home\/USER\/DiscordBotSLP\/DiscordBotSLP.py/'$(echo $pw | sed 's/\//\\\//g')'\/DiscordBotSLP.py/g' cron.py
sed -i 's/\/home\/USER\/DiscordBotSLP\/DiscordBotSLP.py/'$(echo $pw | sed 's/\//\\\//g')'\/DiscordBotSLP.py/g' cron.sh

# Create daemon of the bot
touch "/lib/systemd/system/discordqrbot.service"
printf "[Unit]
Description=Discord SLP Bot
After=multi-user.target
Conflicts=getty@tty1.service
[Service]
Type=simple
ExecStart=/usr/bin/python3 "$pw"/DiscordBotSLP.py
StandardInput=tty-force
[Install]
WantedBy=multi-user.target
" > /lib/systemd/system/discordqrbot.service

sudo systemctl daemon-reload
sudo systemctl enable discordqrbot.service
sudo systemctl start discordqrbot.service
sudo systemctl status discordqrbot.service