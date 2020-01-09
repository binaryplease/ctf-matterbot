from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import re

@listen_to('!gimme help', re.IGNORECASE)
def display_help(message):

    """
    The help function just sends a message with information about available
    commands. Add all new functionality here in the same way to the array.
    """

    commands  =[
            "`!gimme shell <language> [local IP] [port]` Give me a reverse-shell in <language>. Optionally specify [your IP] and [port]",
            "`!gimme <cve-id>` Give me info about CVE-<id>",
            "`!gimme tldr <tool>` Remind me how to use <tool>",
            "`!gimme tool <tool>` Give me misuse of <tool>",
            "`!gimme port <number>` Give me the service for <port>"]

    r = "I know the following commands:\n"
    for item in commands:
        r += "\n- " + item

    r += "\n\nYou can also directly ask me questions with `@mattapottata` and I will try my best to answer them!"
    message.send(r)
