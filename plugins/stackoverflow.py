from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import re
import json
import requests

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

