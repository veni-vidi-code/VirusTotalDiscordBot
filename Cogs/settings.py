import random

from discord import Colour

"""
These are some presets configs, that are predefined
and normally dont need any changes (Thats why they are not in the config file
"""

bottest = True  # decides if the bot checks other bots messages

ignorfiles = ['image/gif', 'image/jpeg']  # Content types to ignor. Check out https://en.wikipedia.org/wiki/Media_type

checkorange = 1  # if more or equal than that checks are positive the embed will be orange

checkred = 3  # if more or equal than that checks are positive the embed will be red

helpembedcolour = Colour(random.randint(0, 16777215))
