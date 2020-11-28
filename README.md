# Lain Bot
Sabi. Simple, Lightweight, but Not Beautiful.

Quick Start
-----------------------------------------
### Create a Discord Webhook
* In a channel you moderate, right click a text channel.
* Edit Channel -> Integrations -> Create Webhook
* Copy the webhook URL into webhooks.conf
* Ex: sabi-general = https://discord.com/api/webhooks/1234/1234

### Start the Lain Bot
* `python3 bot.py nameOfServer`
* Ex: `python3 bot.py sabi-general`

Commands
----------
While in the app, you can use these commands
* /c -OR- /change
  * Change to another server.
  * Ex: /change art-commentary
  * This would change to the art-commentary
  * webhook you have in webhooks.conf
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
