# WEN SLP ?!?

![](https://github.com/vmercadi/DiscordBotSLP/blob/main/img/slpbot.png)

## Description

A simple discord bot for Axie Infinity, to let your scholars know when SLP are claimable.  
**Very** inspired by : https://github.com/ZracheSs-xyZ/QrCodeBot-xyZ

## Install

- Start a ubuntu VM or server (AWS, GCP, ...)
- Inside the VM, clone this repository : `git clone https://github.com/vmercadi/DiscordBotSLP.git`
- [Follow this tutorial to create and add a bot to your Discord Server](https://discordpy.readthedocs.io/en/stable/discord.html)
- Edit the **SecretStorage.py** file with the token of your bot and informations about your scholars
- Then let's start the install : `chmod +x install-ubuntu.sh; sudo ./install-ubuntu.sh`

Everything should be good now and you should see the bot on your server if you added it.  
You can confirm by typing the command : `ps -ef | grep DiscordBotSLP.py` 

## Usage

The scholar can use the command `$wen`  
It must be done in a Discord channel where the bot is enabled.
