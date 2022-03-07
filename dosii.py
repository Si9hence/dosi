# bot.py
import os
import random
import platform
import time
import re


import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context



# import discord
# from discord.ext.commands import Bot
from dotenv import load_dotenv
import yaml
import supp.get_covid as get_covid
import supp.memes as memes
import io

import supp.dosi_tool_kit as dosi_tool_kit
# import cv2
load_dotenv()
# get_covid.data_update()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = disnake.Intents.default()

bot = Bot(command_prefix='^^', proxy="http://localhost:7890", intents=intents)

bot.load_extension("cogs.tool_kit_slash")
@bot.event
async def on_ready():
    print(f'{bot.user.name} wakes up!')
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    print("Dosi wakes up!")
    status_task.start()

@tasks.loop(minutes=5.0)
async def status_task() -> None:
    statuses = ["in Daisy!", "in Erica!", "in Lily!", "in Rose!", "in Sage!", "in Gypsophilia!"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))

bot.run(TOKEN)
