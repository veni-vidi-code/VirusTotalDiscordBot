from discord import Forbidden
from discord.ext import commands

from Utils.domain_tester import get_domain_embed


class DmCommands(commands.Cog, name="Dm Commands"):
    """
    Cog including all Commands that are dm only
    """

    def __init__(self, b):
        self.b = b
        print("Dm Commands succesfully added to the bot!")

    @commands.command(name="check",
                      help="Takes given Input and runs a test over it. Only Dm Channels. Accepts URLs",
                      brief="Checks Input", aliases=["test"])
    async def check(self, ctx, *arg):
        if ctx.guild is not None:
            try:
                await ctx.message.delete()
                await ctx.author.send("Only DM Available")
            except Forbidden:
                await ctx.reply("Only DM Available! Warning! The Above message might be milicious. "
                               "Dont click the file/url until you trust it! (for some reason i cant delete it)")
            return
        if arg is None:
            await ctx.send("Missing an url")
            return
        domain = arg[0]
        await ctx.reply(embed=get_domain_embed(domain, ctx))
