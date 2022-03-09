from code import interact
import yaml

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from supp import memes
# Here we name the cog and create a new class for the cog.
class DosiToyBox(commands.Cog, name="Dosi's toybox"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="meme",
        description="meme maker",
        guild_ids=[941248152575541269,925477279142903868],
        options=[
            Option(
                name="meme",
                description="The meme you want to use.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="content",
                description="The content you want to add",
                type=OptionType.string,
                required=True
            )
        ],
    )
    async def meme_maker(self, interaction: ApplicationCommandInteraction, meme, content):
        flag = 0
        contents = content.split("||")
        flag, response_img, _ = memes.maker_main(meme=meme, sentences=contents)

        if flag == 0:
            await interaction.send('meme not found!')
        else:
            picture = disnake.File(response_img, filename="meme.png")
            await interaction.send(file=picture)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(DosiToyBox(bot))
