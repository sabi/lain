#!/usr/bin/python3

# Lain Bot for Discord
# Sabi. Simple, Lightweight, but Not Beautiful.

import sys, os, requests

version = '1.0'

webhooks = {}
cwd = os.path.abspath(os.path.dirname(__file__)) + '/'

def clear():
    if os.name != 'nt':
        os.system('clear')
    else:
        os.system('cls')
    print('Input message and hit Enter to send. /help for more info.\n')

def postMessage(msg, webhook, tts=False, image=False):
    if image:
        first = True
        for img in os.listdir('images'):
            if first == True:
                requests.post(webhook, data={'content': msg}, files={'file': open('images/' + img, 'rb')})
                first = False
            else:
                requests.post(webhook, data={'content': " "}, files={'file': open('images/' + img, 'rb')})
            os.remove('images/' + img)
    else:
        requests.post(webhook, data={'content': msg, 'tts': tts})

def readConfigOrDie():
    if not os.path.isfile(cwd + 'webhooks.conf'):
        sys.exit('Your webhooks.conf is missing')
    with open('webhooks.conf','r') as ifile:
        for i in ifile.readlines():
            i = i.split('=')
            while i[0][-1] == ' ':
                i[0] = i[0][:-1]
            while i[1][0] == ' ':
                i[1] = i[1][1:]
            webhooks[i[0]] = i[1].strip()
    return webhooks

def helpMenu():
    print("""
    Command Line Messages:

    python3 bot.py textChannel -msg This is the message to send to the textChannel
    Ex: python3 bot.py sabi-general -msg Sabi is Simple, Lightweight, but Not Beautiful.

    Interactive Shell:
    python3 bot.py textChannel
    Ex: python3 bot.py sabi-general

    /c  /change  - Change to another server.
                 Ex: /change art-commentary
                 This would change to the art-commentary
                 webhook you have in webhooks.conf
    /d  /clear   - Clear screen
    /i  /image   - Attach an image to your post.
                 Ex: /image This is a pic of me and my dog!
                 You can also post a pic with no caption by
                 not including additional text in the post
    /q  /quit    - Exit the Lain Bot controls
    /s  /server  - Print the name of the current webhook
                 you are using.
    /t  /tts     - Enable text-to-speech on your post
                 Ex: /tts This message is being read out loud!
    /v  /version - Print current version
    """)

def serverCheck(server, webhook):
    if server in webhooks.keys():
        webhook = webhooks[server]
    else:
        print(server + ' is not found in available webhooks.')
        print('Available servers:\n'+ str(servers))
    return webhook

# Start Program #

webhooks = readConfigOrDie()
servers = list(webhooks.keys())
if len(sys.argv) < 2:
    sys.exit('You need a server as an argument.\nAvailable servers:\n'+ str(servers))
if sys.argv[1] in ['-h','--help']:
    helpMenu()
    sys.exit()
elif sys.argv[1] in ['-v','--version']:
    sys.exit(version)
server = sys.argv[1]
if server in webhooks.keys():
    webhook = webhooks[server]
else:
    sys.exit('Error: ' + server + ' not in webhooks')
clear()

if '-msg' in sys.argv:
    msgArg = sys.argv[sys.argv.index('-msg') + 1:]
    msg = ""
    for i in msgArg:
        msg += i + ' '
    postMessage(msg, webhook)
else:
    while True:
        msg = input('lainbot@' + server + ': ')
        if msg[0:6] == '/quit' or msg[0:2] == '/q':
            sys.exit()
        elif msg[0:7] == '/clear' or msg[0:2] =='/d':
            clear()
        elif msg[0:6] == '/help' or msg[0:2] == '/h':
            helpMenu()
        elif msg[0:8] == '/server' or msg[0:2] == '/s':
            print('Current server: ' + server)
        elif msg[0:9] == '/version' or msg[0:2] == '/v':
            print('Current version: ' + version)
        elif msg[0:4] == '/tts' or msg[0:2] == '/t':
            msg = msg.split(' ',1)[1]
            postMessage(msg, webhook, tts=True)
        elif msg[0:7] == '/image' or msg[0:2] == '/i':
            if " " in msg:
                msg = msg.split(' ',1)[1]
                postMessage(msg, webhook, image=True)
            else:
                postMessage(' ', webhook, image=True)
        elif msg[0:7] == '/change' or msg[0:2] == '/c':
            if " " in msg:
                server = msg.split(' ',1)[1]
                webhook = serverCheck(server, webhook)
            else:
                print('Available servers:\n'+ str(servers))
                server = input('To which server would you like to change?\n')
                webhook = serverCheck(server, webhook)
        else:
            postMessage(msg, webhook)
