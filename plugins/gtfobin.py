import re

import requests
from mmpy_bot.bot import listen_to

import pypandoc
from bs4 import BeautifulSoup


@listen_to("!gimme tool (.*)", re.IGNORECASE)
def tool(message, id):

    """
    Replies with exploitation possiblities of common tools. Data is fetched
    from gtfobins.
    """

    link = "https://gtfobins.github.io/gtfobins/" + id
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")

    for div in soup.find_all("ul", {"class": "function-list"}):
        div.decompose()

    for div in soup.find_all("h1"):
        div.decompose()

    for div in soup.find_all("a", {"class": "permalink"}):
        div.decompose()

    output = pypandoc.convert_text(soup.body, "gfm", format="html")
    message.send(output)
