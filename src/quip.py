"""
File quip.py

The quips module of the diddlebot.

:author Sam Kuzio - sam@skuz.io
"""

from src import client
from src.util import http_get, http_put


def add_quip(quip):
    """
    Adds a given quip string to the collection of quips and adds it to the quips file.
    :param quip:  The quip string to save.
    :return: True if the quip is added, or already exists. False if an error occurs.
    """

    resp = http_put("/quip", {"quip": quip})
    if resp.status_code != 200:
        print("Unexpected error code " + str(resp.status_code) + " and response body " + resp.content.decode("utf-8"))
        return False
    else:
        return True


async def send_quip(channel):
    """
    Sends a random quip to the given channel.
    :param channel: The channel to send a quip to.
    :return:None
    """

    resp = http_get("/quip")

    if resp.status_code == 200:
        quip = resp.content.decode("utf-8")
        await client.send_message(channel, quip)
    else:
        print("quip: Unexpected response code " + resp.status_code + " with message " + resp.content.decode("utf-8"))
