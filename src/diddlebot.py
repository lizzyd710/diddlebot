"""
File diddlebot.py

Main execution entry point for the diddlebot.
Contains all discord client event handlers.

:author Sam Kuzio - sam@skuz.io
"""


from src import client
import src.quip
import src.command
import src.reminders


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

    # First and foremost handle commands. We don't want quips, etc. to be sent
    # in response to a command.
    if message.content.lower().startswith('$db '):
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

    # Load the quips
    src.quip.load_quips()

    # Begin awaiting the reminders.
    await src.reminders.init()


# load the auth token from the auth file so the bot can log in
with open('../auth','r') as auth_file:
    DISCORD_BOT_TOKEN = auth_file.read().strip()

# Start the discord client
client.run(DISCORD_BOT_TOKEN)
