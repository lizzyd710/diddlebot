"""
File util.py

Contains helpful utility methods for the diddblebot.

:author Sam Kuzio - sam@skuz.io
"""

import asyncio
import discord
from datetime import date
import time
import requests

from src import client, ROLE_EBOARD


# The start date of the semester. Useful for calculating whether it's an even or odd week.
# Note: updated this date to account for spring break, which is not counted as a week of the spring semester.
SEMESTER_START_DATE = date(2019, 3, 18)

# The base url of the ritdl-ws rest api.
API_BASE_URL = "http://localhost:3000/api"


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


def is_member_eboard(member):
    """
    Determines if the given member is on eboard.
    :param member: a Member object.
    :return: True if they're on eboard, false if not.
    """

    if type(member) is not discord.Member:
        print("Given object is not a server member - make sure they're sending the message from a server and not DMs.")
        return False

    for role in member.roles:
        if role.name == ROLE_EBOARD:
            return True

    return False


def http_get(endpoint):
    """
    Given an ritdl-ws enpoint, makes an HTTP GET request.
    :param endpoint: An endpoint string formatted as "/[endpoint][vars]" that will be appended to the
                     API_BASE_ENDPOINT string.
    :return: A Response object: http://docs.python-requests.org/en/latest/api/#requests.Response
    """

    url = API_BASE_URL + endpoint
    return requests.get(url)


def http_put(endpoint, data):
    """
    Makes an HTTP PUT request.
    :param endpoint: The api endpoint.
    :param data: A dictionary of key value pairs to put in the request.
    :return: A response object.
    """

    url = API_BASE_URL + endpoint
    return requests.put(url, data=data)


def http_post(endpoint, data):
    """
    Makes an HTTP POST request.
    :param endpoint: The api endpoint
    :param data: A dictionary that represents the body of the request.
    :return: A response object.
    """

    url = API_BASE_URL + endpoint
    return requests.post(url, data=data)
