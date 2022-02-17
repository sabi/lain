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

import requests
import os
import sys

version = '3.03'

def read_config():
    home = os.path.expanduser('~')
    config_dict = {}
    with open(home + '/.config/sabi/lain/webhooks.conf', 'r') as cfile:
        for line in cfile.readlines():
            if line[0] == '#': # remove comments
                continue
            line = line.split('=')
            while line[0][-1] == ' ': # remove whitespace
                line[0] = line[0][:-1]
            while line[1][0] == ' ':
                line[1] = line[1][1:]
            config_dict[line[0]] = line[1]
    return config_dict # dictionary

def post_message(webhook, msg, tts=False, image=False, image_path=''):
    if image:
        requests.post(webhook, data={'content':msg}, files={'file': open(image_path, 'rb')})
    else:
        requests.post(webhook, data={'content': msg, 'tts': tts})
    sys.exit()

def help_menu():
    sys.exit('''
Lain - CLI to Discord
Sabi. Simple, Lightweight, but Not Beautiful
Command Line Messages:
    Text Only:
        lain textChannel -msg This is the message to send to the textChannel
        Ex: lain sabi-general -msg Sabi is Simple, Lightweight, but Not Beautiful.
    
    Image Posts:
        lain textChannel -img This is optional text to post with the image
        Ex: lain sabi-general -img Sabi's logo is katakana made to look like sakura branches.''')

def main():
    home = os.path.expanduser('~')
    os.makedirs(home + '/.config/sabi/lain/', exist_ok=True)
    if not os.path.isfile(home + '/.config/sabi/lain/webhooks.conf'):
        with open( home + '/.config/sabi/lain/webhooks.conf', 'w') as wfile:
            wfile.write('# channel-name = discord-webhook\n')
            wfile.write('# movie-chat = https://discord.com/apt/webhooks/123/123\n')
            sys.exit('Please add a webhook to ~/.config/sabi/lain/webhooks.conf')
    if len(sys.argv) == 1:
        help_menu()
    if sys.argv[1] in ['-h','--help']:
        help_menu()
    elif sys.argv[1] in ['-v','--version']:
        sys.exit(version)
    elif len(sys.argv) < 3:
        help_menu()

    webhook = sys.argv[1]
    webhooks = read_config()
    
    if webhook not in webhooks:
        sys.exit('Webhook not found in ~/.config/sabi/lain/webhooks.conf')
    webhook = webhooks[webhook].strip()
    if sys.argv[2] in ['-i','-img','--img']:
        post_message(webhook, msg=' ', image=True, image_path=sys.argv[3])
    elif sys.argv[2] in ['-m','-msg','--msg']:
        msg = ''
        for word in sys.argv[3:]:
            msg += word + ' '
        post_message(webhook, msg)
    elif sys.argv[2] in ['-t','-tts','--tts']:
        msg = ''
        for word in sys.argv[3:]:
            msg += word + ' '
        post_message(webhook, msg, tts=True)
    
if __name__ == '__main__':
    main()
