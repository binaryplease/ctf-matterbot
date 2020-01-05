
from string import Template
import pypandoc
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to
import os
import pprint
import re
import requests
from bs4 import BeautifulSoup
import json

@listen_to('!gimme help', re.IGNORECASE)
def help(message):

    """
    The help function just sends a message with information about available
    commands. Add all new functionality here in the same way to the array.
    """

    commands  =[
            "`!gimme shell <language> [local IP] [port]` Give me a reverse-shell in <language>. Optionally specify [your IP] and [port]",
            "`!gimme <cve-id>` Give me info about CVE-<id>",
            "`!gimme tldr <tool>` Remind me how to use <tool>",
            "`!gimme tool <toolname>` Give me misuse of <toolname>"]

    r = "I know the following commands:\n"
    for item in commands:
        r += "\n- " + item
    message.send(r)

@listen_to('!gimme shell (.*)', re.IGNORECASE)
def revshell(message, params):

    """
    Replies with code for a reverse shell in the specified language, if available.
    New shells can be put in the ./shells folder, with the language defined by
    the filename.

    The function has three optional parameters 'local_ip' and 'port' to insert
    the correct parameters in the output.
    """

    params_arr = params.split()
    lang = params_arr[0]

    # Set the optional parameters if specified and use defaults otherwise
    params = dict(
            local_ip  = params_arr[1] if len(params_arr) > 1 else '127.0.0.1',
            port      = params_arr[2] if len(params_arr) > 2 else '50000')

    # We first create whitelist of valid filenames. While we could skip this
    # check, it makes the application vultnerable to inserting arbitrary file
    # names like ../../../etc/passwd as a language

    shells = os.listdir('./shells')
    if lang in shells:
        try:
            with open('./shells/'+lang) as f:
                message.send('Here is a reverse shell in `%s`' % lang)

                # Render template with parameters and reply with the output
                tmpl = Template(f.read())
                rendered = tmpl.substitute(params)
                message.send('```' + lang + '\n' + rendered + '```')
        except IOError:
            pass
    else:
        # If an error occured, inform about available shells
        message.send("I don't know that language :(")
        message.send("Supported languages are:")
        message.send(', '.join(shells))

@listen_to('!gimme cve([0-9-]*)', re.IGNORECASE)
def cve(message,id):

    """
    Replies with information about CVEs. The information is the 'summary' field
    from cve.circl.lu.
    """

    link = 'http://cve.circl.lu/cve/CVE'+id
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")

    for item in soup.select("#cveInfo > tbody > tr:nth-child(2) > td.info"):
        message.send('```pre\n'+item.get_text()+'\n```')


@listen_to('!gimme tool (.*)', re.IGNORECASE)
def tool(message,id):

    """
    Replies with exploitation possiblities of common tools. Data is fetched
    from gtfobins.
    """

    link = 'https://gtfobins.github.io/gtfobins/'+id
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")

    for div in soup.find_all("ul", {'class':'function-list'}):
        div.decompose()

    for div in soup.find_all("h1"):
        div.decompose()

    for div in soup.find_all("a", {'class':'permalink'}):
        div.decompose()

    output = pypandoc.convert_text(soup.body, 'gfm', format='html')
    message.send(output)

@listen_to('!gimme tldr (.*)', re.IGNORECASE)
def tldr(message,id):

    """
    Replies with a short reminder of the most common use cases for common
    tools. Data is fetched from the tldr pages.
    """

    link = 'https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/common/'+id+'.md'
    html = requests.get(link).text
    message.send(html)


@listen_to('!gimme info (.*)', re.IGNORECASE)
def info(message,text):

    """
    Replies with the best answer to the top matching question on stackoverflow.
    """

    # Get best matching question and the link to it
    link = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q={}&answers=1&site=stackoverflow".format(text)
    jsonData = json.loads(requests.get(link).text)
    question_id = (jsonData["items"][0]["question_id"])
    qlink = jsonData["items"][0]["link"]

    # Get best matching answer for that question_id
    link = "https://api.stackexchange.com/2.2/questions/{}/answers?order=desc&sort=votes&site=stackoverflow&filter=!-.7zMlMaA9N-".format(question_id)
    jsonData = json.loads(requests.get(link).text)
    output = jsonData["items"][0]["body_markdown"]

    message.send(qlink + "\n\n" +output)
