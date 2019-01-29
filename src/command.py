"""
File command.py

A basic command parser for the diddlebot.
All commands are messages received in the following format:

$db [command] [optional args list]

:author Sam Kuzio
"""

import random
import datetime

from src import client, VERSION, util, reminders
from src.quip import add_quip


# Help text to display when issuing the response to the help command.
HELP_TEXT = "Hi, I'm diddlebot! I mostly annoy everyone here but sometimes have helpful reminders.\n"
HELP_TEXT += "To teach me something stupid, try $db addquip [something stupid]\n"
HELP_TEXT += "To help me do stupid things, look at my brain - https://github.com/samkuzio/diddlebot"


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

    strings =[
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
    add_quip(newquip)
    response = "Nice one! I'll remember that!"
    await client.send_message(message.channel, response)


async def cmd_cancel(message, args):
    """
    Cancels practice on a certain day. If practice wa already canceled on that day, it is uncancelled.
    :param message: The message used to issue the command
    :param args: Arguments issued. The only argument should be a date string formatted YYYY-MM-DD
    :return: None
    """

    cancel_help_text = "usage: $db cancel YYYY-MM-DD\n\nThis cancels practice on the given date. If practice is " \
                       "already canceled on that day, this reschedules practice for that day. Dates must be zero-" \
                       "padded if they're single digits."

    # Only eboard should be able to cancel practice
    if not util.is_member_eboard(message.author):
        return

    # Handle the help case
    if args is None or args[0].lower() == "help":
        await client.send_message(message.channel, cancel_help_text)

    # Otherwise attempt to cancel practice on that day.
    try:
        # We parse the date to ensure it's valid (and inform the user) but we really only want to pass the string.
        datetime.datetime.strptime(args[0], reminders.DATE_FORMAT)
        reminders.cancel_on_day(args[0])
        await client.send_message(message.channel, "Got it! Practice will be canceled on " + args[0])
    except ValueError:
        await client.send_message(message.channel, "Could not parse date - make sure the day and month are 2 digits "
                                                   "(e.g. 2019-01-01 for January First)")


