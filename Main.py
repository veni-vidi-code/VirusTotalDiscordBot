print("""
*********************************************
Virus Total Bot by The-Bow-Hunter
*********************************************


starting importing
""")

import json

import discord
from discord.ext import commands

from Cogs.DmCommands import DmCommands
from Cogs.EverywhereCommand import Everywhere
from Cogs.ServerCommands import ServerCommands
from Cogs.Urllistener import URLListener

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
bot = discord.ext.commands.Bot(commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)

# here i am just calling the Cogs. If you added some yourself call them here
bot.add_cog(ServerCommands(bot))
bot.add_cog(Everywhere(bot))
bot.add_cog(DmCommands(bot))
bot.add_cog(URLListener(bot))

print("""Finished adding cogs. Bot starts now
*********************************************
Virus Total Bot by The-Bow-Hunter
*********************************************
""")
bot.run(CONFIG['Discord_Bot_Token'])
