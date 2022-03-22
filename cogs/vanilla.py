from code import interact
import yaml
import random

import disnake
from disnake.ext.commands import Bot
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from supp import memes
from supp import get_covid
# Here we name the cog and create a new class for the cog.

class Info:
    def __init__(self):
        # covid
        info_covid = yaml.safe_load(open('./configs/covid.yaml', "r"))
        covid_alias = "".join([key + " -> " + info_covid['k2c'][key] + "\n" for key in info_covid['k2c']])
        self.help_covid = f"""^^covid <country name>\n
        The country name (case insensitive) is supposed to be official names of countries like Singapore, United Kingdom.\n
        Following alias is allowed:\n
        {covid_alias}
        Last update date:{info_covid['last_update']}\n
        NB: The signal of United stated of America is too week in abyss. so currently not supported.
        """
        # meme
        info_meme = yaml.safe_load(open("./configs/memes.yaml", "r"))
        meme_available = "".join([key + '\n' for key in info_meme['surjection']])
        self.help_meme = f"""^^meme <meme name> <content1> <content2> ...\n
        sample: ^^meme 表演一下 把心里想的说出来就好 想不到也没有办法, 我要去吃饭了.\n
        Tips:\n
        contents are splitted by space. In case content contains spaces, use double quotation marks to join "your content"\n
        command ^^meme <meme name> template will show the meme template\n
        Current available memes:\n
        {meme_available}
        """

        ## vanilla
        self.help_secret = """
        do you wannt build a snowman?\n
        99!\n
        +1\n
        Hey dosi I'm terribly sorry I'm just wondering if by any chance you happen to have time to very kindly inform me about the covid in the Germany\n
        """
INFO = Info()


class Vanilla(commands.Cog, name="Vanilla"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='covid', enable=True, brief="15 days COVID bar chart", help=INFO.help_covid)
    async def covid_trend(self, interaction, *country):
            country = " ".join([item.strip() for item in country])
            # country = message.content.split(":")[-1].strip()
            response = get_covid.get_new_confirmed(dt=15, country=country)
            await interaction.send(response)

    @commands.command(name='meme', enable=True, brief="mememememememeow!", help=INFO.help_meme)
    async def meme_maker(self, interaction, meme, *content):
        flag = 0
        if not content:
            contents = list(" ")
        else:
            contents = list(content)
        flag, response_img, _ = memes.maker_main(meme=meme, sentences=contents)
        if flag == 0:
            await interaction.send('meme not found!')
        else:
            picture = disnake.File(response_img, filename="meme.png")
            await interaction.send(file=picture)

    @commands.command(name='secret', enable=True, brief="A secret makes Dosi Dosi", help=INFO.help_secret)
    async def secret(self, interaction):
        embed = disnake.Embed(
            description=f"{INFO.help_secret}",
            color=0xFAAFAA
        )
        interaction.send(embed=embed)

    # @commands.command(name='开摆!', enable=True, brief="摆还是不摆, 这是一个问题.", help="摆了不解释")
    # async def kaibai_cmd(self, interaction):
    #     take_a_break = [
    #         "开摆!"*random.randint(1,30),
    #         # "摆"*random.randint(1,30)+"!",
    #         "别摆了, "*random.randint(1,30)+"别摆了!"
    #     ]
    #     response = random.choice(take_a_break)
    #     await interaction.send(response)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Vanilla(bot))
