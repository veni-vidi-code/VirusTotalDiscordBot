import json
from asyncio import sleep

import discord
from virustotal_python import Virustotal

import Cogs.settings as settings

print("starting up file tester unit")
try:
    with open("Config.json", "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    with open("Config.json", "w") as f:
        json.dump({'Discord_Bot_Token': 'YOURTOKEN', 'VirusTotalToken': 'YOURTOKEN',
                   'YourDiscordId': '0', 'Prefix': '&'}, f)
    raise Exception("Missing Config.json. I added it, please fill it out yourself! (Intended at first excecution)")

print("file tester loaded with key " + CONFIG['VirusTotalToken'])
vtotal = Virustotal(API_KEY=CONFIG['VirusTotalToken'], API_VERSION="v2")


async def get_file_embed(attachment: discord.Attachment, ctx):
    if attachment.size > 4000000:
        embed = discord.Embed(title="VirusTotalBot File Check",
                              description="Information about " + attachment.filename,
                              color=discord.Colour.red())
        embed.set_author(name=str(ctx.author))
        embed.add_field(name="Size", value=str(attachment.size), inline=True)
        embed.add_field(name="Value", value="The file is to big, i can not scan it. Sorry", inline=True)
        return embed
    r = await attachment.read()
    files = {"file": (attachment.filename, r, "rb")}
    embed = discord.Embed(title="VirusTotalBot File Check",
                          description="Information about " + attachment.filename,
                          color=discord.Colour.green())
    embed.set_author(name=str(ctx.author))

    resp = vtotal.request("file/scan", files=files, method="POST")
    shasum = resp.json()['sha256']
    await sleep(10)
    resp = vtotal.request("file/report", {"resource": shasum})
    resp = resp.json()
    while resp['response_code'] != 1:
        await sleep(50)
        resp = vtotal.request("file/report", {"resource": shasum})
        resp = resp.json()
    embed.add_field(name="SHA256 Checksum", value=resp['sha256'], inline=True)
    embed.add_field(name="Total Amount of checks", value=resp['total'], inline=True)
    embed.add_field(name="positive checks",
                    value="Amount of Viruscheckers that detect a potential virus: " + str(resp['positives']),
                    inline=True)
    pchecks = ""
    if resp['positives'] != 0:
        for i in resp['scans'].keys():
            if resp['scans'][i]['detected'] and resp['scans'][i]['result'] is not None:
                pchecks += str(i) + " detected, result = " + str(resp['scans'][i]['result']) + "\n"
            elif resp['scans'][i]['detected']:
                pchecks += str(i) + " detected\n"
        embed.add_field(name="by Sites", value=pchecks, inline=True)
    if resp['positives'] >= settings.checkorange:
        embed.color = discord.Colour.orange()
    if resp['positives'] >= settings.checkred:
        embed.color = discord.Colour.red()

    return embed
