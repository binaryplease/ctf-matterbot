from mmpy_bot.bot import listen_to

import re
from bs4 import BeautifulSoup
import requests


@listen_to("!gimme cve([0-9-]*)", re.IGNORECASE)
def cve(message, id):

    """
    Replies with information about CVEs. The information is the 'summary' field
    from cve.circl.lu.
    """

    link = "http://cve.circl.lu/cve/CVE" + id
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")

    for item in soup.select("#cveInfo > tbody > tr:nth-child(2) > td.info"):
        message.send("```pre\n" + item.get_text() + "\n```")
