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
