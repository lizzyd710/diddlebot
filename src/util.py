"""
File util.py

Contains helpful utility methods for the diddblebot.

:author Sam Kuzio - sam@skuz.io
"""

import asyncio
from datetime import date
import time

from src import client


# The start date of the semester. Useful for calculating whether it's an even or odd week.
SEMESTER_START_DATE = date(2018, 8, 27)


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


def delta_weeks(date1, date2):
    """
    A convenience method that calculates how many weeks are between the two dates.
    Assumes date2 comes after date1.
    :param date1: The starting date
    :param date2: The ending date
    :return: The amount of weeks between the two dates.
    """

    return (date2 - date1).days/7


def get_week_number():
    """
    Determines what week of the semester it is.
    :return: The week number of the semester
    """

    stringtime = time.strftime("%Y,%m,%d")
    datearray = stringtime.split(",")

    year = int(datearray[0])
    month = int(datearray[1])
    day = int(datearray[2])

    current_date = date(year, month, day)

    return (delta_weeks(SEMESTER_START_DATE, current_date) // 1) + 1

