'''
Simple boiler plate on self botting
'''
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="$", self_bot=True)

selfBotToken = ""


@client.command()
async def getmsgs(ctx, channelid) -> None:
    try:
        z = await client.fetch_channel(channelid)
        async for message in z.history(limit=20):
            print(message.content)
    except Exception as e:
        print(repr(e))

client.run(selfBotToken, bot=False)
