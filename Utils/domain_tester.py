import json

import discord
from virustotal_python import Virustotal, virustotal

print("starting up domain tester unit")
try:
    with open("Config.json", "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    with open("Config.json", "w") as f:
        json.dump({'Discord_Bot_Token': 'YOURTOKEN', 'VirusTotalToken': 'YOURTOKEN',
                   'YourDiscordId': '0', 'Prefix': '&'}, f)
    raise Exception("Missing Config.json. I added it, please fill it out yourself! (Intended at first excecution)")

print("domain tester unit loaded with key " + CONFIG['VirusTotalToken'])
vtotal = Virustotal(API_KEY=CONFIG['VirusTotalToken'], API_VERSION="v3")


def get_domain_embed(url: str, ctx):
    try:
        resp = vtotal.request(f"domains/{url}")
        embed = discord.Embed(title="VirusTotalBot Domain Check",
                              description="Information about " + url,
                              color=discord.Colour.red())
        embed.set_author(name=str(ctx.author))
        last_analysis_stats = ""
        for i in resp.data['attributes']['last_analysis_stats'].keys():
            last_analysis_stats = last_analysis_stats + "\n" + i + ": " + str(
                resp.data['attributes']['last_analysis_stats'][i])
        embed.add_field(name="Last Analysis stats", value=last_analysis_stats, inline=True)
        embed.add_field(name="reputation score", value=str(resp.data['attributes']["reputation"]), inline=True)
        votes = ""
        for i in resp.data['attributes']['total_votes'].keys():
            votes = votes + "\n" + i + ": " + str(resp.data['attributes']['total_votes'][i])
        embed.add_field(name="votes", value=votes, inline=True)
    except virustotal.VirustotalError:
        print("An Error occured trying to handle " + url)

        embed = discord.Embed(title="VirusTotalBot Url Check",
                              description="Information about " + url,
                              color=discord.Colour.red())
        embed.add_field(name="Results", value="Something went wrong, most commonly is that it is not an working domain")

    finally:
        return embed
