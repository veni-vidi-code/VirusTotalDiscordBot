print("""
*********************************************
Virus Total Bot by Tom Mucke
*********************************************


starting importing
""")

import json

import discord
from discord.ext import commands

from Cogs.DmCommands import DmCommands
from Cogs.DomainListener import DomainListener
from Cogs.EverywhereCommand import Everywhere
from Cogs.MsgChangeListener.Domainchangelistener import DomainListener as DomainChangeListener
from Cogs.MsgChangeListener.Filelistener import FileListener as FilechangeListener
from Cogs.MsgChangeListener.UrlListener import UrlListener as Urlchangelistener
from Cogs.MsgListener.Filelistener import FileListener
from Cogs.MsgListener.UrlListener import UrlListener
from Cogs.ServerCommands import ServerCommands

print("Loading up bot unit...")
try:
    with open("Config.json", "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    with open("Config.json", "w") as f:
        json.dump({'Discord_Bot_Token': 'YOURTOKEN', 'VirusTotalToken': 'YOURTOKEN',
                   'YourDiscordId': '0', 'Prefix': '&'}, f)
    raise Exception("Missing Config.json. I added it, please fill it out yourself! (Intended at first excecution)")

print("config loaded for bot unit!")
print("Initializing Bot with Token " + CONFIG['Discord_Bot_Token'] + " and Prefix " + str(CONFIG['Prefix']))
intents = discord.Intents.none()
intents.messages = True  # read and write messages. Change to intents.guild_messages to disable dm commands
intents.guilds = True  # This is needed to have the Guild Object to send messages
# This ensures the bot gets as minimal information and rights as possible to function
bot = discord.ext.commands.Bot(commands.when_mentioned_or(CONFIG['Prefix']),
                               case_insensitive=True,
                               intents=intents
                               )

# here i am just calling the Cogs. If you added some yourself call them here

if intents.dm_messages:
    bot.add_cog(DmCommands(bot))
for i in [ServerCommands(bot), Everywhere(bot), DomainListener(bot), UrlListener(bot), FileListener(bot),
          Urlchangelistener(bot), FilechangeListener(bot), DomainChangeListener(bot)]:
    bot.add_cog(i)

print("""Finished adding cogs. Bot starts now
*********************************************
Virus Total Bot by Tom Mucke
*********************************************
""")
bot.run(CONFIG['Discord_Bot_Token'])
