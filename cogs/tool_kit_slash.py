import json
import os
import sys
import platform
import random 
import yaml

import aiohttp
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
import supp.get_covid as get_covid

# Here we name the cog and create a new class for the cog.
class DosiToolkit(commands.Cog, name="Dosi's toolkit"):
    def __init__(self, bot):
        self.bot = bot
        self.info_covid = yaml.safe_load(open('./configs/covid.yaml', "r"))
        self.covid_alias = "".join([key + " -> " + self.info_covid['k2c'][key] + "\n" for key in self.info_covid['k2c']])
        self.help_covid = f"""^^covid <country name>\n
        The country name (case insensitive) is supposed to be official names of countries like Singapore, United Kingdom.\n
        Following alias is allowed:\n
        {self.covid_alias}
        Last update date:{self.info_covid['last_update']}\n
        NB: The signal of United stated of America is too week in abyss. so currently not supported.
        """
    @commands.slash_command(
        name="covid",
        description="covid function",
        guild_ids=[941248152575541269],
        options=[
            Option(
                name="country",
                description="The country you want to check.",
                type=OptionType.string,
                required=True
            )
        ],
        # auto_sync=False
    )
    async def covid(self, interaction: ApplicationCommandInteraction, country: str):
        country = list(country)
        country = " ".join([item.strip() for item in country])
        print(country)
        # country = message.content.split(":")[-1].strip()
        response = get_covid.get_new_confirmed(dt=15, country=country)
        print(response)
        embed = disnake.Embed(
            description=f"{response}",
            color=0xD75BF4
        )
        await interaction.channel.send(content="1", embed = embed)



    @commands.slash_command(
        name="ping",
        description="Check if the bot is alive.",
        guild_ids=[941248152575541269],
    )
    async def ping(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Check if the bot is alive.
        :param interaction: The application command interaction.
        """
        embed = disnake.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await interaction.channel.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(DosiToolkit(bot))
