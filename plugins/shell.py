from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import re
import os
from string import Template

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
