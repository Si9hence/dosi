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

# bot.load_extension("cogs.tool_kit_slash")

# change presence
# https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.Bot.change_presence
@bot.event
async def on_ready():
    print(f'{bot.user.name} wakes up!')
    # await bot.change_presence(activity = discord.Activity(
    #     type = discord.ActivityType.competing,
    #     name = 'Kindergarten'))

    # activeservers = bot.guilds
    # print(activeservers)
    # for guild in activeservers:
    #     if guild.id == 925477279142903868:
    #         for channel in guild.channels:
    #             print(guild.id, guild.name, channel.name, channel.created_at, channel.overwrites)
    # await bot.change_presence(activity = discord.Activity(
    #     type = discord.ActivityType.playing,
    #     name = 'SOlO'))
    # await bot.change_presence(activity = discord.Activity(
    #                       type = discord.ActivityType.playing, 
    #                       name = 'OutSIDe'))
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
    statuses = ["in Diasy!", "in Erica!", "in Lily!", "in Rose!", "in Sage!", "in Gypsophilia!"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))


@bot.command(name='server', enabled=False)
async def fetchServerInfo(ctx):
	guild = ctx.guild
	await ctx.send(f'Server Name: {guild.name}')
	await ctx.send(f'Server Size: {len(guild.members)}')

@bot.command()
async def showguilds(ctx):
    message = ""
    for guild in bot.guilds:
         message += f"{guild.name}\n{guild.id}\n"
    await ctx.send(message)

info_covid = yaml.safe_load(open('./configs/covid.yaml', "r"))
covid_alias = "".join([key + " -> " + info_covid['k2c'][key] + "\n" for key in info_covid['k2c']])
help_covid = f"""^^covid <country name>\n
The country name (case insensitive) is supposed to be official names of countries like Singapore, United Kingdom.\n
Following alias is allowed:\n
{covid_alias}
Last update date:{info_covid['last_update']}\n
NB: The signal of United stated of America is too week in abyss. so currently not supported.
"""
@bot.command(name='covid', enable=True, brief="15 days COVID bar chart", help=help_covid)
async def covid_trend(ctx, *country):
        country = " ".join([item.strip() for item in country])
        # country = message.content.split(":")[-1].strip()
        response = get_covid.get_new_confirmed(dt=15, country=country)
        await ctx.send(response)

info_meme = yaml.safe_load(open("../configs/memes.yaml", "r"))
meme_available = "".join([key + '\n' for key in info_meme['surjection']])
help_meme = f"""^^meme <meme name> <content1> <content2> ...\n
sample: ^^meme 表演一下 把心里想的说出来就好 想不到也没有办法, 我要去吃饭了.\n
Tips:\n
contents are splitted by space. In case content contains spaces, use double quotation marks to join "your content"\n
command ^^meme <meme name> template will show the meme template\n
Current available memes:\n
{meme_available}
"""
@bot.command(name='meme', enable=True, brief="mememememememeow!",help=help_meme)
async def meme_maker(ctx, template=None, *content):
    flag = 0
    print(content)
    if template == None:
        return
    else:
        if not content:
            contents = list(" ")
        else:
            contents = list(content)

        if contents[0] == 'template':
            print('meme template')
            flag, response_img, _ = memes.maker_template(meme=template)
        else:
            print('meme normal')
            flag, response_img, _ = memes.maker_main(meme=template, sentences=contents)
    
    if flag == 0:
        await ctx.send('meme not found!')
    else:
        picture = disnake.File(response_img, filename="meme.png")
        await ctx.send(file=picture)

@bot.command(name='开摆!', enable=True, brief="摆还是不摆, 这是一个问题.", help="摆了不解释")
async def kaibai_cmd(ctx):
    take_a_break = [
        "开摆!"*random.randint(1,30),
        # "摆"*random.randint(1,30)+"!",
        "别摆了, "*random.randint(1,30)+"别摆了!"
    ]
    response = random.choice(take_a_break)
    await ctx.send(response)

help_secret = """
do you wannt build a snowman?\n
99!\n
+1\n
Hey dosi I'm terribly sorry I'm just wondering if by any chance you happen to have time to very kindly inform me about the covid in the Germany\n
"""
@bot.command(name='secret', enable=True, brief="A secret makes Dosi Dosi", help=help_secret)



