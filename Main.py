import json
import re

import discord
from discord.ext import commands
from virustotal_python import Virustotal, virustotal

print("starting...")
try:
    with open("Config.json", "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    with open("Config.json", "w") as f:
        json.dump({'Discord_Bot_Token': 'YOURTOKEN', 'VirusTotalToken': 'YOURTOKEN',
                   'YourDiscordId': '0', 'Prefix': '&'}, f)
    raise Exception("Missing Config.json. I added it, please fill it out yourself! (Intended at first excecution)")

print("config loaded")
vtotal = Virustotal(API_KEY=CONFIG['VirusTotalToken'], API_VERSION="v3")

bot = discord.ext.commands.Bot(commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)


def get_url_embed(url: str, ctx):
    try:
        resp = vtotal.request(f"domains/{url}")
        embed = discord.Embed(title="VirusTotalBot Url Check",
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
        embed.add_field(name="Results", value="Something went wrong, most commonly is that it is not an working url")

    finally:
        return embed


class DmCommands(commands.Cog, name="Dm Commands"):
    def __init__(self, b):
        self.b = b

    @commands.command(name="check",
                      help="Takes given Input and runs a test over it. Only Dm Channels. Accepts URLs and Files",
                      brief="Checks Input", aliases=["test"])
    async def check(self, ctx, *arg):
        if ctx.guild is not None:
            try:
                await ctx.message.delete()
                await ctx.author.send("Only DM Available")
            except:
                await ctx.send("Only DM Available! Warning! The Above message might be milicious. "
                               "Dont click the file/url until you trust it! (for some reason i cant delete it)")
            return
        if arg is None:
            await ctx.send("Missing an url or file")
            return
        domain = arg[0]
        await ctx.send(embed=get_url_embed(domain, ctx))


class ServerCommands(commands.Cog, name="Server Commands"):
    def __init__(self, b):
        self.b = b

    @commands.command(name="Function on server",
                      help="This bot checks all links and files on a server with virus total",
                      brief="No commands here")
    async def run(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == bot.user.id:
            return
        else:
            # Note: I am unsure if this covers all what Discord sees as a link.
            # I tested a bit and it seems to be working but i am just gessing
            URLREGEX = r2 = re.compile(
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                , re.IGNORECASE
            )
            matches = re.findall(URLREGEX, msg.content)
            if len(matches) == 0:
                return
            else:
                await msg.channel.send(
                    "🛑‼⚠️⚠️⚠️️WARNING⚠️⚠️⚠️‼️🛑\n Do never trust any links! Even if you think you know "
                    "the website is safe it might still contain special characters! "
                    "I will run a short test over it but cant ensure anything.")
                for i in matches:
                    if i[len(i) - 1] == '/':
                        i = i[:len(i) - 1]
                    await msg.channel.send(embed=get_url_embed(i, msg))


class Everywhere(commands.Cog, name="Available everywhere"):
    def __init__(self, b):
        self.b = b

    @commands.command(name="Github",
                      brief="Gives you the Github link",
                      help="[This bot is a clone from a Github repository. Click here to open]()")
    async def github(self, ctx):
        await ctx.send("[This bot is a clone from a Github repository. Click here to open]()")


bot.add_cog(ServerCommands(bot))
bot.add_cog(Everywhere(bot))
bot.add_cog(DmCommands(bot))

bot.run(CONFIG['Discord_Bot_Token'])
