from mmpy_bot.bot import Bot
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to
import os
import pprint
import re

@listen_to('!bot help', re.IGNORECASE)
def help(message):
    message.reply('I don\'t know any commands yet :(')

@listen_to('!shell (.*)', re.IGNORECASE)
def revshell(message, lang):
    shells = os.listdir('./shells')
    if lang in shells:
        try:
            with open('./shells/'+lang) as f:
                message.send('Here is a reverse shell in `%s`' % lang)
                message.send('```' + lang + '\n' + f.read() + '```')
        except IOError:
            pass
    else:
        message.send("I don't know that language :(")
        message.send("Supported languages are:")
        message.send(', '.join(shells))


if __name__ == "__main__":
    Bot().run()
