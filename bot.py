# bot.py
import os
import random
import time

import discord
from dotenv import load_dotenv
import get_covid

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    take_a_break = [
        "开摆!开摆!",
        "开摆!开摆!开摆!开摆!开摆!开摆!开摆!",
        f"摆{random.randint(10,30)}分钟!",
        "别摆了, 别摆了."
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

    def snowman():
        snowmans = ("\_\_===\_\_\n \\\\(o_O)\n   (]    [)>\n   (       )",
                    "\_===\_\n( . , . )\n(   :   )\n(   :   )"

                    )
        return snowmans[1]

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
    lmal = "Leave me alone. thx."
    # time.sleep(3)
    if message.content == 'Hi DotherSi9H':
        await message.channel.send(lmal)
    elif message.content == 'Hi Dosi':
        response = f'AbaAba, why not try <{random.choice(inventory)}> !'
        await message.channel.send(lmal)
    elif "covid:" in message.content:
        country = message.content.split(":")[-1].strip()
        response = get_covid.get_new_confirmed(dt="", country=country)
        await message.channel.send(lmal)
    elif message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(lmal)
    elif message.content == '开摆!':
        response = random.choice(take_a_break)
        await message.channel.send(lmal)
    elif message.content == 'do you want to build a snowman?':
        await message.channel.send("\_===\_\n( . , . )\n(   :   )\n(   :   )")
    elif message.content == 'ᕕ( ᐛ )ᕗ':
        await message.channel.send(snowman())
    elif message.content == 'raise-exception':
        raise discord.DiscordException


client.run(TOKEN)