"""
File util.py

Contains helpful utility methods for the diddblebot.

:author Sam Kuzio - sam@skuz.io
"""

import asyncio

from src import client


def get_first_channel_by_name(name):
    """
    Gets the id of the channel with the given name. Will search all the channels the bot can see, but just
    because the bot can see a channel does NOT mean the bot can message that channel.
    NOTE: If the bot has access to multiple channels with the given name, returns the id of the first.
    :param name: The name of the channel to find.
    :return: The ID of the first channel with the given name, or None if there's no access to the given channel.
    """

    for chan in client.get_all_channels():
        if chan.name == name:
            return chan

    return None


def send_message_async(channel, text):
    """
    A convenience method for sending messages from synchronous methods.
    :param channel: The Channel to send the message to
    :param text: The text of the message
    :return: None
    """

    asyncio.run_coroutine_threadsafe(client.send_message(channel, text), client.loop)

