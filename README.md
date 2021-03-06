# VirusTotalDiscordBot
Simple Discord Bot that scans messages in Servers for urls and files and checks them with virus total

Why this instead of the one already hosted? Many people want to know who gets their files and can read their messages or want to change parts of the code. So i quickly wrote this bot in python, which allows it to be integrated into most other bots as well



It is still in alpha and im working on it


If you want to use it i suggest running it in a docker container


On first loading it will throw an error after creating a config.json file, fill it with you discord bot token and your VirusTotal Api Token, then reload the bot

Now the bot should send warnings on servers where urls, files and domains get posted and should test them
