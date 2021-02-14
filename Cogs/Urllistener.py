import re
from pprint import pformat

from discord.ext import commands

from Utils.url_tester import get_url_embed


class URLListener(commands.Cog, name="Server Listener"):
    def __init__(self, b):
        self.b = b
        print("URL Listener sucessfully added to bot!")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == self.b.user.id:
            pass
        elif str(msg.channel.type) != "private":
            # Note: I am unsure if this covers all what Discord sees as a link.
            # I tested a bit and it seems to be working but i am just gessing
            urlregex = re.compile(
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                , re.IGNORECASE
            )
            matches = re.findall(urlregex, msg.content)
            if len(matches) == 0:
                pass
            else:
                await msg.channel.send(
                    "🛑‼⚠️⚠️⚠️️WARNING⚠️⚠️⚠️‼️🛑\n Do never trust any links! Even if you think you know "
                    "the website is safe it might still contain special characters! "
                    "I will run a short test over it but cant ensure anything.")
                for c in matches:
                    if c[len(c) - 1] == '/':
                        c = c[:len(c) - 1]
                    await msg.channel.send(embed=get_url_embed(c, msg))

            if len(msg.embeds) != 0:
                for e in msg.embeds:
                    urlregex = re.compile(
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                        , re.IGNORECASE
                    )
                    matches = re.findall(urlregex, pformat(e.to_dict()))
                    if len(matches) == 0:
                        pass
                    else:
                        await msg.channel.send(
                            "🛑‼⚠️⚠️⚠️️WARNING⚠️⚠️⚠️‼️🛑\n Do never trust any links! Even if you think you know "
                            "the website is safe it might still contain special characters! "
                            "I will run a short test over it but cant ensure anything.")
                        for c in matches:
                            if c[len(c) - 1] == '/':
                                c = c[:len(c) - 1]
                            await msg.channel.send(embed=get_url_embed(c, msg))
