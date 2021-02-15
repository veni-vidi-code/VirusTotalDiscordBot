import re
from pprint import pformat

from discord.ext import commands

from Utils.Url_tester import get_url_embed


class UrlListener(commands.Cog, name="Server URL Listener"):
    def __init__(self, b):
        self.b = b
        print("Url Listener sucessfully added to bot!")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == self.b.user.id:
            pass
        elif str(msg.channel.type) != "private":
            # Note: I am unsure if this covers all what Discord sees as a link.
            # I tested a bit and it seems to be working but i am just gessing
            urlregex = re.compile(
                        r'^(?:http|ftp)s?://' # http:// or https://
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                        r'localhost|' #localhost...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                        r'(?::\d+)?' # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            matches = re.findall(urlregex, msg.content)
            if len(matches) == 0:
                pass
            else:
                for c in matches:
                    if c[len(c) - 1] == '/':
                        c = c[:len(c) - 1]
                    await msg.channel.send(embed=await get_url_embed(c, msg))

            if len(msg.embeds) != 0 and msg.author.bot:
                print("check")
                for e in msg.embeds:
                    from pprint import pprint
                    pprint(e.to_dict())
                    matches = re.findall(urlregex, pformat(e.to_dict()))
                    if len(matches) == 0:
                        print("0")
                        pass
                    else:
                        for c in matches:
                            if c[len(c) - 1] == '/':
                                c = c[:len(c) - 1]
                            await msg.channel.send(embed=await get_url_embed(c, msg))
