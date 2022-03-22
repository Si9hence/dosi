""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import random
import sys
import yaml
import time
import disnake
import aiohttp
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from supp import memes


class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="daisy", style=disnake.ButtonStyle.blurple)
    async def a1(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="cat", style=disnake.ButtonStyle.blurple)
    async def a2(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()



class Info():
    def __init__(self):
        return

INFO = Info()
with open("./configs/info.yaml", "r") as f:
    INFO.servers = yaml.safe_load(f)['servers']

class Test(commands.Cog, name="test module"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="Blank",
        description="Blank",
        guild_ids=[s for s in INFO.servers.values()],
    )
    async def some_sc(self, interaction: ApplicationCommandInteraction):
        return None


    # @commands.slash_command(
    #     name="aa",
    #     description="Blank",
    #     guild_ids=[s for s in INFO.servers.values()],
    # )
    # async def some_sc(self, interaction: ApplicationCommandInteraction):
    #     buttons = Choice()
    #     await interaction.send(view=buttons)
    #     while True:
    #         buttons = Choice()
    #         await interaction.edit_original_message(view=buttons)
    #         await buttons.wait()
    #         if buttons.choice == "cat":
    #             async with aiohttp.ClientSession() as session:
    #                 async with session.get('https://api.thecatapi.com/v1/images/search') as resp:
    #                     if resp.status != 200:
    #                         return await interaction.send('No dog found 555')
    #                     js = await resp.json()
    #                     await interaction.author.send(embed=disnake.Embed(title='I am a random 💕').set_image(url=js[0]['url']))
    #         else:
    #             await interaction.author.send(content=buttons.choice)
        # while True:
        #     await interaction.edit_original_message(view=buttons)
        #     await buttons.wait()
        #     # await interaction.send(content=buttons.choice)
        #     await interaction.author.send(content=buttons.choice)
        #     bottons = Choice()




def setup(bot):
    bot.add_cog(Test(bot))
