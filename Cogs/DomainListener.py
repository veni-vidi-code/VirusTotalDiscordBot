import re
from pprint import pformat

from discord.ext import commands

from Utils.domain_tester import get_domain_embed


class DomainListener(commands.Cog, name="Server Domain Listener"):
    def __init__(self, b):
        self.b = b
        print("Domain Listener sucessfully added to bot!")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == self.b.user.id:
            pass
        elif str(msg.channel.type) != "private":
            # Note: I am unsure if this covers all what Discord sees as a link.
            # I tested a bit and it seems to be working but i am just gessing
            domainregex = re.compile(
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                , re.IGNORECASE
            )
            matches = re.findall(domainregex, msg.content)
            if len(matches) == 0:
                pass
            else:
                await msg.channel.send(
                    "🛑‼⚠️⚠️⚠️️WARNING⚠️⚠️⚠️‼️🛑\n Do never trust any links! Even if you think you know "
                    "the website is safe it might still contain special characters! "
                    "I will run a short test over it but cant ensure anything. \nNotice that i dont test files that "
                    "would be downloaded via a link, im just testing the domain")
                for c in matches:
                    if c[len(c) - 1] == '/':
                        c = c[:len(c) - 1]
                    await msg.channel.send(embed=get_domain_embed(c, msg))

            if len(msg.embeds) != 0 and msg.author.bot:
                for e in msg.embeds:
                    matches = re.findall(domainregex, pformat(e.to_dict()))
                    if len(matches) == 0:
                        pass
                    else:
                        await msg.channel.send(
                            "🛑‼⚠️⚠️⚠️️WARNING⚠️⚠️⚠️‼️🛑\n Do never trust any links! Even if you think you know "
                            "the website is safe it might still contain special characters! "
                            "I will run a short test over it but cant ensure anything.\n"
                            "This is just about the domain, not the actual page")
                        for c in matches:
                            await msg.channel.send(embed=get_domain_embed(c, msg))
