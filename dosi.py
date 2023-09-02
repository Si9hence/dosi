# bot.py
from http.client import CONFLICT
import os
import random
import platform
import time
import re

import yaml
import datetime 
import sqlite3

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context
# import discord
# from discord.ext.commands import Bot
from supp import get_covid
from supp import dosi_tool_kit
# from supp import authorization
# import cv2
# get_covid.data_update()

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



with open("./configs/dosi.yaml") as f:
    CONFIG = yaml.safe_load(f)

with open("./configs/token.yaml") as f:
    TOKEN = yaml.safe_load(f)['token']
intents = disnake.Intents.default()

bot = Bot(command_prefix=CONFIG['prefix'], intents=intents)


@bot.event
async def on_ready():

    """
    The code in this even is executed when the bot is ready
    """
    print("extensions")
    for file in os.listdir("./cogs"):
        if len(file.split(".")) == 2:
            file = file.split(".")[0]
            print(file)
            bot.load_extension(f"cogs.{file}")

    activeservers = bot.guilds
    # print(activeservers)
    print("-------------------")
    print("registered server")
    for guild in activeservers:
        print(guild.id, guild.name)
    print("-------------------")
    # print(f"Logged in as {bot.user.name}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    print(f'{bot.user.name} wakes up!')
    status_task.start()

@bot.event
async def on_voice_state_update(member, before, after):

    def vc_id_check(status):
        if status.channel:
            return [status.channel, status.channel.id]
        else:
            return ["None", "None"]
    def rec_channel():
    # print(datetime.)
    # print(member)
        status_bf = vc_id_check(before)
        status_af = vc_id_check(after)
        conn = sqlite3.connect('./data/db/test.db')
        cursor = conn.cursor()
        cursor.execute(f"insert into rec (ts, user, before, before_id, after, after_id) values ('{str(datetime.datetime.now())}', '{str(member)}', '{status_bf[0]}', '{status_bf[-1]}', '{status_af[0]}', '{status_af[-1]}')")
        cursor.close()
        conn.commit()
        conn.close()
    rec_channel()
    # if after.channel:
    #     if after.channel.id == 941248155415093261:
    #         member_list.start()

@bot.event
async def on_reminder(a):
    aa = bot.get_all_channels()
    for item in aa:
        print(item, item.id)
    chn = bot.get_channel(952299623886749696)
    await chn.send(a)
    print(a)


@tasks.loop(minutes=5.0)
async def status_task() -> None:
    statuses = ["in Daisy!", "in Erica!", "in Lily!", "in Rose!", "in Sage!", "in Gypsophilia!"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))


# @tasks.loop(seconds=5)
# async def member_list(dst=941248155415093261) -> None:
#     channel = bot.get_channel(dst)
#     curMembers = []
#     for member in channel.members:
#         curMembers.append(member)
#     print(curMembers)
#     if len(curMembers) == 0:
#         member_list.stop()
#         print("rec stopped")



@bot.event
async def on_message(message):
    if bot.user == message.author:
        return
    else:
        
        pass
        # user = bot.get_user(926846583788687402)
        # buttons = Choice()
        # embed = disnake.Embed(
        #     description="Dosi would like to know more about you. Do you mind sharing your discord activity with Dosi?\n\
        #         **Please** be aware that by accpeting the request, the bot will record the time when you enter a channel in this guild.",
        #     color=0x9C84EF
        # )
        # msg = await message.author.send(embed=embed, view=buttons)
        # await buttons.wait()  # We wait for the user to click a button.
        # if buttons.choice == "sure!":
        #     # User guessed correctly
        #     embed = disnake.Embed(
        #         description="ahhhh Thanks! Dosi will keep your privacy a secret!",
        #         color=0x9C84EF
        #     )
        # else:
        #     embed = disnake.Embed(
        #         description="No worries!",
        #         color=0x002147
        #     )
        # print(buttons.choice)
        # await msg.edit(embed=embed, view=None)
    # else:
    #     print(message.author.name)
    #     print(message.author.id)
    
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
        response = f"Hi {message.author.nick}!"
        await message.channel.send(response)
    elif message.content == '11':
        for item in bot.slash_commands:
            print(item.name)
            print(item.body)

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
