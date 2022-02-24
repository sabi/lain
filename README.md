# Lain
Sabi. Simple, Lightweight, but Not Beautiful.

## Overview
- Lain is a Linux command line utility that allows you to script messages to Discord. 

## Setup
- Effortless install: `sudo apt update && sudo apt install -y python3 python3-pip wget && pip3 install requests && wget https://raw.githubusercontent.com/sabi/lain/main/lain.py && python3 lain.py`

- `python3 lain.py`
- Add webhooks to `~/.config/sabi/lain/webhooks.conf` in the format:
  - `channel-name = https://discord.com/api/123/123`

## Usage
- Send a message
  - `lain <channel> -msg <Replace with message>`
  - `lain friends -msg Let's love Lain!`
- Send an image
  - `lain <channel> -img </path/to/image>`
  - `lain friends -img /home/lain/Pictures/selfie.jpg`

## How to create a Discord webhook
- Open your Server Settings, then go to Integrations
![image](https://user-images.githubusercontent.com/49737728/146336626-2e511660-dd73-4fe9-8b50-4a211d27d2a3.png)

- Create a new webhook for the appropriate channel, then copy the webhook to clipboard
![image](https://support.discord.com/hc/article_attachments/1500000455142/Screen_Shot_2020-12-15_at_4.45.52_PM.png)

- Finally add the webhook to `~/.config/sabi/lain/webhooks.conf` in the format:
  - `channel-name = https://discord.com/api/123/123` 
