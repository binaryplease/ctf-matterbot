from mmpy_bot.bot import listen_to

import re
from bs4 import BeautifulSoup
import requests


@listen_to("!gimme geoip (.*)", re.IGNORECASE)
def cve(message, ip):

    """
    Replies with geoip location data to a ip or domain
    """
    link = "http://ip-api.com/line/{}".format(ip)


    html = requests.get(link).text

    if html.startswith( 'success' ):
        message.send("```\n"+html+"\n```")

