"""
File quip.py

The quips module of the diddlebot.

:author Sam Kuzio - sam@skuz.io
"""

from src import client
from src.db import database


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

    conn = database.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT quip FROM quips ORDER BY RANDOM() LIMIT 1")
    rows = cursor.fetchone()
    msg = rows[0]

    await client.send_message(channel, msg)
