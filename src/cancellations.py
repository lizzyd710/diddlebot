"""
File cancellations.py

Contains methods for handling practice cancellations.

:author Sam Kuzio
"""

import datetime
import json

from src import client, CHAN_ANNOUNCEMENTS, util

# Help text for the cancellation commands.
CANCEL_HELP_TEXT = "usage: $db cancel YYYY-MM-DD\n\nThis cancels practice on the given date. Dates must be zero-" \
                       "padded if they're single digits."
UNCANCEL_HELP_TEXT = "usage: $db cancel YYYY-MM-DD\n\nThis uncancels practice on the given date. If practice is " \
                         "already canceled on that day, this reschedules practice for that day. Dates must be zero-" \
                         "padded if they're single digits."

# The format we expect dates in.
DATE_FORMAT = "%Y-%m-%d"


def parse_date(date):
    """
    Determines if the given string is a valid date in the DATE_FORMAT format.
    :param date: A string the verify.
    :return: A datetime object, or None if the date is invalid.
    """
    try:
        return datetime.datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        return None


def get_cancellations():
    """
    Gets a list of all of the cancellations.
    :return: A list of all the dates on which practice is cancelled. Dates in this list are Strings.
    """

    res = util.http_get('/cancellations')

    if res.status_code == 200:
        return json.loads(res.content.decode("utf-8"))
    else:
        print("Something went wrong when getting /api/cancellations: " +
              str(res.status_code) + "\n" + res.content.decode("utf-8"))
        return None


def cancel_on_day(date):
    """
    Cancels practice on the given date.
    :param date: A string in the format DATE_FORMAT.
    :return: True iff practice has been registered as cancelled.
    """

    res = util.http_post("/cancellations/cancel/" + date, {})
    if res.status_code == 200:
        return True
    else:
        print("Something went wrong when trying to cancel practice on '" + date + "' " +
              str(res.status_code) + ":\n" + res.content.decode("utf-8"))
        return False


def uncancel_on_date(date):
    """
    If practice is cancelled on the given date, this will uncancel it.
    :param date: The date to uncancel it. It is assumed this date is in DATE_FORMAT.
    :return: True iff the update operation was successful, false if not.
    """

    res = util.http_post("/cancellations/uncancel/" + date, {})
    if res.status_code == 200:
        return True
    else:
        print("Something went wrong when trying to uncancel practice on '" + date + "' " +
              str(res.status_code) + ":\n" + res.content.decode("utf-8"))
        return False


def is_cancelled_on(date):
    """
    Determines if practice is cancelled on the given date.
    :param date: A String in the format YYYY-MM-DD.
    :return: True if practice is cancelled on the given date, False if not.
    """

    res = util.http_get("/cancellations/is/cancelled/" + date)

    if res.status_code == 200:
        # The response will just be true or false.
        return json.loads(res.content.decode("utf-8"))
    else:
        print("Something went wrong when trying to determine if practice is cancelled " +
              "on " + date + ":\n" + res.content.decode("utf-8"))
        return None


def is_cancelled_today():
    """
    Determines if practice is cancelled today.
    :return: True if today is in the CANCELLATION_DATES list, false if not
    """

    date = datetime.datetime.today().strftime(DATE_FORMAT)
    return is_cancelled_on(date)


def is_cancelled_tomorrow():
    """
    Determines if practice is cancelled tomorrow.
    :return: True if tomorrow is in the cancellation_dates list, false if not
    """

    tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime(DATE_FORMAT)
    return is_cancelled_on(tomorrow)


async def handle_cancel_command(message, args):
    """
    Cancels practice on a certain day.
    :param message: The message used to issue the command
    :param args: Arguments issued. The only argument should be a date string formatted YYYY-MM-DD
    :return: None
    """

    # Only eboard should be able to cancel practice
    if not util.is_member_eboard(message.author):
        await client.send_message(message.channel, "You're not in eboard... trying to stage a coup?")
        return

    # Handle the help case
    if args is None or len(args) != 1 or args[0].lower() == "help":
        await client.send_message(message.channel, CANCEL_HELP_TEXT)
        return

    # Parse & verify the date is in a valid format
    dt = parse_date(args[0])
    if dt is None:
        await client.send_message(message.channel, "Could not parse date - make sure the day and month are 2 digits "
                                                   "(e.g. 2019-01-02 for January 2nd)")
        return

    # Check if already cancelled.
    if is_cancelled_on(args[0]):
        await client.send_message(message.channel, "Practice is already cancelled on " + args[0] + ". " +
                                  "Use $db uncancel YYYY-MM-DD if you wish to reschedule practice.")

    # If not cancelled, we try cancelling on the date
    elif cancel_on_day(args[0]):
        await client.send_message(message.channel, "Practice has been cancelled on " + dt.strftime("%B %d, %Y") + ".")
        await client.send_message(util.get_first_channel_by_name(CHAN_ANNOUNCEMENTS),
                                  "Notice: Practice has been cancelled on " +
                                  dt.strftime("%A %B %d, %Y"))

    # And if something went wrong with that, report a failure.
    else:
        await client.send_message(message.channel, "Something went wrong! Practice has not been cancelled...")


async def handle_uncancel_command(message, args):
    """
    Attempts to uncancel a practice that was cancelled on a certain date.
    :param message: The message used to issue the command
    :param args: Arguments issued. The argument should be a date string in format YYYY-MM-DD
    :return:
    """

    # Only eboard should be able to cancel practice
    if not util.is_member_eboard(message.author):
        await client.send_message(message.channel, "You're not in eboard... trying to stage a coup?")
        return

    # Handle the help case
    if args is None or len(args) != 1 or args[0].lower() == "help":
        await client.send_message(message.channel, UNCANCEL_HELP_TEXT)
        return

    # Otherwise attempt to cancel practice on that day.
    dt = parse_date(args[0])
    if dt is None:
        await client.send_message(message.channel, "Could not parse date - make sure the day and month are 2 digits "
                                                   "(e.g. 2019-01-02 for January 2nd)")
        return

    # If already cancelled, do uncancelling.
    if is_cancelled_on(args[0]):
        if uncancel_on_date(args[0]):
            await client.send_message(message.channel, "Practice has been uncancelled on " + dt.strftime("%B %d, %Y"))
            await client.send_message(util.get_first_channel_by_name(CHAN_ANNOUNCEMENTS),
                                      "Notice: Practice, which was previously cancelled on "
                                      + dt.strftime("%A %B %d, %Y") + " has been rescheduled for the same time - "
                                                                      "sorry for any inconvenience.")
        else:
            await client.send_message(message.channel, "Failed to uncancel practice on " + args[0] +
                                      " - something went wrong.")
    else:
        await client.send_message(message.channel, "Practice was not cancelled on " + args[0] +
                                  " so it can't be uncancelled.")
