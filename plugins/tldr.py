from mmpy_bot.bot import listen_to

import re
import requests


@listen_to("!gimme tldr (.*)", re.IGNORECASE)
def tldr(message, id):

    """
    Replies with a short reminder of the most common use cases for common
    tools. Data is fetched from the tldr pages.
    """

    link = (
        "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/common/"
        + id
        + ".md"
    )
    html = requests.get(link).text
    message.send(html)
