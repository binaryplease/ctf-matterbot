from mmpy_bot.bot import listen_to
import urllib.request, json
import urllib.parse

import re
from bs4 import BeautifulSoup
import requests


@listen_to("!gimme meme (.*)", re.IGNORECASE)
def meme(message, query):

    """
    Replies with a meme for given query
    """

    link = "https://api.gfycat.com/v1/me/gfycats/search?count=1&search_text=" + urllib.parse.quote_plus(query)

    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        message.send("![]({})".format(data['gfycats'][0]['max5mbGif']))
