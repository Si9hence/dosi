import yaml
import sqlite3
# import aiofiles
import datetime
import random
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands, tasks
from supp import get_covid
from supp import dosi_tool_kit
import asyncio

# init
class Info():
    pass

INFO = Info()
with open("./configs/info.yaml", "r") as f:
    INFO.servers = yaml.safe_load(f)['servers']

## choice authorization
class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="Sure!", style=disnake.ButtonStyle.blurple)
    async def bai(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Nah...", style=disnake.ButtonStyle.blurple)
    async def nobai(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Yes", style=disnake.ButtonStyle.blurple)
    async def positive(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Maybe next time", style=disnake.ButtonStyle.blurple)
    async def negative(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

class DosiToolkit(commands.Cog, name=":wrench:Dosi's toolkit"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="reminder",
        description="currently on development",
        guild_ids=[s for s in INFO.servers.values()],
        options=[
            Option(
                name="name",
                description="the name of the reminder",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="description",
                description="the description of the reminder",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="days",
                description="how many days you want to sleep",
                type=OptionType.integer,
                required=False
            ),
            Option(
                name="hours",
                description="how many hours you want to sleep",
                type=OptionType.integer,
                required=False
            ),
            Option(
                name="minutes",
                description="how many minutes you want to sleep",
                type=OptionType.integer,
                required=False
            ),
            Option(
                name="seconds",
                description="how many seconds you want to sleep",
                type=OptionType.integer,
                required=False
            ),
        ],
        # auto_sync=False
    )
    async def reminder(self, interaction: ApplicationCommandInteraction, name=None, description=None, days=0, hours=0, minutes=0, seconds=0):
        # country = message.content.split(":")[-1].strip()
        # embed = disnake.Embed(
        #     description=f"{response}",
        #     color=0xFAAFAA
        # )
        if days+hours+minutes+seconds == 0:
            await interaction.send('at least 1 seconds!')
        utcnow = datetime.datetime.utcnow()
        info = {'author': interaction.user.id,
        'name': name,
        'description': description,
        'created': utcnow,
        'duration': datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds),
        'extra': None}
        tmp = dosi_tool_kit.Timer(info=info, bot=self.bot)
        await interaction.send('Dosi will reminds u in 1 hours!')
        await tmp.dispatch()

    
    @commands.slash_command(
        name="covid",
        description="covid function",
        guild_ids=[s for s in INFO.servers.values()],
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
        await interaction.send(response)
    
    @commands.slash_command(
        name="help",
        description="a help functon for clash command",
        guild_ids=[s for s in INFO.servers.values()],
        # options=[
        #     Option(
        #         name="command",
        #         description="The command you want to check.",
        #         type=OptionType.string,
        #         required=False
        #     )
        # ],
        # auto_sync=False
    )
    async def help(self, interaction: ApplicationCommandInteraction):
        async def des_simple(cogs=self.bot.cogs.items()):
            res = str()
            for cog in cogs:
                if cog[0] == "Vanilla":
                    continue
                res += f"**{cog[0]}**\n"
                for cmd in cog[1].get_slash_commands():
                    res += f"`/{cmd.name}`\n"
                    if cmd.options:
                        for opt in cmd.options:
                            res += f"-{opt.name}: {opt.description}\n" 
                res += "\n"
            return res
        # print(await self.bot.fetch_guild_commands(941248152575541269))
        # for cmd in await self.bot.fetch_guild_commands(interaction.user.guild.id):
        #     print(cmd.name, cmd.description, cmd.options)
        content = "Dosi is a :door: :bowl_with_spoon: Dosi.\n You could use the following slash commands to call Dosi (if she is free).\n\n"
        # Use `/help <command>` to get more informaiton.\n\n"
        content += await des_simple(cogs=self.bot.cogs.items())
        embed = disnake.Embed(
            description = content
        )
        await interaction.send(embed=embed)

    @commands.slash_command(        
        name="sing",
        description="sing",
        guild_ids=[s for s in INFO.servers.values()],
        options=[
            Option(
                name="song",
                description="Currently not available",
                type=OptionType.string,
                required=False
            )
        ],
        # auto_sync=False
    )
    async def sing(self, interaction: ApplicationCommandInteraction, song=None):
        # async with aiofiles.open('./test/乌鸦.lrc', "r", encoding="utf-8") as f:
        #     contents = f.readlines()
        if song:
            try:
                with open(f'./data/lrc/{song}.lrc', "r", encoding="utf-8") as f:
                    contents = f.readlines()
            except:
                await interaction.send(content="Song not found!")

        for idx, itm in enumerate(contents):
            tmp = itm.split("]", 1)
            if tmp[1] == "" or tmp[1] == "\n":
                tmp[1] = "...\n"
            try:
                tmp[0] = datetime.datetime.strptime(tmp[0][1::],"%M:%S.%f")
            except:
                continue
            if idx == 0:
                t_p = tmp[0]
                tmp[0] = datetime.timedelta(0).total_seconds()
            else:
                t_p, tmp[0] = tmp[0], (tmp[0] - t_p).total_seconds()
            contents[idx] = tmp
        # print(contents)
        colors = [0xff0000,0xffa500,0xffff00,0x008000,0x0000ff,0x4b0082,0xee82ee]
        for idx, content in enumerate(contents):
            embed = disnake.Embed(
                description=content[1],
                color=random.choice(colors)
            )
            if idx == 0:
                await interaction.send(embed=embed)
            else:
                await interaction.edit_original_message(embed=embed)
            if idx < len(contents) - 1:
                await asyncio.sleep(contents[idx+1][0])
        return None

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(DosiToolkit(bot))
