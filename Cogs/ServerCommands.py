from discord.ext import commands


class ServerCommands(commands.Cog, name="Server Commands"):
    def __init__(self, b):
        self.b = b
        print("Server Commands succesfully added to the bot!")

    @commands.command(name="Function on server",
                      help="This bot checks all links and files on a server with virus total",
                      brief="No commands here")
    async def run(self):
        pass
