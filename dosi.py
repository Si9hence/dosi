# bot.py
import os
import random
import time
import re

import discord
from discord.ext.commands import Bot
from discord import Intents
from dotenv import load_dotenv

import get_covid
import memes
import io
import cv2
load_dotenv()
# get_covid.data_update()
TOKEN = os.getenv('DISCORD_TOKEN')

# intents = Intents.all()
# client = discord.Client(proxy="http://localhost:7890")
bot = Bot(command_prefix='^^', proxy="http://localhost:7890")
# client = discord.Client(proxy="http://localhost:7890")

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
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.playing, 
                          name = 'in the abySS'))

@bot.command(name='server', enabled=False)
async def fetchServerInfo(ctx):
	guild = ctx.guild
	await ctx.send(f'Server Name: {guild.name}')
	await ctx.send(f'Server Size: {len(guild.members)}')

@bot.command(name='roll', help='roll a dice!')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='covid', enable=True, help="covid trend\n sample code ")
async def covid_trend(ctx, *country):
        country = " ".join([item.strip() for item in country])
        # country = message.content.split(":")[-1].strip()
        response = get_covid.get_new_confirmed(dt=15, country=country)
        await ctx.send(response)



@bot.command(name='meme', enable=True, help="memememememow")
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
        picture = discord.File(response_img, filename="meme.png")
        await ctx.send(file=picture)

@bot.command(name='开摆!', enable=True, help="摆还是不摆, 这是一个问题.")
async def kaibai_cmd(ctx):
    take_a_break = [
        "开摆!"*random.randint(1,30),
        # "摆"*random.randint(1,30)+"!",
        "别摆了, "*random.randint(1,30)+"别摆了!"
    ]
    response = random.choice(take_a_break)
    await ctx.send(response)


async def send_picture(src, message):
    with open(src, 'rb') as f:
        picture = discord.File(f)
        await message.channel.send(file=picture)
    return

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
        await send_picture(src = "./data/img/sabwnk.jpg", message=message)
    elif message.content == '开摆!':
        response = kaibai_legacy()
        await message.channel.send(response)
    elif re.search("^do you want to (build|code) a (\w* )?snowman\??$", content_modified, flags=re.IGNORECASE):
        response = snowman(msg=content_modified.lower())
        await message.channel.send(response)
    elif message.content == 'ᕕ( ᐛ )ᕗ':
        await message.channel.send("```'ᕕ( ᐛ )ᕗ'```")
    else:
        pass
    await bot.process_commands(message)
bot.run(TOKEN)
# client.run(TOKEN)
