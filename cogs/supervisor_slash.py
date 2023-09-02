import yaml
import sqlite3
# import aiofiles
import datetime
import random
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType, SlashCommand
from disnake.ext import commands, tasks
from supp import get_covid
from supp import remind
import asyncio

class Supervisor(commands.Cog, name=":owl:Dosi's supervisor"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="guilds",
        description="currently on development",
        guild_ids=[941248152575541269],
    )
    async def guilds(self, interaction: ApplicationCommandInteraction):
        # activeservers = self.bot.guilds
        res = ""
        guilds = await self.bot.fetch_guilds().flatten()
        for guild in guilds:
            res += f"`{guild.name}` {guild.id}\n"
            for channel in await guild.fetch_channels():
                res += f"`{channel.name}` {channel.id}\n"
            res += "\n"
        # print(res)
        embed = disnake.Embed(
            description = res
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="uid",
        description="currently on development",
        guild_ids=[941248152575541269],
    )
    async def uid(self, interaction: ApplicationCommandInteraction):
        res = f"{interaction.author.name}: {interaction.author.id}"
        embed = disnake.Embed(
            description = res
        )
        await interaction.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Supervisor(bot))
