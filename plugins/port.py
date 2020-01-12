import re

from mmpy_bot.bot import listen_to


@listen_to("!gimme port ([0-9]*)", re.IGNORECASE)
def cve(message, id):

    """
    Replies with the common service for a port.
    """

    with open("./plugins/ports.csv", "r") as fp:
        for line in generate_lines_that_equal(id, fp):
            message.send("Port {} is: `{}`".format(id, line))
            break


def generate_lines_that_equal(port, fp):
    for line in fp:
        if line.startswith(port + ","):
            yield line.split(",")[1]
