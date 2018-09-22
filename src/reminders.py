"""
File reminders.py

Contains functionality for sending reminders about meetings and rehearsals.
Uses 3rd party module schedule to make scheduling super ez:
https://github.com/dbader/schedule

:author Sam Kuzio - sam@skuz.io
"""

import schedule
import asyncio

from src import util
from src import CHAN_EBOARD, CHAN_PLAYGROUND


async def init():
    """
    Initializes the reminders and reminders thread.
    Runs as a coroutine so that it can run on the same thread that all
    of the discord interactions occur on.
    :return:
    """

    # Create the set of reminders before monitoring them.
    init_reminders()

    await run_scheduler()


def init_reminders():
    """
    Initializes the reminders. When reminders should be added or removed, declare them here.
    :return: None
    """

    # Enable for spam
    # print("Registered test reminder. Spam incoming!")
    # schedule.every(5).seconds.do(reminder_test)

    print("Registered sports federation weekly reminder for every tuesday")
    schedule.every().tuesday.at("12:00").do(reminder_sports_fed_meeting)


async def run_scheduler():
    """
    Runs the scheduler task as a coroutine on the main thread.
    :return:
    """

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def reminder_test():
    """
    A test reminder.
    :return:
    """
    cid = util.get_first_channel_by_name(CHAN_PLAYGROUND)
    text = "Automated reminders test"
    util.send_message_async(cid, text)


def reminder_sports_fed_meeting():
    """
    Reminder for weekly sports federation meetings.
    :return:
    """
    # Sports fed meeting should only go to eboard.
    cid = util.get_first_channel_by_name(CHAN_EBOARD)

    # Reminder text
    text = "REMINDER @eboard: The Sports Federation Meeting is scheduled for tomorrow at 11:00am."

    util.send_message_async(cid, text)
