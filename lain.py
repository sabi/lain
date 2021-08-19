#!/usr/bin/python3

# Lain - CLI to Discord
# Sabi. Simple, Lightweight, but Not Beautiful.

# Copyright 2021 Sabi
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import sabi, sys, os, requests, shutil

software_name = 'lain'
version = '2.220'
server = ''
prompt = 'lain@' + server + ': '

def setup():
    sabi.sudoexit()
    cwd = sabi.cwd(software_name)
    sabi.sabifs(software_name)
    shutil.move('sabi.py',cwd + 'sabi.py')
    shutil.move('lain.py',cwd + 'lain.py')
    sabi.symlink(software_name)
    for directory in ['docs','images']:
        if not sabi.dircheck(cwd + directory):
            os.mkdir(cwd + directory)
    if not os.path.isfile(cwd + 'webhooks.conf'):
        with open(cwd + 'webhooks.conf', 'w') as wfile:
            wfile.write('# channel-name = discord-webhook\n')
            wfile.write('# movie-chat = https://discord.com/apt/webhooks/123/123\n')
            wfile.write('# For more info on getting Discord weblinks or generating this config\n')
            wfile.write('# see sabisimple.com/lain_installation.html\n')
        print('Add webhooks to your webhooks.conf\nEx: movie-chat = https://discord.com/api/123/123')
        #return 0
    #sys.exit('Lain is installed. See "lain -h" for more info')

def post_message(msg, webhook, tts=False, image=False, del_image=False):
    if image:
        first = True
        for img in os.listdir(cwd + 'images'):
            if first == True:
                requests.post(webhook, data={'content':msg}, files={'file': open('images/' + img, 'rb')})
                first = False
            else:
                requests.post(webhook, data={'content': " "}, files={'file': open('images/' + img, 'rb')})
            if del_image:
                os.remove(cwd + 'images/' + img)
    else:
        requests.post(webhook, data={'content': msg, 'tts': tts})

def help_menu():
    sys.exit('''
Lain - CLI to Discord
Sabi. Simple, Lightweight, but Not Beautiful

To install: sudo python3 lain.py install

Command Line Messages:

    Text Only:
    lain textChannel -msg This is the message to send to the textChannel
    Ex: lain sabi-general -msg Sabi is Simple, Lightweight, but Not Beautiful.

    Image Posts:
    lain textChannel -img This is optional text to post with the image
    Ex: lain sabi-general -img Sabi's logo is katakana made to look like sakura branches.

Interactive Shell:

    lain textChannel
    Ex: lain sabi-general

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
    /v  /version - Print current version\n''')

def main():
    sabi.arg_check(software_name)
    if sys.argv[1] in ['-h','--help']:
        help_menu()
    elif sys.argv[1] in ['-v','--version']:
        sys.exit(version)

    cwd = sabi.cwd(software_name)

    if 'install' in sys.argv:
        setup() # exits
        return 0

    webhooks = sabi.config_read(cwd + 'webhooks.conf')

    server = sys.argv[1]
    if server not in webhooks.keys():
        sys.exit(server + 'not found in webhooks.conf')

    webhook = webhooks[server].strip()

    msg = ''
    if '-img' in sys.argv:
        for word in sys.argv[3:]:
            msg += word + ' '
        post_message(msg, webhook, image=True)
        sys.exit(0) #TODO Check?

    elif '-msg' in sys.argv:
        for word in sys.argv[3:]:
            msg += word + ' '
        post_message(msg, webhook)
        sys.exit(0) #TODO Check?

    sabi.clear()

    # Interactive Shell
    while True:
        command = ''
        msg = input(prompt)
        if msg[0] in ['/q','/h','/v','/t','/i']:
            if ' ' in msg:
                msg.split(' ', 1)
                command = msg[0]
                msg = msg[1:]
            else:
                command = msg
                msg = ''
        if command in ['/quit','/q']:
            sys.exit(0) # TODO
        elif command in ['/help','h']:
            help_menu()
        elif command in ['/version','/v']:
            print(version)
        elif command in ['/tts','/t']:
            post_message(msg, webhook, tts=True)
        elif command in ['/image','/i']:
            post_message(msg, webhook, image=True)
        elif command in ['/change','/c']:
            if sabi.key_check(msg, webhooks):
                webhook = webhooks[msg]
            else:
                print('Available servers:\n'+str(list(webhooks.keys())))
                server = input('To which server would you like to change?\n')
                if sabi.key_check(server, webhooks):
                    webhook = webhooks[server]
        else:
            post_message(msg, webhook)

if __name__ == "__main__":
    main()
