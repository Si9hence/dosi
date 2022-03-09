import yaml

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
import supp.get_covid as get_covid

info_covid = yaml.safe_load(open('./configs/covid.yaml', "r"))
covid_alias = "".join([key + " -> " + info_covid['k2c'][key] + "\n" for key in info_covid['k2c']])
help_covid = f"""^^covid <country name>\n
The country name (case insensitive) is supposed to be official names of countries like Singapore, United Kingdom.\n
Following alias is allowed:\n
{covid_alias}
Last update date:{info_covid['last_update']}\n
NB: The signal of United stated of America is too week in abyss. so currently not supported.
"""


# Here we name the cog and create a new class for the cog.
class DosiToolkit(commands.Cog, name="Dosi's toolkit"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="covid",
        description="covid function",
        guild_ids=[941248152575541269,925477279142903868],
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
        # country = message.content.split(":")[-1].strip()
        response = get_covid.get_new_confirmed(dt=15, country=country)
        # embed = disnake.Embed(
        #     description=f"{response}",
        #     color=0xFAAFAA
        # )
        await interaction.send(content=response)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(DosiToolkit(bot))
