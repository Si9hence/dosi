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

import aiohttp
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="开摆!", style=disnake.ButtonStyle.blurple)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="不摆?", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()



class Test(commands.Cog, name="test module"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="开摆",
        description="摆还是不摆? 这是一个问题.",
        guild_ids=[941248152575541269,925477279142903868],
    )
    async def kaibai(self, interaction: ApplicationCommandInteraction) -> None:

        buttons = Choice()
        embed = disnake.Embed(
            description="Nah, I am gonna flip a coin to decide whether to 摆 or 不摆\nWhat is your choice?",
            color=0x9C84EF
        )
        message = await interaction.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["开摆!", "支楞起来!"])
        mp = {"开摆!":"开摆!", "支楞起来!":"不摆?"}
        if buttons.choice == mp[result]:
            # User guessed correctly
            embed = disnake.Embed(
                description=f"Congs! `{result}`.",
                color=0x9C84EF
            )
        else:
            embed = disnake.Embed(
                description=f"Woops! You chose to `{buttons.choice}` but the coin is `{result}`, better luck next time!",
                color=0x002147
            )
        await interaction.edit_original_message(embed=embed, view=None)



def setup(bot):
    bot.add_cog(Test(bot))
