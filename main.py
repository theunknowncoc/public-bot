#!/usr/bin/python3
import os
import requests
import json
import coc
import aiohttp
from asyncio import sleep
from datetime import datetime
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel, Intents
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
                                  CommandOnCooldown, Context, when_mentioned_or, command, has_permissions, CheckAnyFailure)
from db import db
from difflib import SequenceMatcher
from dotenv import load_dotenv as dotenv
from PIL import Image
from urllib.request import urlopen

dotenv()

TOKEN = os.getenv("token")
PREFIX = "$"
VERSION = "1.8.0"
OWNER_IDS = [1, 2]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument, aiohttp.ClientOSError)

COGS = ["GodPerms", "Help", "Basic", "ForEveryone",
        "RankPerms", "SeasonPerms", "GenPerms", "CosPerms", "DB", 'Music']


def get_prefix(bot, message):
    try:
        prefix = db.field(
            "SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    except:  # for dms
        prefix = "$"
    return when_mentioned_or(prefix)(bot, message)


def sanitize(url) -> str:
    url2 = url.split("/")
    return f"{url2[4]}-{url2[5]}"


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog) -> None:
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        with open("jsondata/mutelist.json") as f:
            self.banlist = json.load(f)

        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix,
                         owner_ids=OWNER_IDS, intents=Intents.all())
        #self.coc_client = client
        self.seasonsfinished = True
        self.godsid = 801243015016087562

    def setup(self):
        for cog in COGS:
            self.load_extension(f"cogs.{cog}")
            print(f" {cog} cog loaded")
        print("setup complete")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))

        db.multiexec("INSERT OR IGNORE INTO tags (UserID) VALUES (?)",
                     ((member,) for member in self.ids))

        db.commit()

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        self.TOKEN = os.getenv("token")

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        if self.ready:
            await self.stdout.send("I am back online\n")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_guild_join(self, guild):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))
        db.commit()
        await guild.system_channel.send(f"Hi! Nice server you got going {guild.owner.mention}! My default prefix is $, but you can change that with $prefix <newprefix>. \
                                        Please run $help to learn more about me!\n\n*__I am a bot and my owners are Gulag#2001/Holster4#9516, please consult them for inquiries__*")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            print(err, args, kwargs)
        elif isinstance(err, Forbidden):
            pass
        elif hasattr(err, "original"):
            if isinstance(err.original, Forbidden):
                pass
        else:
            await self.stdout.send("An error occured.")
            raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, CheckAnyFailure):
            await ctx.send("You don't have perms to do that lmao")

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention}, that command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")

        elif isinstance(exc, Forbidden):
            pass

        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
            # 	await ctx.send("Unable to send message.")
            if isinstance(exc.original, Forbidden):
                try:
                    await ctx.send("I do not have permission to do that.")
                except:
                    print('couldnt send a message in {} in {}'.format(
                        ctx.guild.name, ctx.channel.name))
            else:
                raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(1)
            self.stdout = self.get_channel(1)
            self.ids = self.get_cog("GodPerms").allperms
            self.update_db()
            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            print("Now online!")
            await self.stdout.send("I am alive")
            self.ready = True
            print(" bot ready")
            await self.stdout.send("Version {}".format(self.VERSION))
        else:
            print("bot reconnected")

    async def on_shutdown(self):
        print("Shutting down...")
        await super().close()

    async def on_close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if message.author.id in self.banlist:
                await ctx.send("You are banned from using commands.")

            elif not self.ready:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

            else:
                await self.invoke(ctx)

    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if member.guild.id == 1:
            channel = await self.fetch_channel(1)
            await channel.send("Welcome to {0.guild.name}, {0.mention}, who invited you?".format(member, member))
        elif channel is not None:
            await channel.send("Welcome to {0.guild.name}, {0.mention}!".format(member, member))

    async def on_command(self, ctx):
        async with ctx.typing():
            pass

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=Context)
        if not message.author.bot:
            words = ['fonem', 'cuh', 'crip', 'blood', 'gang', 'foenem']
            repls = ['replies?', 'replies rn', 'replies rfn', 'how are replies',
                     'reply time', 'how are replys', 'how are responses', 'replies fast']
            if any(word in message.content.lower().replace("0", "O") for word in words) and message.content[0] != '$' and "on" in message.content.lower():
                await ctx.invoke(self.get_command('fonem'))
                return
            if any(repl in message.content.lower() for repl in repls):
                await ctx.send(f"{message.author.mention} SHUT THE FUCK UP AND CHECK YOURSELF NIGGA GODDAMN")
                return

            if isinstance(message.channel, DMChannel) and message.author.id not in [801243015016087562]:
                await message.channel.send("Please use commands in a server.")
            else:
                await self.process_commands(message)

        with open("logs/log.txt", "a", encoding='UTF-8') as f:
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M")
            try:
                a = message.guild.name
                f.write("\n{} ({}) wrote {} in {}~{} ({}) at {} EST".format(message.author, message.author.id,
                        message.content, message.guild.name, message.channel, message.guild.id, dt_string))
            except AttributeError:
                f.write("\n{} ({}) wrote {} in DMs at {} EST".format(
                    message.author, message.author.id, message.content, dt_string))

        if ctx.valid or message.author.id == 801558267284815892:
            with open("logs/log-commands.txt", "a", encoding="UTF-8") as z:
                now = datetime.now()
                dt_string = now.strftime("%m/%d/%Y %H:%M")
                try:
                    a = message.guild.name
                    z.write("\n{} ({}) wrote {} in {}~{} ({}) at {} EST".format(message.author, message.author.id,
                            message.content, message.guild.name, message.channel, message.guild.id, dt_string))
                except AttributeError:
                    z.write("\n{} ({}) wrote {} in DMs at {} EST".format(
                        message.author, message.author.id, message.content, dt_string))

        if message.attachments != [] and message.author.id != 801558267284815892:
            url = message.attachments[0].url
            if "mp4" in url or "wav" in url or "mov" in url:  # doesnt work dk
                op = urlopen(url)
                with open("unsentmedia/{}.{}".format(sanitize(url), url[-3:]), 'wb') as f:
                    f.write(op.read())
            else:
                im = Image.open(requests.get(url, stream=True).raw)
                im.save("unsentmedia/{}.png".format(sanitize(url)))

        if message.author.id in self.banlist:
            if message.author.id == 1 and message.channel.id == 1:
                return
            try:
                await message.delete()
            except:
                pass

    async def on_message_edit(self, before, after):
        before.content = before.content.replace(
            "@everyone", '`@everyone`').replace('@here', '`@here`')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M %p EST")
        msg = f'<@{before.author.id}> edited a message at {dt_string} EST. "{before.content}" is the old message.'
        if before.content and before.author.id != self.godsid:
            db.execute(
                "UPDATE guilds SET Editsnipe = ? WHERE GuildID = ?", msg, before.guild.id)
            db.commit()
        logmode = db.field(
            "SELECT Logging FROM guilds WHERE GuildID = ?", before.guild.id)
        if logmode and not before.author.bot and before.author.id != self.godsid and before.author.id not in self.banlist:
            similarity = SequenceMatcher(
                None, before.content, after.content).ratio()
            if similarity < .9:
                await before.channel.send(msg)

    async def on_raw_message_edit(self, payload):
        channel = self.get_channel(payload.channel_id)
        try:
            message = await channel.fetch_message(payload.message_id)
        except:
            return
        else:
            await self.process_commands(message)

    async def on_message_delete(self, message):
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M %p EST")
        message.content = message.content.replace(
            "@everyone", '`@everyone`').replace('@here', '`@here`')
        msg = f'<@{message.author.id}> unsent a message "{message.content}" at {dt_string}'
        if message.content and message.author.id != self.godsid:
            db.execute("UPDATE guilds SET Snipe = ? WHERE GuildID = ?",
                       msg, message.guild.id)
            db.commit()
        logmode = db.field(
            "SELECT Logging FROM guilds WHERE GuildID = ?", message.guild.id)
        if logmode and not message.author.bot and message.author.id != self.godsid and message.author.id not in self.banlist:
            if message.attachments == []:
                await message.channel.send(f'<@{message.author.id}> unsent a message "{message.content}" at {dt_string}')
            else:
                url = message.attachments[0].url
                print(url)
                await message.channel.send(f'<@{message.author.id}> unsent an image at {dt_string}')
                await message.channel.send(file=File(f"unsentmedia/{sanitize(url)}.png"))

    async def on_invite_create(self, invite):
        with open("logs/log-invites.txt", "a", encoding="utf-8") as f:
            f.write(
                f"{invite.guild.name} {invite.guild.id} {invite.inviter} {invite.inviter.id} {invite.url}\n")


bot = Bot()
if __name__ == "__main__":
    bot.run(VERSION)
