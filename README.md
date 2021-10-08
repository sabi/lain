# Lain
Sabi. Simple, Lightweight, but Not Beautiful.

Installation
-----------------------------------------
* Download lain.py and [sabi.py](https://github.com/sabi/sabi/blob/main/sabi.py) to the same directory
* Run `sudo python3 lain.py install` to be installed at /opt/sabi/lain/ (Recommended)
* -OR- Run `python3 lain.py install --local-install` to be installed in local path

Quick Start
-----------------------------------------
### Create a Discord Webhook
* In a channel you moderate, right click a text channel.
* Edit Channel -> Integrations -> Create Webhook
* Copy the webhook URL into webhooks.conf
* Ex: `sabi-general = https://discord.com/api/webhooks/1234/1234`
### Message from the command line for scripting ease
* `lain nameOfServer -msg This is the message to send to the textChannel.` 
* `lain sabi-general -msg Sabi is Simple, Lightweight, but Not Beautiful.`
### Start the Lain Bot (Interactive Shell)
* `lain nameOfServer`
* Ex: `lain sabi-general`
#### How do you attach pictures (Interactive Shell)?
* Add any pics you want in your next post to the `images` directory
* Lain will post all pics in the directory, then move them to `posted` directory to be purged
* First pic will receive the caption, all subsequent pics will just be posted without a caption
