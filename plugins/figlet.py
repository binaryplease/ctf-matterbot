from mmpy_bot.bot import listen_to
import pyfiglet

import re
from bs4 import BeautifulSoup
import requests


@listen_to("!gimme figlet ([a-z]*) (.*)", re.IGNORECASE)
def figlet(message, fontname, id):

    """
    Replies with given text in ascii art.
    """
    try:
         f = pyfiglet.Figlet(font=fontname)
         message.send("```\n" + f.renderText(id) + "\n```")
    except pyfiglet.FontNotFound:
         message.send("font {} not found. See avaitible fonts at http://www.figlet.org/examples.html".format(fontname))

