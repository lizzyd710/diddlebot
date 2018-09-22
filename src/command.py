"""
File command.py

A basic command parser for the diddlebot.
All commands are messages received in the following format:

$db [command] [optional args list]

:author Sam Kuzio
"""

from src import client
from src.quip import add_quip


# Help text to display when issuing the response to the help command.
HELP_TEXT = "Hi, I'm diddlebot! I mostly annoy everyone here but sometimes have helpful reminders.\n"
HELP_TEXT += "To teach me something stupid, try $db addquip [something stupid]"


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
    command = command_string.split()[0]

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

    elif command == "help":
        await cmd_help(message)

    else:
        await client.send_message(message.channel, "I don't have a '" + command + "' command")


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
