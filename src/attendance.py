"""
File attendance.py

includes all of the functionality for attendance taking.

:author Sam Kuzio
"""

from src import client, CHAN_ATTENDANCE
import datetime
import src.diddlemail

# Help text
FORMAT_HELP_TEXT = "This channel is used to get an absence/late arrival to practice excused and I couldn't " \
                   "understand your message. Type a message in the following format to be excused:\n\n" \
                   "[late/absent] [MM/DD or today/tonight] [First] [Last] <Optional Reason>\n\n" \
                   "Example messages:\n" \
                   "Late 2/4 Paul Rennick\n" \
                   "absent 10/11 Sam Kuzio\n" \
                   "absent today George Hopkins I'm going to prison\n" \
                   "Late tonight Marc Garside Van broke down"

ABSENT = "absent"
LATE = "late"
TODAY = "today"
TONIGHT = "tonight"


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
        await client.send_message(message.channel, "Got it! " + first + " " + last + " will be excused on " + date +
                                  " with " + ("no reason given" if reason is None else "reason '" + reason + "'"))

        subject = first + " " + last + " " + ("late arrival" if absence == LATE else "absence") + " on " + date

        message = "Hello,\n\n" + first + " " + last + " will be " + absence + " on " + date + " because:\n" +\
                  (reason if reason else "<no reason given>") + "\n\nSincerely,\nDiddlebot"

        src.diddlemail.send_email_to_club(message, subject)


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
        if parts[1].lower() == TODAY or parts[1].lower() == TONIGHT:
            date = datetime.date.today().strftime("%B %d")
        else:
            date = parts[1]

    # try to parse the names
    if len(parts) >= 4:
        first = parts[2]
        last = parts[3]

    # The reason is the remainder of the list
    if len(parts) >= 5:
        reason = str.join(' ', parts[4:])

    return absence, date, first, last, reason

