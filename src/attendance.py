"""
File attendance.py

includes all of the functionality for attendance taking.

:author Sam Kuzio
"""

from src import client, CHAN_ATTENDANCE
from src import diddlemail
from src.util import http_post

import datetime


# How we expect people to format their dates.
USER_DATE_FORMAT = "%m/%d"

# Full date format that we can use for database insertions - YYYY-MM-DD
DB_DATE_FORMAT = "%Y-%m-%d"

# Help text
FORMAT_HELP_TEXT = "This channel is used to get an absence/late arrival to practice excused and I couldn't " \
                   "understand your message. Type a message in the following format to be excused:\n\n" \
                   "[late/absent] [MM/DD or today/tonight] [First] [Last] <Optional Reason>\n\n" \
                   "Example messages:\n" \
                   "Late 2/4 Paul Rennick\n" \
                   "absent 10/11 Sam Kuzio\n" \
                   "absent today George Hopkins I'm going to prison\n" \
                   "Late tonight Marc Garside Van broke down"

# Parsing string constants.
ABSENT = "absent"
LATE = "late"
TODAY = "today"
TONIGHT = "tonight"

# Excuse status type names.
EXCUSED = "excused"
UNEXCUSED = "unexcused"


async def excuse(message):
    """
    Handles an excuse message. This method assumes that the given message was sent to CHAN_ATTENDANCE!
    :param message: The message to handle.
    :return:
    """
    if message.channel.name != CHAN_ATTENDANCE:
        print("Warning: trying to handle attendance message in non #attendance channel!")
        return

    (absence, date, first, last, reason) = parse_message(message.content)

    valid = absence is not None and date is not None and first is not None and last is not None
    if not valid:
        await client.send_message(message.channel, FORMAT_HELP_TEXT)
        return
    else:
        email_sent = send_excuse_email(first, last, absence, date, reason)
        data_posted = add_excuse_record(absence, date, first, last, reason)

        if not email_sent or not data_posted:
            await client.send_message(message.channel, "I understood your message, but something went wrong "
                                                       "while recording it. Tell someone to check my error log!")
        else:
            await client.send_message(message.channel, "Got it! " + first + " " + last + " will be excused on " + date +
                                      " with " + ("no reason given" if reason is None else "reason '" + reason + "'"))


def send_excuse_email(first, last, absence, date, reason):
    """
    Attempts to send the attendance excuse email.
    :param first: The first name
    :param last: The last name
    :param absence: Whether they are late/absent
    :param date: date string on which the person will be absent
    :param reason: A reason they may have given.
    :return: True iff sending of the email succeeded, false otherwise.
    """
    subject = first + " " + last + " " + ("late arrival" if absence == LATE else "absence") + " on " + date

    message = "Hello,\n\n" + first + " " + last + " will be " + absence + " on " + date + " because:\n" + \
              (reason if reason else "<no reason given>") + "\n\nSincerely,\nDiddlebot"

    return diddlemail.send_email_to_club(message, subject)


def add_excuse_record(absence_type, date, first, last, reason):
    """
    Adds a record to the database for an excuse.
    :param absence_type: The type of excuse - late/absent
    :param date: The date on which the excuse is for - formatted as MM/DD - year will be assumed to be the current year.
    :param first: The first name
    :param last: The last name
    :param reason: The reason, or None if no reason was given.
    :return: True iff the excuse record was created.
    """

    # Format some of the fields for easy db insertion later.
    name = first + " " + last
    date = datetime.datetime.strptime(date, USER_DATE_FORMAT)\
        .replace(year=datetime.date.today().year).strftime(DB_DATE_FORMAT)

    # POST it to the web service which manages the database.
    post_data = {"absence_type": absence_type, "name": name, "date": date, "reason": reason}
    res = http_post('/attendance/excuse', post_data)

    # Handle the post response, failing if something went wrong.
    if res.status_code == 200:
        return True
    else:
        print("attendance: unexpected status code " + res.status_code + " posting /api/attendance/excuse: " +
              res.content.decode("utf-8") + "\nData submitted = " + str(post_data))
        return False


def parse_message(text):
    """
    Parses the contents of an absence message.
    :param text: The text of a message
    :return: A tuple containing the type of absence, the date, the firstname, lastname and reason.
    """

    parts = text.split()

    absence = None
    date = None
    first = None
    last = None
    reason = None

    # try to parse the absence type
    if len(parts) >= 1:
        if parts[0].lower() == ABSENT:
            absence = ABSENT
        elif parts[0].lower() == LATE:
            absence = LATE

    # try to parse the date
    if len(parts) >= 2:
        # If they said today/tonight, turn that into MM/DD
        if parts[1].lower() == TODAY or parts[1].lower() == TONIGHT:
            date = datetime.date.today().strftime(USER_DATE_FORMAT)

        # Otherwise try to parse the time they gave as a MM/DD string.
        else:
            try:
                date = datetime.datetime.strptime(parts[1], USER_DATE_FORMAT)
            except ValueError:
                date = None

    # try to parse the names
    if len(parts) >= 4:
        first = parts[2]
        last = parts[3]

    # The reason is the remainder of the list
    if len(parts) >= 5:
        reason = str.join(' ', parts[4:])

    return absence, date, first, last, reason