@bot.event
async def on_message(message):
    if bot.user == message.author:
        return
    
    # elif str(message.author) != "Si9H#0724":
    #     print(str(message.author))
    #     doutside()
    #     return

    # async def doutside():
    #     send_picture(src="./img/doutside.jpg", message=message)
    #     return

    def check_content(msg):
        reserved = {
            " wanna ": " want to "
        }
        
        for word in reserved:
            if word in msg:
                msg = msg.replace(msg, reserved[word])
        return msg

    content_modified = check_content(message.content)

    def snowman(msg: str):
        # msg is expected to be in lowercase
        def random_gen():
            res = ""
            for _ in range(8):
                res += str(random.randint(1, 4))
            return res

        def build_snowman(flag = None):
            reserved = {
                "jenny": "\_\_===\_\_\n \\\\(o_O)\n   (]    [)>\n   (       )",
                "si9h": "\_===\_\n ( . , . )\n (   :   )\n (   :   )"
            }

            res = str()
            # print(flag)
            # print(message.author)
            if (flag == "xiaohei" or flag== "heihei") and \
                (str(message.author) == "Shirley2333#5348" or str(message.author) == "Si9H#0724"):
                return "No I dont. yao build you build.\n\
                ```( ^ω^)```"
            if (flag == "wq" or flag == "wls" or flag == "沁宝" or flag == "Alicia"):
                if str(message.author) == "Shirley2333#5348":
                    pass
                else:
                    # channel.send(file=discord.File('./img/wq.png'))
                    return "Hush, Hush Don't tell nobody. Alicia is Shirley's private snowman."
            if flag:
                res += f"{flag} snowman! \n"
                if flag in reserved:
                    res += reserved[flag]
                    return res
                else:
                    flag = random_gen()
            elif flag == None:
                flag = random_gen()
                

            V = '.oO-'
            def D(i): return int(flag[i]) - 1

            res += "```" + "  " + ("", "___", " _ ", "___")[D(0)] + "\n " +\
                "_. (=./_=._*=.\\__. )"[D(0)::4]+"\n" +\
                " \\  "[D(4)] + "("+V[D(2)] + ',._ '[D(1)]+V[D(3)]+")" + " /  "[D(5)]+'\n' +\
                "< / "[D(4)] + "(" + " ]> :    [< "[D(6)::4]+")" + "> \\ "[D(5)] + "\n (" +\
                ' "_ : _  "_ '[D(7)::4]+")" + "```"
            return res

        txt = re.search("^do you want to (build|code) a\s?\w*\s*snowman\??$", msg).string.split(" ")
        # print(txt)
        if (flag := txt[-2]) != "a" and (flag := txt[-2]) != "":
            return build_snowman(flag=flag)
        else:
            return build_snowman()

    def kaibai_legacy():
        take_a_break = [
            "开摆!"*random.randint(1,30),
            # "摆"*random.randint(1,30)+"!",
            "别摆了, "*random.randint(1,30) + "别摆了!"
        ]
        response = random.choice(take_a_break)
        return response


    # time.sleep(3)
    if re.search("^Hi.*Dosi$", content_modified, flags=re.IGNORECASE):
        response = f"Hi {message.author.nick}"
        await message.channel.send(response)
    elif message.content == '+1':
        await message.channel.send("+1")
    elif re.search("^Hey dosi I'm terribly sorry I'm just wondering if by any chance you happen to have time to very kindly inform me about the covid in the( \w+)+$", content_modified, flags=re.IGNORECASE):
        country = message.content.split("the")[-1].strip()
        # country = message.content.split(":")[-1].strip()
        response = get_covid.get_new_confirmed(dt=15, country=country)
        await message.channel.send(response)
        if random.randint(0, 20) > 15:
            await message.channel.send("Hump, just let you know Dosi gives you the information because Dosi likes you! (Don't tell Nobody!)")
    elif re.search("^covid:( \w+)+", content_modified, flags=re.IGNORECASE):
        if random.randint(0, 20) > 2:
            country = message.content.split(":")[-1].strip()
            # country = message.content.split(":")[-1].strip()
            response = get_covid.get_new_confirmed(dt=15, country=country)
            await message.channel.send(response)
        else:
            await message.channel.send("Unfortunately, at the moment I am afraid that I don't have time to help you with your request. I am terribly sorry for that and I hope you find someone else to help you.")
    elif message.content == '99!':
        await dosi_tool_kit.send_picture(src = "./data/img/sabwnk.jpg", message=message)
    elif message.content == '开摆!':
        response = kaibai_legacy()
        await message.channel.send(response)
    elif re.search("^do you want to (build|code) a (\w* )?snowman\??$", content_modified, flags=re.IGNORECASE):
        response = snowman(msg=content_modified.lower())
        await message.channel.send(response)
    elif message.content == 'ᕕ( ᐛ )ᕗ':
        await message.channel.send("```'ᕕ( ᐛ )ᕗ'```")
    # elif message.content == 'welcome back, I miss you... a little bit':
    #     await message.channel.send("I know~```ᕕ( ᐛ )ᕗ```")
    else:
        pass
    await bot.process_commands(message)
bot.run(TOKEN)
# client.run(TOKEN)
