"""
File diddlebot.py

Main execution entry point for the diddlebot.
Contains all discord client event handlers.

:author Sam Kuzio - sam@skuz.io
"""


from src import client, CHAN_ATTENDANCE
import src.quip
import src.command
import src.reminders
import src.attendance
import src.diddlemail


@client.event
async def on_message(message):
    """
    Called when the bot receives a message in any channel.
    :param message: A message object describing the message.
    :return: None.
    """

    # ensure the bot does not reply to itself
    if message.author == client.user:
        return

    # Before handling commands, we handle channels where users solely interact with
    # diddlebot, like #attendance. We don't need commands here bc it's assumed every
    # message will be an attendance excuse.
    if message.channel.name == CHAN_ATTENDANCE:
        await src.attendance.excuse(message)
    # First and foremost handle commands. We don't want quips, etc. to be sent
    # in response to a command.
    elif message.content.lower().startswith('$db '):
        await src.command.handle_incoming_command(message)

    # When the diddlebot is mentioned it should chime in with sass or humor or whatever
    elif "diddlebot" in message.content.lower():
        await src.quip.send_quip(message.channel)

    # Press f to pay respects
    elif message.content.lower() == 'f':
        await client.send_message(message.channel, 'f')


@client.event
async def on_ready():
    """
    Called when the bot has logged in and is ready to interact with chats.
    :return: None
    """

    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print('-------------')

    # Begin awaiting the reminders.
    await src.reminders.init()


def start():
    """
    Starts diddlebot!
    :return: The auth token.
    """

    # load the auth token from the auth file so the bot can log in
    with open('auth','r') as auth_file:
        bot_token = auth_file.read().strip()

    # load the email credentials
    src.diddlemail.load_creds()

    # Load the quips
    src.quip.load_quips()

    print("\nLogging in...")

    # Start the discord client
    client.run(bot_token)
