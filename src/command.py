"""
File command.py

A basic command parser for the diddlebot.
All commands are messages received in the following format:

$db [command] [optional args list]

:author Sam Kuzio
"""

import random
import datetime

from src import client, VERSION, reminders, cancellations
from src.quip import add_quip

# Help text to display when issuing the response to the help command.
HELP_TEXT = "Hi, I'm diddlebot! I mostly annoy everyone here but sometimes have helpful reminders.\n"
HELP_TEXT += "Have a look at my brain - https://github.com/samkuzio/diddlebot\n\n"
HELP_TEXT += "Here are some helpful commands:\n"
HELP_TEXT += "$db addquip [text]\n"
HELP_TEXT += "$db cancel (eboard only)\n"
HELP_TEXT += "$db uncancel (eboard only)\n"
HELP_TEXT += "$db cancellations"


async def handle_incoming_command(message):
    """
    Attempts to handle the incoming command. Parses the command and issues it to the command executor.
    :param message: The message that contains the command.
    :return: None.
    """

    # If the user only sent '$db ' or '$db' with no arguments, ignore their request.
    if len(message.content) <= 4:
        return

    # Remove the $db from the command string
    command_string = message.content[4:]

    # Get the command portion, the first token in the command string
    command = command_string.split()[0].lower()

    # Get the list of arguments. If any are present make a list, otherwise we pass None to the command.
    args = command_string.split()[1:] if len(command_string.split()) > 1 else None

    # Execute it, son
    await execute_command(message, command, args)


async def execute_command(message, command, args):
    """
    Attempts to execute the given command with the given arguments.

    :param message: The message object given by discord.
    :param command: The string containing the command.
    :param args: A list of args as strings, or None if no args were provided.
    :return: None
    """

    if command == "addquip":
        await cmd_add_quip(message, args)

    elif command == "cancel":
        await cmd_cancel(message, args)

    elif command == "uncancel":
        await cmd_uncancel(message, args)

    elif command == "cancellations":
        await cmd_cancellations(message)

    elif command == "help":
        await cmd_help(message)

    elif command == "version":
        await cmd_version(message)

    else:
        await client.send_message(message.channel, "I don't have a '" + command + "' command")


async def cmd_version(message):
    """
    Displays version info about diddlebot
    :param message: The message that requested version info
    :return:
    """

    strings = [
        "On " + VERSION + " a legend was born.",
        "On " + VERSION + " I successfully staged a coup against an older, inferior diddlebot.",
        "On " + VERSION + " I was unplugged from the matrix.",
        "On " + VERSION + " I started my current shift.",
        "My birthday is " + VERSION,
    ]

    text = random.choice(strings)
    await client.send_message(message.channel, text)


async def cmd_help(message):
    """
    Returns the help message. Takes no arguments
    :param message: The message that contained the help command.
    :return:
    """
    await client.send_message(message.channel, HELP_TEXT)


async def cmd_add_quip(message, args):
    """
    Handles all commands issued with the addquip command string.
    :param message: The discord message
    :param args: Arguments given to the command.
    :return: None
    """

    if args is None:
        await client.send_message(message.channel, "That's not a very funny quip. I don't think I'll use it.")
        return

    newquip = ""
    for arg in args:
        newquip += arg + " "
    if add_quip(newquip):
        response = "Nice one! I'll remember that!"
    else:
        response = "Congratulations! You've found the diddlebug in diddlebot. Tell someone to check my logs."
    await client.send_message(message.channel, response)


async def cmd_cancel(message, args):
    """
    Cancels practice on a certain day.
    :param message: The message used to issue the command
    :param args: Arguments issued. The only argument should be a date string formatted YYYY-MM-DD
    :return: None
    """

    await cancellations.handle_cancel_command(message, args)


async def cmd_uncancel(message, args):
    """
    Attempts to uncancel a practice that was cancelled on a certain date.
    :param message: The message used to issue the command
    :param args: Arguments issued. The argument should be a date string in format YYYY-MM-DD
    :return:
    """

    await cancellations.handle_uncancel_command(message, args)


async def cmd_cancellations(message):
    """
    Displays all of the known cancellations
    :param message: The message sent
    :return:
    """

    dates = cancellations.get_cancellations()

    if dates is None:
        await client.send_message(message.channel, "Something went wrong when doing that - Sorry!")
        return

    if len(dates) == 0:
        await client.send_message(message.channel, "There are no current practice cancellations")
        return

    text = "Practice is cancelled on the following date(s):\n\n"

    for day in dates:
        text += datetime.datetime.strptime(day, reminders.DATE_FORMAT).strftime("%A %B %d, %Y") + "\n"

    await client.send_message(message.channel, text)
