# ritdl-bot
ritdl-bot is a discord bot written in python for the RIT drumline. It reminds us about meetings and dishes out sass.

# How to work on this project
ritdl-bot requires the discord.py library, which is limited to python 3.5. It is strongly recommended that you use python 3.5.6 (that is all ritdl-bot has been tested with.) 

### Set up a development bot 
To test ritdl-bot independently of the drumline discord server, it is recommended that you create your own discord bot test server. Once you have a server, you will also want to create a new discord bot via the discord website - while testing, your code will drive this bot account instead of the production ritdl-bot account. Once your bot is created, you can add it to your private development server like any other bot. For a better guide on all of this stuff, see this page: https://discordpy.readthedocs.io/en/rewrite/discord.html

The reason for creating your own test bot is two-fold:

- We only want to have one active login for the production ritdl-bot
- To prevent anyone from stealing access to the ritdl-bot (hence why the auth token is not a string constant in one of the source files)

### Driving your bot with the ritdl-bot source
In order to drive your development bot with the ritdl-bot code, you'll need to configure your auth token. On the discord development portal, you can retrieve your bot's authorization token - paste that bad boy into a file named `auth` in the project's working directory (don't worry, this file is .gitignored)  which will automatically be read and used to log in when you first start the bot.

### Working on email features
Much like the bot's auth token, the password to the ritdl-bot gmail is kept a secret. To test/add email features, a file named `email` must exist in the working directory. This file should contain one line with the password to the test email account.

Presently, the email address is hardcorded as diddlebot9000 (at) gmail.com. You will need to change this constant to another email address you wish to use, for which the password is stored in the `email` file.

If you intend on setting up your own gmail address for test usage, make sure you change the security settings for that Google account to allow less secure 3rd party apps - this allows automated log-ins that don't require any kind of multi-factor authentication.

### Dependencies
When configuring your development environment, the following dependencies are needed and can be installed with pip:
- [discord.py](https://github.com/Rapptz/discord.py) - `pip install discord.py`
- [schedule](https://github.com/dbader/schedule) - `pip install schedule`
- [requests](https://github.com/kennethreitz/requests) - `pip install requests`
