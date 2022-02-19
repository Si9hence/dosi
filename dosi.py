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

load_dotenv()
get_covid.data_update()
TOKEN = os.getenv('DISCORD_TOKEN')

# intents = Intents.all()
bot = Bot(command_prefix='!', proxy="http://localhost:7890")

client = discord.Client(proxy="http://localhost:7890")

@bot.event
async def on_ready():
    print(f'{bot.user.name} wakes up!')


@client.event
async def on_ready():
    print(f'{client.user.name} wakes up!')

@bot.command(name='server', help = 'Fetches server information')
async def fetchServerInfo(ctx):
	guild = ctx.guild
	print(1)
	await ctx.send(f'Server Name: {guild.name}')
	await ctx.send(f'Server Size: {len(guild.members)}')
	await ctx.send(f'Server Name: {guild.owner.display_name}')
# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )


@client.event
async def on_message(message):

    if client.user == message.author:
        # print(message.author)
        return
    print(message.author)
    def check_content(msg):
        reserved = {
            " wanna ": " want to "
        }
        
        for word in reserved:
            if word in msg:
                msg = msg.replace(word, reserved[word])
        return msg

    # async def send_picture(src):
    #     with open(src, 'rb') as f:
    #         picture = discord.File(f)
    #         await message.channel.send(file=picture)
    #     return
    content_modified = check_content(message.content)
    # print(check_content(message.content))
    # print(message.content)
    # print(message.content)

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    take_a_break = [
        "开摆!"*random.randint(1,30),
        # "摆"*random.randint(1,30)+"!",
        # "别摆了, "*random.randint(1,30)+"别摆了!"
    ]

    inventory = (
        'do you want to build a snowman?',
        '99!',
        '开摆!',
        'covid: country'
    )

    def show_option(inventory=inventory):
        res = ""
        for item in inventory:
            res += item + "\n"
        return res

    # def snowman():
    #     snowmans = ("\_\_===\_\_\n \\\\(o_O)\n   (]    [)>\n   (       )",
    #                 "\_===\_\n ( . , . )\n (   :   )\n (   :   )"

    #                 )
    #     return snowmans[1]

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
        print(txt)
        if (flag := txt[-2]) != "a" and (flag := txt[-2]) != "":
            return build_snowman(flag=flag)
        else:
            return build_snowman()
    # if message.content == 'Hi DotherSi9H':
    #     await message.channel.send(show_option())
    # elif message.content == 'Hi Dosi':
    #     response = f'AbaAba, why not try <{random.choice(inventory)}> !'
    #     await message.channel.send(response)
    # elif "covid:" in message.content:
    #     country = message.content.split(":")[-1].strip()
    #     response = get_covid.get_new_confirmed(dt="", country=country)
    #     await message.channel.send(response)
    # elif message.content == '99!':
    #     response = random.choice(brooklyn_99_quotes)
    #     await message.channel.send(response)
    # elif message.content == '开摆!':
    #     response = random.choice(take_a_break)
    #     await message.channel.send(response)
    # elif message.content == 'do you want to build a snowman?':
    #     await message.channel.send(snowman())
    # elif message.content == 'raise-exception':
    #     raise discord.DiscordException

    lmal = "Not a good time. Leave me alone. THX."
    # time.sleep(3)
    if message.content == 'Hi DotherSi9H':
        pass
        # await message.channel.send(lmal)
    elif message.content == 'Hi Dosi':
        # response = f'AbaAba, why not try <{random.choice(inventory)}> !'
        # await message.channel.send(lmal)
        pass
    elif message.content == '+1':
        await message.channel.send("+1")
    # elif re.search("^covid: \w+$", content_modified, flags=re.IGNORECASE):
    elif re.search("^Hey dosi I'm terribly sorry I'm just wondering if by any chance you happen to have time to very kindly inform me about the covid in the( \w+)+$", content_modified, flags=re.IGNORECASE):
        country = message.content.split("the")[-1].strip()
        # country = message.content.split(":")[-1].strip()
        response = get_covid.get_new_confirmed(dt=15, country=country)
        await message.channel.send(response)
        if random.randint(0, 20) > 15:
            await message.channel.send("Hump, just let you know Dosi gives you the information because Dosi likes you! (Don't tell Nobody!)")
    elif re.search("^covid:( \w+)+", content_modified, flags=re.IGNORECASE):
        if random.randint(0, 20) > 5:
            country = message.content.split(":")[-1].strip()
            # country = message.content.split(":")[-1].strip()
            response = get_covid.get_new_confirmed(dt=15, country=country)
            await message.channel.send(response)
        else:
            await message.channel.send("Unfortunately, at the moment I am afraid that I don't have time to help you with your request. I am terribly sorry for that and I hope you find someone else to help you.")


    # elif "covid:" in message.content:
    #     country = message.content.split(":")[-1].strip()
    #     response = get_covid.get_new_confirmed(dt=20, country=country)
    #     await message.channel.send(response)
    elif message.content == '99!':
        # response = random.choice(brooklyn_99_quotes)
        with open("./img/sabwnk.jpg", 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        # await message.channel.send(lmal)
    elif message.content == '开摆!':
        response = random.choice(take_a_break)
        await message.channel.send(response)
    elif re.search("^do you want to (build|code) a (\w* )?snowman\??$", content_modified, flags=re.IGNORECASE):
        response = snowman(msg=content_modified.lower())
        await message.channel.send(response)
    elif message.content == 'ᕕ( ᐛ )ᕗ':
        await message.channel.send("```'ᕕ( ᐛ )ᕗ'```")
    elif message.content == 'raise-exception':
        raise discord.DiscordException

bot.run(TOKEN)
# client.run(TOKEN)
