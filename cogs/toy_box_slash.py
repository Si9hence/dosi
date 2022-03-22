from code import interact
import yaml
import time
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from supp import memes
import random
import aiohttp
import asyncio
## init
class Info():
    def __init__(self):
        return

INFO = Info()
with open("./configs/info.yaml", "r") as f:
    INFO.servers = yaml.safe_load(f)['servers']

## choice kaibai
class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="开摆!", style=disnake.ButtonStyle.blurple)
    async def bai(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="不摆?", style=disnake.ButtonStyle.blurple)
    async def nobai(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

# name the cog and create a new class for the cog.
class DosiToyBox(commands.Cog, name=":tada:Dosi's toybox"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="meme",
        description="create your own memememememeow",
        guild_ids=[s for s in INFO.servers.values()],
        options=[
            Option(
                name="meme",
                description="The meme you want to use.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="content",
                description="The content you want to insert. Use || to split multiple contents.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    async def meme_maker(self, interaction: ApplicationCommandInteraction, meme, content):
        flag = 0
        contents = [item.strip() for item in content.split("||")]
        flag, response_img, _ = memes.maker_main(meme=meme, sentences=contents)

        if flag == 0:
            await interaction.send('meme not found!')
        else:
            picture = disnake.File(response_img, filename="meme.png")
            await interaction.send(file=picture)

    @commands.slash_command(        
        name="cj8",
        description="cartonj8",
        guild_ids=[s for s in INFO.servers.values()],
        options = [
            Option(
                name="rainbow",
                required=False,
                description="rainbowed cj8!",
                autocomplete=True
            )
        ]
        )
    async def cj8(self, interaction, rainbow=False):
        colors = [0xff0000,0xffa500,0xffff00,0x008000,0x0000ff,0x4b0082,0xee82ee]
        embed = disnake.Embed(
            description="ᕕ( ᐛ )ᕗ",
            color=random.choice(colors)
        )
        await interaction.send(embed=embed)
        if rainbow:
            for _ in range(100):
                embed = disnake.Embed(
                    description="ᕕ( ᐛ )ᕗ",
                    color=random.choice(colors)
                )
                await interaction.edit_original_message(embed=embed)
                await asyncio.sleep(0.1)

    @commands.slash_command(
        name="开摆",
        description="摆还是不摆? 这是一个问题.",
        guild_ids=[s for s in INFO.servers.values()],
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

    @commands.slash_command(
        name="cat",
        description="Give you a random cat!",
        guild_ids=[s for s in INFO.servers.values()],
        options=[
            Option(
                name="option",
                required=False,
                description="specify what kind of cat you want"
            )
        ]
    )
    async def cat(self, interaction: ApplicationCommandInteraction, option=None) -> None:
        if option == None:
            option = 'cat'
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://g.tenor.com/v1/random?&key=HAQEG9GS7Y2X&q={option}&limit=1') as resp:
                if resp.status != 200:
                    return await interaction.send(f'No {option} found 555')
                js = await resp.json()
                await interaction.send(embed=disnake.Embed(title=f"I am a random {option}~💕").set_image(url=js['results'][0]['media'][0]['gif']['url']))

    # @commands.slash_command(
    #     name="dog",
    #     description="Give you a random dog!",
    #     guild_ids=[s for s in INFO.servers.values()],
    # )
    # async def dog(self, interaction: ApplicationCommandInteraction) -> None:
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get('https://api.thedogapi.com/v1/images/search') as resp:
    #             if resp.status != 200:
    #                 return await interaction.send('No dog found 555')
    #             js = await resp.json()
    #             await interaction.send(embed=disnake.Embed(title="💕").set_image(url=js[0]['url']))

    @commands.slash_command(
        name="emod",
        description="emotional damage",
        guild_ids=[s for s in INFO.servers.values()],
    )
    async def emod(self, interaction: ApplicationCommandInteraction) -> None:
        await interaction.send(embed=disnake.Embed(title='EMOTIONAL DAMAGE').set_image(url='https://c.tenor.com/K9-SqJMNjkEAAAAC/emotional-damage.gif'))

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(DosiToyBox(bot))
