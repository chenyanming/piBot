#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# import sys
import os
import re
import time, datetime
import unicodedata
from os.path import splitext
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from forex_python.converter import CurrencyRates
import json

c = CurrencyRates()
now = datetime.datetime.now()

import shlex
from subprocess import Popen, PIPE


import pexpect
pythonMode = pexpect.spawnu('/usr/bin/python3')
pythonMode.expect('>>>')

pythonModeEnable = False
shellModeEnable = True


import logging
logging.basicConfig(level=logging.DEBUG)
logging.info("Start Pibot!")




whitelist = [896631342]

#
# SIMPLE REPLY
#
def action(msg):
	chat_id = msg['chat']['id']
	command = msg['text']

	if not chat_id in whitelist:
		print("Invalid Chat ID: ", chat_id)
		return
	else:
		print("Valid Chat ID: ", chat_id)
		print('Command: ', command)

	if command == '/hi':
		telegram_bot.sendMessage (chat_id, str("Hi! This is PiBot."))
	elif command == '/time':
		telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
	elif command == '/godaddy':
		telegram_bot.sendDocument(chat_id, document=open('/home/pi/godaddy.log'))
	# elif command == '/audio':
	# 	telegram_bot.sendAudio(chat_id, audio=open('/home/pi/Desktop/Mittens.mp3'))
	elif command == '/ip':
		telegram_bot.sendMessage(chat_id, str(get_exitcode_stdout_stderr("curl -s 'https://api.ipify.org/?format=json'")))
	elif command == '/apache2':
		telegram_bot.sendMessage(chat_id, str(get_exitcode_stdout_stderr("sudo systemctl is-active apache2")))
	elif command == '/mysql':
		telegram_bot.sendMessage(chat_id, str(get_exitcode_stdout_stderr("sudo systemctl is-active mysql")))
	elif command == '/speed':
		telegram_bot.sendMessage(chat_id, str(get_exitcode_stdout_stderr("/home/pi/speedtest.sh")))
	# elif command == '/file':
	# 	telegram_bot.sendDocument(chat_id, document=open(str(get_exitcode_stdout_stderr("ls *.webm"))))
	else:
		#print('./'+command)
		try:
			telegram_bot.sendMessage(chat_id, str(get_exitcode_stdout_stderr(command)))
		except:
			pass
		# try:
		# telegram_bot.sendDocument(chat_id, document=open(command, 'rb'))
		# except:
		# 	pass

#
# SPLIT COMMAND
#
def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    # return exitcode, out.decode("utf-8"), err
    return out.decode("utf-8")

#
# Split and Send long telegram message
#
def sendMessageAdvanced(chat_id, s):
    for i in range(0,len(s),4096):
        telegram_bot.sendMessage(chat_id, str('*' + s[i:i+4096] + '*'), parse_mode="Markdown")


#
# SLUGIFY
#
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    file, ext = splitext(value)
    value = str(file)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value) + ext



#
# INLINE KEYBOARD
#
def on_chat_message(msg):
    global pythonMode, pythonModeEnable, shellModeEnable
    content_type, chat_type, chat_id = telepot.glance(msg)
    logging.info('Received Content Type: %s', content_type)
    command =''
    if content_type == 'text':
        command = msg['text']
        logging.debug(command)

    elif content_type == 'photo':
        file_id = msg['photo']#['file_id']
        logging.info(file_id)

    elif content_type == 'document':
        file_id = msg['document']['mime_type']
        logging.info(msg['document'])
        logging.info(file_id)
