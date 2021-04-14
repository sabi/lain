# Lain
Sabi. Simple, Lightweight, but Not Beautiful.

Installation
-----------------------------------------
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
* Ex: /image This is a picture of my dog

Commands
----------
While in the app, you can use these commands
* /c -OR- /change
  * Change to another server.
  * Ex: /change art-commentary
  * This would change to the art-commentary
  * webhook you have in webhooks.conf
* /d -OR- /clear
  * Clear the screen
* /i -OR- /image
  * Attach an image to your post.
  * Ex: /image This is a pic of me and my dog!
  * You can also post a pic with no caption by
  * not including additional text in the post
* /q -OR- /quit
  * Exit the Lain Bot controls
* /s -OR- /server
  * Print the name of the current webhook
  * you are using.
* /t -OR- /tts
  * Enable text-to-speech on your post
  * Ex: /tts This message is being read out loud!
* /v -OR- /version
  * Print current version
