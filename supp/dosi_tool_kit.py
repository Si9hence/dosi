import discord
# supp
async def send_picture(src, message):
    with open(src, 'rb') as f:
        picture = discord.File(f)
        await message.channel.send(file=picture)
    return
