"""
File quip.py

The quips module of the diddlebot.

:author Sam Kuzio - sam@skuz.io
"""

import random

from src import client

# The location of the quips file relative to the bot program on the production server.
QUIPS_FILE_PATH = 'quips.txt'

# A list that contains all of the loaded quips
quips = []


def load_quips():
    """
    Loads the quips from the the current QUIPS_FILE
    :return: None
    """

    global quips
    with open(QUIPS_FILE_PATH) as f:
        quips = f.readlines()
    quips = [quip.strip() for quip in quips]

    print("Loaded " + str(len(quips)) + " quips")


def add_quip(quip):
    """
    Adds a given quip string to the collection of quips and adds it to the quips file.
    :param quip:  The quip string to save.
    :return: None
    """

    global quips
    quips.append(quip)
    with open(QUIPS_FILE_PATH, 'w') as f:
        for item in quips:
            f.write("%s\n" % item)
    print("Saved new quip: " + quip)


async def send_quip(channel):
    """
    Sends a random quip to the given channel.
    :param channel:
    :return:
    """

    msg = random.choice(quips)
    await client.send_message(channel, msg)
