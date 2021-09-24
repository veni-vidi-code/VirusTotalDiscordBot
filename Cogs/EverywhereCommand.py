from discord.ext import commands

from Utils.Helpembed import helpembed


class Everywhere(commands.Cog, name="Available everywhere"):
    """
    Cog with Commands that are available in dms and guilds
    """

    def __init__(self, b: commands.Bot):
        self.b = b
        print("General Commands succesfully added to the bot!")

    @commands.command(name="Github",
                      brief="Gives you the Github link",
                      help="This bot is a clone from a Github repository. Click here to open:"
                           "\nhttps://github.com/veni-vidi-code/VirusTotalDiscordBot")
    async def github(self, ctx):
        await ctx.reply(
            "This bot is a clone from a Github repository. Click here to open:"
            "\nhttps://github.com/veni-vidi-code/VirusTotalDiscordBot")

    @commands.command(name="info")
    async def info(self, ctx):
        await ctx.reply(embed=helpembed)