#'mime_type': 'application/x-bittorrent'

    # filter out valid users
    if not chat_id in whitelist:
        logging.warning("Invalid Chat ID: %s", chat_id)
        return
    else:
        logging.info("Valid Chat ID: %s", chat_id)
        # print('Command: ', msg['text'])






    if command == '/help' or command =='#help':

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       # [InlineKeyboardButton(text='Python', callback_data='Python')],
                       # [InlineKeyboardButton(text='Weather', callback_data='Weather')],
                       # [InlineKeyboardButton(text='Godaddy', callback_data='Godaddy')],
                       [InlineKeyboardButton(text='IP', callback_data='IP')],
                       [InlineKeyboardButton(text='Python Mode', callback_data='Python Mode')],
                       [InlineKeyboardButton(text='Restart Python Terminal', callback_data='Restart Python Terminal')],
                       # [InlineKeyboardButton(text='Currency - HKD', callback_data='Currency - HKD')],
                       # [InlineKeyboardButton(text='Currency - CNY', callback_data='Currency - CNY')],
                       # [InlineKeyboardButton(text='Currency - USD', callback_data='Currency - USD')],
                       # [InlineKeyboardButton(text='News', callback_data='News')],
                       [InlineKeyboardButton(text='Recently Added Books', callback_data='Calibre_New')],
                       ])
        telegram_bot.sendMessage(chat_id,
            '*Functions*\n' +
            '[Youtube m4a downlaod](https://www.youtube.com/) - Send a youtube link to Pibot, Pibot downloads the music and send back the sound file (Up to 50MB)\n'+
            '[Aria2 BT download](https://hkvim.com) - Send a BT file to Pibot to trigger the server download\n' +
            '[Import Ebook](https://book.hkvim.com/calibre) - send a pdf/mobi/epub/azw3 file to Pibot to backup the ebook to calibre library (Up to 20MB)\n'+
            '[Run terninal command](https://hkvim.com) - send a message to Pibot, pibot will take it as a normal command and issue it. If you send it the python source codes, it will run it!\n'+
            '[Calculator](https://docs.python.org/3/library/math.html) - send a formula to Pibot, start from a number or a parenthesis, you can use Built-in Functions as well\n'+
            '[Hex/Bin to Dec Converter](https://docs.python.org/3/library/math.html) - send an hex (0x) or bin (0b) to Pibot\n'+
            '[Python Mode](https://pexpect.readthedocs.io/en/stable/index.html) - Turn on/off Python Mode\n\n'+
            '*Commands*\n' +
            '/help - manual\n'+
            '/mode - show mode status\n'+
            '#mode python - switch to python mode\n' +
            '#mode restart python - restart python\n' +
            '#mode shell - switch to shell mode\n' +
            '#youtube videorul - Youtube video downlaod\n' +
            '#download http|magnet - Aria2 download\n'+
            '#booksearch word - Calibre search\n'+
            '#bookshow id - Calibre show\n'+
            '#bookexport id - Calibre export"\n'+
            # '#hex decimal number - Convert int to hex\n'+
            # '#int hex number - Convert hex to int\n'+
            '#hkd number - Convert hkd to cny, usd\n'+
            '#cny number - Convert cny to hkd, usd\n'+
            '#usd number - Convert usd to hkd, cny\n'+
            '#jpy number - Convert jpy to hkd, cny\n'+
            '#search keyword - Duck duck go search\n'+
            '#preview keyword - Duck duck go search and preview\n'+
            '#py command - Run interative python command\n',
            parse_mode="Markdown", disable_web_page_preview=True)
        telegram_bot.sendMessage(chat_id, 'You can perform the following shortcuts:', reply_markup=keyboard)

    elif command == '/mode' or command =='#mode':
        if pythonModeEnable == True:
            telegram_bot.sendMessage(chat_id, 'Python Mode is: ON', parse_mode="Markdown")

        if shellModeEnable == True:
            telegram_bot.sendMessage(chat_id, 'Shell Mode is: ON', parse_mode="Markdown")


    elif re.match('/mode .*|#mode .*',command):
        # Enable python mode
        if re.search(r'(?<=/mode )(.*)|(?<=#mode )(.*)', command).group() == 'python':
            pythonModeEnable = True
            shellModeEnable = False
            telegram_bot.sendMessage(chat_id, 'Python Mode is: ON', parse_mode="Markdown")
            # telegram_bot.sendMessage(chat_id, 'Deleting keyboard', reply_markup=ReplyKeyboardRemove())
            telegram_bot.sendMessage(chat_id, 'Python Keyboarad is On',
                    # reply_markup=ReplyKeyboardMarkup(
                    #     keyboard=[
                    #        [KeyboardButton(text='7'),KeyboardButton(text='8'),KeyboardButton(text='9'),KeyboardButton(text='*')],
                    #        [KeyboardButton(text='4'),KeyboardButton(text='5'),KeyboardButton(text='6'),KeyboardButton(text='/')],
                    #        [KeyboardButton(text='1'),KeyboardButton(text='2'),KeyboardButton(text='3'),KeyboardButton(text='-')],
                    #        [KeyboardButton(text='0'),KeyboardButton(text='.'),KeyboardButton(text='='),KeyboardButton(text='+')]
                    #     ]
                    # ))
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                           [KeyboardButton(text='/mode shell'),KeyboardButton(text='/mode')],
                           [KeyboardButton(text='/mode restart python'),KeyboardButton(text='/help')]
                           ],one_time_keyboard=True
                    ))


        # Enable shell mode
        elif re.search(r'(?<=/mode )(.*)|(?<=#mode )(.*)', command).group() == 'shell':
            pythonModeEnable = False
            shellModeEnable = True
            telegram_bot.sendMessage(chat_id, 'Shell Mode is: ON', parse_mode="Markdown")
            # telegram_bot.sendMessage(chat_id, 'Deleting keyboard', reply_markup=ReplyKeyboardRemove())
            telegram_bot.sendMessage(chat_id, 'Shell Keyboarad is On',
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                           [KeyboardButton(text='/mode python'),KeyboardButton(text='/hkd 100')],
                           [KeyboardButton(text='/cny 100'),KeyboardButton(text='/help')]
                           ],one_time_keyboard=True
                    ))


        # Restart python
        elif re.search(r'(?<=/mode )(.*)|(?<=#mode )(.*)', command).group() == 'restart python':
            pythonMode.kill(1)
            pythonMode = pexpect.spawnu('/usr/bin/python3')
            pythonMode.expect('>>>')
            telegram_bot.sendMessage(chat_id, str("Python Terminal Restarted"))
            # telegram_bot.sendMessage(chat_id, str('Python Mode is: ') + str(pythonModeEnable))
        else:
            telegram_bot.sendMessage(chat_id, str("mode command error"))


    elif pythonModeEnable == True:

        try:
            # telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "import math\nprint(' + re.search(r'(?<=/cal )(.*)|(?<=#cal )(.*)|(^[0-9].*)|([\(].*)$', command).group() + ')"') + '*'), parse_mode="Markdown") #Return the output
            # pythonMode.sendline(str(re.search(r'(?<=/py )(.*)|(?<=#py )(.*)', command).group()))
            pythonMode.sendline(str(command))
            pythonMode.expect('>>>')
            if str(pythonMode.before[len(command)+3:]) != '': # if the output is not empty, normally it is import command
                telegram_bot.sendMessage(chat_id, str(pythonMode.before[len(command)+3:] )) #Return the output

        except Exception as e:
            telegram_bot.sendMessage(chat_id, 'python mode command Error:\n' + str(e))
        return

    elif shellModeEnable == True:

        #
        # 1. Youtube m4a downlaod
        # Usage: forward a youtube link to Pibot, Pibot downloads the music and send back the sound file
        # Limit: up to 50 MB
        #
        if re.match('https://www.youtube.com.*|https://youtu.be.*|https://music.youtube.com.*',command):
            try:
                # telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('youtube-dl --extract-audio --audio-format mp3 ' + command) + '*'), parse_mode="Markdown") #Return the output
                # telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('youtube-dl -f bestaudio[ext=m4a] --embed-thumbnail --add-metadata -o "%(title)s.%(ext)s" ' + command) + '*'), parse_mode="Markdown") #Return the output
                get_exitcode_stdout_stderr('youtube-dl -f bestaudio[ext=m4a] --embed-thumbnail --add-metadata -o "/media/pi/ShareDrive/Download/%(title)s.%(ext)s" ' + command)
            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'Youtube-dl Command Error:\n' + str(e))

            try:
                # Get File Name, split by ., then get the name without extension
                # telegram_bot.sendAudio(chat_id, audio=open('/media/pi/ShareDrive/Download/' + get_exitcode_stdout_stderr('youtube-dl --skip-download  --get-filename -o "%(title)s.%(ext)s" ' +  re.search('https://.*', command).group() ).split('.')[0] + '.m4a', 'rb'))
                # telegram_bot.sendAudio(chat_id, audio=open('/media/pi/ShareDrive/Download/' + get_exitcode_stdout_stderr('youtube-dl --skip-download  --get-title ' +  command ).rstrip() + '.m4a', 'rb'))
                telegram_bot.sendAudio(chat_id, audio=open(get_exitcode_stdout_stderr('ls -At /media/pi/ShareDrive/Download/').split('\n')[0], 'rb')) # send the lastest file
            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'Send Audio Error, please send manually!\n' + str(e))

        #
        # 2. Youtube video downlaod
        # Usage: input "/youtube video_url"
        #
        elif re.match('/y .*|#y .*',command):
            try:
                # get_exitcode_stdout_stderr('youtube-dl ' + command)
                sendMessageAdvanced(chat_id, get_exitcode_stdout_stderr('youtube-dl --no-progress --write-sub --write-auto-sub --sub-lang "en,ja,zh-Hans,zh-Hant" -o "/media/pi/ShareDrive/Download/%(title)s.%(ext)s" ' + re.search('https://.*', command).group()))
            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'Youtube-dl video Error:\n' + str(e))
        #
        # 3. Aria2 download
        # Usage: input "/download http|magnet..."
        #
        elif re.match('/download .*|#download .*',command):
            try:
                telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python /home/pi/Documents/aria2rpc/aria2rpc.py --cookie "id=xxx; name=yyy;" --dir /media/pi/ShareDrive/Download --rpc http://127.0.0.1:6800/jsonrpc ' + re.search('http.*|magnet.*', command).group()) + '*'), parse_mode="Markdown") #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'Aria2 Command Error:\n' + str(e))


        #
        # 4. Aria2 BT download / Ebook backup
        # Usage: send a BT file to Pibot to trigger the server download; send a pdf/mobi/epub/azw3 file to Pibot to backup the ebook to calibre library
        # Limit: up to 20MB
        #
        elif content_type == 'document':
            ebookName = slugify(msg['document']['file_name'], True)
            # now = str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')) + '.pdf'

            if msg['document']['mime_type'] == 'application/x-bittorrent':
                try:
                    btFile = 'https://api.telegram.org/file/bot' + '914501764:AAEc5t9sEaIm8Ro4a0lwhr2aGc_LpUQacOQ/' + telegram_bot.getFile(msg['document']['file_id'])['file_path']
                    telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python /home/pi/Documents/aria2rpc/aria2rpc.py --cookie "id=xxx; name=yyy;" --dir /media/pi/ShareDrive/Download --rpc http://127.0.0.1:6800/jsonrpc ' + btFile) + '*'), parse_mode="Markdown") #Return the output

                except Exception as e:
                    telegram_bot.sendMessage(chat_id, 'Aria2 Command Error:\n' + str(e))
            elif msg['document']['mime_type'] == 'application/pdf':
                try:
                    telegram_bot.download_file(msg['document']['file_id'], '/media/pi/ShareDrive/Download/' + ebookName)
                    telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr("calibredb add --library-path /media/pi/ShareDrive/Documents/Library --duplicates --tags telegram " + ebookName) + '*'), parse_mode="Markdown") #Return the output
                    # calibredb remove --library-path /media/pi/ShareDrive/Documents/Library 10799
                except Exception as e:
                    telegram_bot.sendMessage(chat_id, 'PDF Upload Error:\n' + str(e))
            elif msg['document']['mime_type'] == 'application/x-mobipocket-ebook':
                try:
                    telegram_bot.download_file(msg['document']['file_id'], '/media/pi/ShareDrive/Download/' + ebookName)
                    telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('calibredb add --library-path /media/pi/ShareDrive/Documents/Library --duplicates --tags telegram ' + ebookName) + '*'), parse_mode="Markdown") #Return the output
                except Exception as e:
                    telegram_bot.sendMessage(chat_id, 'MOBI/AZW3 upload Error:\n' + str(e))
            elif msg['document']['mime_type'] == 'application/epub+zip':
                try:
                    telegram_bot.download_file(msg['document']['file_id'], '/media/pi/ShareDrive/Download/' + ebookName)
                    telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('calibredb add --library-path /media/pi/ShareDrive/Documents/Library --duplicates --tags telegram ' + ebookName) + '*'), parse_mode="Markdown") #Return the output
                except Exception as e:
                    telegram_bot.sendMessage(chat_id, 'EPUB upload Error:\n' + str(e))
            else:
                telegram_bot.sendMessage(chat_id, str('*This type of file ' + msg['document']['mime_type'] + ' is not supported.*'), parse_mode="Markdown")


        elif content_type == 'photo':
            pass
        elif content_type == 'location':
            pass
        elif content_type == 'voice':
            pass
        #
        # 5. Calibre search
        # Usage: input "/booksearch word"
        #
        elif re.match('/booksearch .*|#booksearch .*',command):
            try:
                # search the characters after 'booksearch '
                telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('calibredb list --library-path /media/pi/ShareDrive/Documents/Library --field title --search ' + re.search(r'(?<=/booksearch )(.*)|(?<=#booksearch )(.*)', command).group()) + '*'), parse_mode="Markdown") #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'booksearch Command Error:\n' + str(e))
        #
        # 6. Calibre show
        # Usage: input "/bookshow id"
        #
        elif re.match('/bookshow .*|#bookshow .*',command):
            try:
                # search the characters after 'booksearch '
                telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('calibredb show_metadata --library-path /media/pi/ShareDrive/Documents/Library ' + re.search(r'(?<=/bookshow )(.*)|(?<=#bookshow )(.*)', command).group()) + '*'), parse_mode="Markdown") #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'bookshow Command Error:\n' + str(e))
        #
        # 7. Calibre export
        # Usage: input "/bookexport id"
        #
        elif re.match('/bookexport .*|#bookexport .*',command):
            try:
                # search the characters after 'booksearch '
                telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('calibredb export --library-path /media/pi/ShareDrive/Documents/Library --dont-save-cover --dont-update-metadata --dont-asciiize --dont-write-opf --single-dir --to-dir /media/pi/ShareDrive/Download --progress ' + re.search(r'(?<=/bookexport )(.*)|(?<=#bookexport )(.*)', command).group()) + '*'), parse_mode="Markdown") #Return the output
                # send out the most recent file
                telegram_bot.sendDocument(chat_id, document=open(get_exitcode_stdout_stderr('ls -At /media/pi/ShareDrive/Download/').split('\n')[0], 'rb')) # send the lastest file

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'bookexport command Error:\n' + str(e))

        #
        # 8. Convert int to hex
        # Usage: input "/hex decimal number"
        #
        # elif re.match('/hex .*|#hex .*',command):
        #     try:
        #         # search the characters after 'booksearch '
        #         telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "print(hex(' + re.search(r'(?<=/hex )(.*)|(?<=#hex )(.*)', command).group() + '))"') + '*'), parse_mode="Markdown") #Return the output

        #     except Exception as e:
        #         telegram_bot.sendMessage(chat_id, 'hex command Error:\n' + str(e))
        #
        # 9. Convert hex to int
        # Usage: input "/int hex number"
        #
        # elif re.match('/int .*|#int .*',command):
        #     try:
        #         # search the characters after 'booksearch '
        #         telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "print(int(' + re.search(r'(?<=/int )(.*)|(?<=#int )(.*)', command).group() + '))"') + '*'), parse_mode="Markdown") #Return the output

        #     except Exception as e:
        #         telegram_bot.sendMessage(chat_id, 'int command Error:\n' + str(e))
        #
        # 10. Convert hkd to cny, usd
        # Usage: input "/hkd number"
        #
        elif re.match('/hkd .*|#hkd .*',command):
            try:
                # search the characters after 'booksearch '
                telegram_bot.sendMessage(chat_id, str('*CNY  ￥' + str(c.convert('HKD', 'CNY', float(re.search(r'(?<=/hkd )(.*)|(?<=#hkd )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output
                telegram_bot.sendMessage(chat_id, str('*USD  $ ' + str(c.convert('HKD', 'USD', float(re.search(r'(?<=/hkd )(.*)|(?<=#hkd )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'hkd command Error:\n' + str(e))
        #
        # 11. Convert cny to hkd, usd
        # Usage: input "/cny number"
        #
        elif re.match('/cny .*|#cny .*',command):
            try:
                # search the characters after 'booksearch '
                telegram_bot.sendMessage(chat_id, str('*HKD  $ ' + str(c.convert('CNY', 'HKD', float(re.search(r'(?<=/cny )(.*)|(?<=#cny )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output
                telegram_bot.sendMessage(chat_id, str('*USD  $ ' + str(c.convert('CNY', 'USD', float(re.search(r'(?<=/cny )(.*)|(?<=#cny )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'cny command Error:\n' + str(e))
        #
        # 12. Convert usd to hkd, cny
        # Usage: input "/cny number"
        #
        elif re.match('/usd .*|#usd .*',command):
            try:
                # search the characters after 'booksearch '
                telegram_bot.sendMessage(chat_id, str('*HKD  $ ' + str(c.convert('USD', 'HKD', float(re.search(r'(?<=/usd )(.*)|(?<=#usd )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output
                telegram_bot.sendMessage(chat_id, str('*CNY  ￥' + str(c.convert('USD', 'CNY', float(re.search(r'(?<=/usd )(.*)|(?<=#usd )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'usd command Error:\n' + str(e))
        #
        # 12. Convert jpy to hkd, cny
        # Usage: input "/jpy number"
        #
        elif re.match('/jpy .*|#jpy .*',command):
            try:
                # search the characters after 'booksearch '
                telegram_bot.sendMessage(chat_id, str('*HKD  $ ' + str(c.convert('JPY', 'HKD', float(re.search(r'(?<=/jpy )(.*)|(?<=#jpy )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output
                telegram_bot.sendMessage(chat_id, str('*CNY  ￥' + str(c.convert('JPY', 'CNY', float(re.search(r'(?<=/jpy )(.*)|(?<=#jpy )(.*)', command).group()))) + '*'), parse_mode="Markdown") #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'jpy command Error:\n' + str(e))
        #
        # 13. Calculator
        # Usage: input "/cal equation or equation directly"
        #
        # elif re.match(r'(/cal.*)|(#cal.*)|(^[0-9].*)|([\(].*)',command):
        elif re.match(r'^[0-9].*',command):
            try:
                # telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "import math\nprint(' + re.search(r'(?<=/cal )(.*)|(?<=#cal )(.*)|(^[0-9].*)|([\(].*)$', command).group() + ')"') + '*'), parse_mode="Markdown") #Return the output
                telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "import math\nprint(' + re.search(r'(^[0-9].*)|([\(].*)', command).group() + ')"') + '*'), parse_mode="Markdown") #Return the output
            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'number command Error:\n' + str(e))

        elif re.match(r'[\(].*',command):
            try:
                # telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "import math\nprint(' + re.search(r'(?<=/cal )(.*)|(?<=#cal )(.*)|(^[0-9].*)|([\(].*)$', command).group() + ')"') + '*'), parse_mode="Markdown") #Return the output
                telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "import math\nprint(' + re.search(r'(^[0-9].*)|([\(].*)', command).group() + ')"') + '*'), parse_mode="Markdown") #Return the output
            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'cal command Error:\n' + str(e))

        #
        # 14. Send Python Command to subprocess, in Non-Python Mode
        # Usage: input "/py or #py command input"
        #
        elif re.match(r'/py .*|#py .*',command):
            try:
                # telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr('python -c "import math\nprint(' + re.search(r'(?<=/cal )(.*)|(?<=#cal )(.*)|(^[0-9].*)|([\(].*)$', command).group() + ')"') + '*'), parse_mode="Markdown") #Return the output
                realCommand = str(re.search(r'(?<=/py )(.*)|(?<=#py )(.*)', command).group())
                pythonMode.sendline(realCommand)
                pythonMode.expect('>>>')
                telegram_bot.sendMessage(chat_id, str(str(pythonMode.before[len(realCommand)+3:]) )) #Return the output

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'cal command Error:\n' + str(e))
        #
        # 14. Duck duck go search
        # Usage: input "/search keyword"
        #
        elif re.match('/search .*|#search .*',command):
            try:
                output = ''
                ddgrDicList = json.loads(get_exitcode_stdout_stderr('ddgr ' + re.search(r'(?<=/search )(.*)|(?<=#search )(.*)', command).group() + ' --json -x '))
                logging.debug(ddgrDicList)
                for num, ddgrDic in enumerate(ddgrDicList, start=1):
                    # telegram_bot.sendMessage(chat_id, str(num) + '. ' + '[' + ddgrDic["title"] +  '](' + ddgrDic["url"] + ')' + '\n', parse_mode="Markdown")
                    output = output + str(num) + '. ' + '[' + ddgrDic["title"] +  '](' + ddgrDic["url"] + ')' + '\n' + ddgrDic["abstract"] + '\n\n'
                telegram_bot.sendMessage(chat_id, output, parse_mode="Markdown", disable_web_page_preview=True)

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'search command Error:\n' + str(e))

        #
        # 15. Duck duck go search and preview
        # Usage: input "/search keyword"
        #
        elif re.match('/preview .*|#preview .*',command):
            try:
                output = ''
                ddgrDicList = json.loads(get_exitcode_stdout_stderr('ddgr ' + re.search(r'(?<=/preview )(.*)|(?<=#preview )(.*)', command).group() + ' --json -x '))
                # logging.debug(ddgrDicList)
                for num, ddgrDic in enumerate(ddgrDicList, start=1):
                    telegram_bot.sendMessage(chat_id, str(num) + '. ' + '[' + ddgrDic["title"] +  '](' + ddgrDic["url"] + ')' + '\n', parse_mode="Markdown")
                #     output = output + str(num) + '. ' + '[' + ddgrDic["title"] +  '](' + ddgrDic["url"] + ')' + '\n' + '_' + ddgrDic["abstract"] + '_\n\n'
                # telegram_bot.sendMessage(chat_id, output, parse_mode="Markdown", disable_web_page_preview=True)

            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'preview command Error:\n' + str(e))
        #
        # *. Normal command
        # Usage: send a message to Pibot, pibot will take it as a normal command and issue it. If you send it the python source codes, it will run it!
        #
        else:
            # Input the command
            try:
                # telegram_bot.sendMessage(chat_id, str('*' + get_exitcode_stdout_stderr(command) + '*'), parse_mode="Markdown")
                sendMessageAdvanced(chat_id, get_exitcode_stdout_stderr(command))
                # for i in range(0,len(s),4096):
                #      # print s[i:i+4]:
                #     telegram_bot.sendMessage(chat_id, str('*' + s[i:i+4096] + '*'), parse_mode="Markdown")
                # pass
            except Exception as e:
                telegram_bot.sendMessage(chat_id, 'Normal Command Error:\n' + str(e))




def on_callback_query(msg):
    global pythonMode, pythonModeEnable, shellModeEnable

    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    telegram_bot.answerCallbackQuery(query_id, text='Got it')

    # if query_data == 'Python':
    #     telegram_bot.sendMessage (from_id, str("python -c '\nprint(hex(  ))\n'"))
    #     telegram_bot.sendMessage (from_id, str("python -c '\nprint(int(0x  )\n)'"))
    # elif query_data == 'Weather':
    # if query_data == 'Weather':
    #     telegram_bot.sendPhoto(from_id, photo='http://wttr.in/Hongkong_qn2F_lang=zh.png')
        # telegram_bot.sendMessage(from_id, str(get_exitcode_stdout_stderr('curl http://wttr.in/Hongkong?qn2F&lang=zh')))
    # elif query_data == 'Godaddy':
    #     telegram_bot.sendDocument(from_id, document=open('/home/pi/godaddy.log'))
    # elif query_data == 'Audio':
    #     telegram_bot.sendAudio(from_id, audio=open('/home/pi/Desktop/Mittens.mp3'))
    if query_data == 'IP':
        try:
            telegram_bot.sendMessage(from_id, str(get_exitcode_stdout_stderr("curl -s 'https://api.ipify.org/?format=json'")))
        except Exception as e:
            telegram_bot.sendMessage(from_id, str(e))
    # elif query_data == 'Currency - HKD':
    #     telegram_bot.sendMessage(from_id, str(get_exitcode_stdout_stderr("curl https://api.ratesapi.io/api/latest?base=HKD&symbols=CNY,USD")))
    # elif query_data == 'Currency - CNY':
    #     telegram_bot.sendMessage(from_id, str(get_exitcode_stdout_stderr("curl https://api.ratesapi.io/api/latest?base=CNY&symbols=HKD,USD")))
    # elif query_data == 'Currency - USD':
    #     telegram_bot.sendMessage(from_id, str(get_exitcode_stdout_stderr("curl https://api.ratesapi.io/api/latest?base=USD&symbols=HKD,CNY")))
        # try:
        #     telegram_bot.sendMessage(from_id, str(get_exitcode_stdout_stderr("/home/pi/speedtest.sh")))
        # except Exception as e:
        #     telegram_bot.sendMessage(from_id, str(e))
    # elif query_data == 'News':
    #     sendMessageAdvanced(from_id, get_exitcode_stdout_stderr("curl getnews.tech/raspberry"))
    elif query_data == 'Calibre_New':
        try:
            telegram_bot.sendMessage(from_id, str(get_exitcode_stdout_stderr("calibredb list --library-path /media/pi/ShareDrive/Documents/Library --field title --limit 15 --sort-by id")))
        except Exception as e:
            telegram_bot.sendMessage(from_id, str(e))
    elif query_data == 'Python Mode':
        pythonModeEnable = not pythonModeEnable
        telegram_bot.sendMessage(from_id, str('Mode: ') + mode)
    elif query_data == 'Restart Python Terminal':
        try:
            pythonMode.kill(1)
            pythonMode = pexpect.spawnu('/usr/bin/python3')
            pythonMode.expect('>>>')
            telegram_bot.sendMessage(from_id, str("Restart Python Terminal"))
            telegram_bot.sendMessage(from_id, str('Python Mode: ') + str(pythonModeEnable))
        except Exception as e:
            telegram_bot.sendMessage(from_id, str(e))
    # elif query_data == 'File':
    #     telegram_bot.sendDocument(from_id, document=open(str(get_exitcode_stdout_stderr("ls *.webm"))))



#
# INLINE QUERY
#
def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        articles = [InlineQueryResultArticle(
                        id='abc',
                        title=query_string,
                        input_message_content=InputTextMessageContent(
                            message_text=query_string
                        )
                   )]

        return articles

    answerer.answer(msg, compute)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)







telegram_bot = telepot.Bot('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
# print(telegram_bot.getMe())
logging.info(telegram_bot.getMe())
telegram_bot.sendMessage(896631342, str('*Pi03 Started.*'), parse_mode="Markdown")
answerer = telepot.helper.Answerer(telegram_bot)

# MessageLoop(telegram_bot, action).run_as_thread()
MessageLoop(telegram_bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

# MessageLoop(telegram_bot, {'inline_query': on_inline_query, 'chosen_inline_result': on_chosen_inline_result}).run_as_thread()

while 1:
	time.sleep(10)
