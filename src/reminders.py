"""
File reminders.py

Contains functionality for sending reminders about meetings and rehearsals.
Uses 3rd party module schedule to make scheduling super ez:
https://github.com/dbader/schedule

:author Sam Kuzio - sam@skuz.io
"""

import schedule
import asyncio
import datetime

from src import util
from src import CHAN_EBOARD, CHAN_PLAYGROUND, CHAN_ANNOUNCEMENTS


# A list of days on which practice has been cancelled. Stored as strings in DATE_FORMAT
CANCELLATION_DATES = []

# The file that contains the cancellation dates.
CANCELLATION_DATES_FILE = "cancellations.txt"

# Format that we use to store cancellation dates.
DATE_FORMAT = "%Y-%m-%d"


async def init():
    """
    Initializes the reminders and reminders thread.
    Runs as a coroutine so that it can run on the same thread that all
    of the discord interactions occur on.
    :return:
    """

    # Read the list of cancellations
    read_cancellation_file()

    # Create the set of reminders before monitoring them.
    init_reminders()

    await run_scheduler()


def init_reminders():
    """
    Initializes the reminders. When reminders should be added or removed, declare them here.
    :return: None
    """

    # Enable for spam
    # schedule.every(5).seconds.do(reminder_test)
    # print("Registered test reminder. Spam incoming!")

    schedule.every().tuesday.at("12:00").do(reminder_sports_fed_meeting)
    print("Registered sports federation weekly reminder for every tuesday")

    schedule.every().tuesday.at("12:00").do(reminder_practice_every_other_tuesday)
    schedule.every().thursday.at("12:00").do(reminder_practice)
    schedule.every().friday.at("17:00").do(reminder_saturday_practice)
    print("Registered practice reminders")


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


def reminder_practice_every_other_tuesday():
    """
    Remind about practice on odd weeks of the semester.
    This function exists because while the scheduler can schedule events every other tuesday,
    it does not know what week of the semester we are currently in.
    :return:
    """

    # Only remind us about this stuff on odd weeks.
    if util.get_week_number() % 2 == 1:
        reminder_practice()


def reminder_practice():
    """
    Reminder for practices.
    :return:
    """

    # Practice reminders go in the announcements channel
    cid = util.get_first_channel_by_name(CHAN_ANNOUNCEMENTS)

    if not is_cancelled_today():
        text = "⚠️Reminder: Practice tonight at 9:00! Be there or be ⬛"
    else:
        text = "Reminder: NO PRACTICE TODAY! Enjoy your day off!"

    util.send_message_async(cid, text)


def reminder_saturday_practice():
    """
    Reminder for saturday practices
    :return:
    """

    cid = util.get_first_channel_by_name(CHAN_ANNOUNCEMENTS)

    if not is_cancelled_today():
        text = "⚠️Reminder: Practice tomorrow morning at 10am! Set your alarm now!⏰"
    else:
        text = "Reminder: NO PRACTICE TOMORROW! Turn off that alarm and sleep in!"

    util.send_message_async(cid, text)


def is_cancelled_today():
    """
    Determines if practice is cancelled today.
    :return: True if today is in the CANCELLATION_DATES list, false if not
    """

    date = datetime.datetime.today().strftime(DATE_FORMAT)
    return date in CANCELLATION_DATES


def cancel_on_day(date):
    """
    Cancels the practice on the given date.
    :param date: A string formatted as DATE_FORMAT
    :return:
    """

    # can't do anything with none date.
    if date is None:
        print("Warning: tried to cancel practice on None date!")
        return

    if date not in CANCELLATION_DATES:
        CANCELLATION_DATES.append(date)
        write_cancellation_file()
    elif date in CANCELLATION_DATES:
        CANCELLATION_DATES.remove(date)
        write_cancellation_file()


def write_cancellation_file():
    """
    Saves the CANCELLATION_DATES to a file.
    Each line of the file will be a different date.
    :return:
    """

    file = open(CANCELLATION_DATES_FILE, "w")

    for date in CANCELLATION_DATES:
        file.write(date.strftime("%Y-%m-%d\n"))

    file.close()


def read_cancellation_file():
    """
    Reads all of the entries in the cancellation file and parses
    them into the CANCELLATION_DATES list. Clears the list of cancellations
    before reading.
    :return:
    """

    try:
        file = open(CANCELLATION_DATES_FILE, "r")
    except FileNotFoundError:
        file = open(CANCELLATION_DATES_FILE, "w")

    lines = file.readlines()
    file.close()

    CANCELLATION_DATES.clear()

    for line in lines:
        try:
            # Parse each date just to be sure it's valid.
            datetime.datetime.strptime(line.strip(), "%Y-%m-%d")
            CANCELLATION_DATES.append(line.strip())
        except ValueError:
            print("Failed to parse date '" + line.strip() + "' while reading cancellation file.")

