import json

import discord
from virustotal_python import Virustotal, virustotal

print("starting up url tester unit")
try:
    with open("Config.json", "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    with open("Config.json", "w") as f:
        json.dump({'Discord_Bot_Token': 'YOURTOKEN', 'VirusTotalToken': 'YOURTOKEN',
                   'YourDiscordId': '0', 'Prefix': '&'}, f)
    raise Exception("Missing Config.json. I added it, please fill it out yourself! (Intended at first excecution)")

print("url tester loaded with key " + CONFIG['VirusTotalToken'])
vtotal = Virustotal(API_KEY=CONFIG['VirusTotalToken'], API_VERSION="v3")

def get_file_embed(file:discord.File, ctx):
    pass
