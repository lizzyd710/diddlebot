"""
File quip.py

The quips module of the diddlebot.

:author Sam Kuzio - sam@skuz.io
"""

from src import client
from src.db import database
from src.util import http_get


def add_quip(quip):
    """
    Adds a given quip string to the collection of quips and adds it to the quips file.
    :param quip:  The quip string to save.
    :return: None
    """

    conn = database.get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quips (quip) VALUES (?)", (quip,))
    conn.commit()


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
        print("quip: Unexpected response code " + resp.status_code + " with message " + str(resp.content))
