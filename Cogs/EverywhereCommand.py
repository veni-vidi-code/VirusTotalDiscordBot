from discord.ext import commands


class Everywhere(commands.Cog, name="Available everywhere"):
    """
    Cog with Commands that are available in dms and guilds
    """

    def __init__(self, b):
        self.b = b
        print("General Commands succesfully added to the bot!")

    @commands.command(name="Github",
                      brief="Gives you the Github link",
                      help="[This bot is a clone from a Github repository. Click here to open]()")
    async def github(self, ctx):
        await ctx.send("[This bot is a clone from a Github repository. Click here to open]()")
