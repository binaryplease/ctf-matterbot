from mmpy_bot.bot import Bot
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to
import os
import pprint
import re
import requests
from bs4 import BeautifulSoup

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

@listen_to('!cve([0-9-]*)', re.IGNORECASE)
def cve(message,id):

    link = 'http://cve.circl.lu/cve/CVE'+id
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")

    for item in soup.select("#cveInfo > tbody > tr:nth-child(2) > td.info"):
        message.send('```pre\n'+item.get_text()+'\n```')

if __name__ == "__main__":
    Bot().run()
