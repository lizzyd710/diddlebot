import discord
import random

from discord import Client

QUIPS_FILE = 'quips.txt'
TOKEN = 'NDkxNzcyNjU5NTEyNjM5NTEw.DoMwmw.ctS2ARtRhQlDSmTzyc7QMyEKqmU'
client = discord.Client()  # type: Client

# A list of quips from the quips file
quips = []

HELP_TEXT = "Hi, I'm diddlebot! I mostly annoy everyone here but sometimes have helpful reminders.\n"
HELP_TEXT += "To teach me something stupid, try $db addquip [something stupid]"


# Loads the quips from the file
def loadQuips():
    global quips
    with open(QUIPS_FILE) as f:
        quips = f.readlines()
    quips = [quip.strip() for quip in quips]
    for quip in quips:
        print('read ' + quip)


# Adds the given quip to the list of quips
def addQuip(quip):
    global quips
    quips.append(quip)
    with open(QUIPS_FILE, 'w') as f:
        for item in quips:
            f.write("%s\n" % item)
    print("Saved new quip: " + quip)


# Parses a command with the given args
async def parseCommand(message, command, args):
    global quips

    if command == "addquip" and args is not None:
        newquip = ""
        for arg in args:
            newquip += arg + " "
        addQuip(newquip)
        response = "Nice one! I'll remember that!"
        await client.send_message(message.channel, response)


# Executed when processing a message.
@client.event
async def on_message(message):

    global quips
    global HELP_TEXT

    # ensure the bot does not reply to itself
    if message.author == client.user:
        return

    if message.content.lower().startswith('$db '):
        if len(message.content) > 4:
            commandStr = message.content[4:]
            command = commandStr.split(" ")[0]
            args = commandStr.split(" ")[1:] if len(commandStr.split(" ")) > 1 else None
            await parseCommand(message, command, args)

    elif message.content.lower().startswith("diddlebot help"):
        await client.send_message(message.channel, HELP_TEXT)

    elif "diddlebot" in message.content.lower():
        msg = random.choice(quips)
        await client.send_message(message.channel, msg)

    elif message.content.lower() == 'f':
        await client.send_message(message.channel, 'f')


# Executed when th bot logs in
@client.event
async def on_ready():
    
    global quips
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    loadQuips()
    for quip in quips:
        print("quip: " + quip)

client.run(TOKEN)
