"""
File cancellations.py

Contains methods for handling practice cancellations.

:author Sam Kuzio
"""

import datetime
from src import client, reminders, CHAN_ANNOUNCEMENTS, util

# Help text for the cancellation commands.
CANCEL_HELP_TEXT = "usage: $db cancel YYYY-MM-DD\n\nThis cancels practice on the given date. Dates must be zero-" \
                       "padded if they're single digits."
UNCANCEL_HELP_TEXT = "usage: $db cancel YYYY-MM-DD\n\nThis uncancels practice on the given date. If practice is " \
                         "already canceled on that day, this reschedules practice for that day. Dates must be zero-" \
                         "padded if they're single digits."


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

    # Otherwise attempt to cancel practice on that day.
    try:
        # We parse the date to ensure it's valid (and inform the user) but we really only want to pass the string.
        dt = datetime.datetime.strptime(args[0], reminders.DATE_FORMAT)
    except ValueError:
        await client.send_message(message.channel, "Could not parse date - make sure the day and month are 2 digits "
                                             "(e.g. 2019-01-02 for January 2nd)")
        return

    # Check if already cancelled.
    if reminders.is_cancelled_on(args[0]):
        await client.send_message(message.channel, "Practice is already cancelled on " + args[0] + ". " +
                            "Use $db uncancel YYYY-MM-DD if you wish to reschedule practice.")
    else:
        reminders.cancel_on_day(args[0])
        await client.send_message(message.channel, "Practice has been cancelled on " + dt.strftime("%B %d, %Y") + ".")
        await client.send_message(util.get_first_channel_by_name(CHAN_ANNOUNCEMENTS),
                            "Notice: Practice has been cancelled on " +
                            dt.strftime("%A %B %d, %Y"))


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
    try:
        # We parse the date to ensure it's valid (and inform the user) but we really only want to pass the string.
        dt = datetime.datetime.strptime(args[0], reminders.DATE_FORMAT)
    except ValueError:
        await client.send_message(message.channel, "Could not parse date - make sure the day and month are 2 digits "
                                                   "(e.g. 2019-01-02 for January 2nd)")
        return

    # If already cancelled, do uncancelling.
    if reminders.is_cancelled_on(args[0]):
        reminders.uncancel_on_date(args[0])
        await client.send_message(message.channel, "Practice has been uncancelled on " + dt.strftime("%B %d, %Y") + ".")
        await client.send_message(util.get_first_channel_by_name(CHAN_ANNOUNCEMENTS),
                                  "Notice: Practice, which was previously cancelled on "
                                  + dt.strftime("%A %B %d, %Y") + " has been rescheduled for the same time - "
                                                                  "sorry for any inconvenience.")
    else:
        await client.send_message(message.channel, "Practice was not cancelled on " + args[0] +
                                  " so it can't be uncancelled.")