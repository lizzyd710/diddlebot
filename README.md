# diddlebot
Diddlebot is a discord bot written in python for the RIT drumline. It reminds us about meetings and dishes out sass.

Diddlebot is named for drummer slang for double strokes on a membrane. It is frequently joked that drummers add "diddle" to all their slang (e.g., paradiddle, flamadiddle, paradiddlediddle...) so we decided it belonged in the name of our discord bot.

# configuring your development environment
Diddlebot requires the discord.py library, which is limited to python 3.5. It is strongly recommended that you use python 3.5.6 (that is all diddlebot has been tested with.) 

Additionally, you will need to create a discord bot to test with, and you will probably want to make a private discord server for testing. Once your bot has been created, you will need its auth token (available on the discord page for your bot). Create a new file named 'auth' next to the src directory and paste the auth token in it. This will be read by the diddlebot script, and the script will log in as your bot. You are now ready to test.

The reason for creating your own test bot is two-fold:

- To prevent redundant sessions of the diddlebot (imagine trying to test against several different versions of diddlebot in the same channel)
- To prevent anyone from stealing access to the diddlebot (hence why the auth token is not a string constant in one of the source files)
