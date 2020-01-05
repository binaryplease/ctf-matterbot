from mmpy_bot.bot import Bot
import pypandoc
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to
import os
import pprint
import re
import requests
from bs4 import BeautifulSoup

@listen_to('!gimme help', re.IGNORECASE)
def help(message):
    commands  =[
            "`!gimme shell <language>` Give me a reverse-shell in <language>",
            "`!gimme <cve-id>` Give me info about CVE-<id>",
            "`!gimme tldr <tool>` Remind me how to use <tool>",
            "`!gimme tool <toolname>` Give me misuse of <toolname>"]

    r = "I know the following commands:\n"
    for item in commands:
        r += "\n- " + item
    message.send(r)

@listen_to('!gimme shell (.*)', re.IGNORECASE)
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

@listen_to('!gimme cve([0-9-]*)', re.IGNORECASE)
def cve(message,id):

    link = 'http://cve.circl.lu/cve/CVE'+id
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")

    for item in soup.select("#cveInfo > tbody > tr:nth-child(2) > td.info"):
        message.send('```pre\n'+item.get_text()+'\n```')


@listen_to('!gimme tool (.*)', re.IGNORECASE)
def tool(message,id):

    link = 'https://gtfobins.github.io/gtfobins/'+id
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")

    for div in soup.find_all("ul", {'class':'function-list'}):
        div.decompose()

    for div in soup.find_all("h1"):
        div.decompose()

    for div in soup.find_all("a", {'class':'permalink'}):
        div.decompose()

    for item in soup.select("body"):
        output = pypandoc.convert_text(soup.body, 'gfm', format='html')
        message.send(output)

@listen_to('!gimme tldr (.*)', re.IGNORECASE)
def tldr(message,id):

    link = 'https://gtfobins.github.io/gtfobins/'+id
    link = 'https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/common/'+id+'.md'
    html = requests.get(link).text
    message.send(html)

if __name__ == "__main__":
    Bot().run()

