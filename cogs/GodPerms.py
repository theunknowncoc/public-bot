from .A import *
import aiofiles
import asyncio
from datetime import timedelta
from dateutil.parser import parse
from discord import Embed, File, Game
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import BucketType, Cog, command, cooldown
from db import db
from os.path import isfile


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        super().__init__(data, per_page=10)
        self.god = 1
        self.gods_url = f"https://cdn.discordapp.com/avatars/{self.god}/b0df2621a8f5b5155a561cca35a3e79e.webp?size=1024"

    async def write_page(self, menu, fields=[]):
        try:
            offset = (menu.current_page*self.per_page) + 1
            len_data = len(self.entries)
            embed = Embed(title="**Menu**", description="**Here's your list, God**",
                        color=random_hex(), timestamp=datetime.utcnow())
            embed.set_author(name="Queried by {}".format(
                self.ctx.message.author.name), icon_url=self.ctx.message.author.avatar_url)
            embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
            embed.set_footer(
                text=f'Showing {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} items', icon_url=self.gods_url)

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)
            return embed
        except Exception as e:
            print(repr(e))

    async def format_page(self, menu, entries):
        try:
            fields = []
            if type(entries[0]) == tuple:
                for entry in entries:
                    fields.append((entry[0], entry[1]))
            else:
                for idx in range(len(entries)):
                    fields.append((str(10*menu.current_page+idx+1)+".", entries[idx]))
            return await self.write_page(menu, fields)
        except Exception as e:
            print(repr(e))


class GodPerms(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.god = 1
        with open('jsondata/perms.json') as f:
            data = json.load(f)
        self.rankperms = data['rankperms']
        self.seasonperms = data['seasonperms']
        self.genperms = data['genperms']
        self.cosperms = data['cosperms']
        self.allperms = list(set(list(self.rankperms.keys(
        )) + list(self.seasonperms.keys()) + list(self.genperms.keys()) + list(self.cosperms.keys())))
        self.allperms = sorted(self.allperms)
        self.godperms = [1, self.god]
        self.gods_url = f"https://cdn.discordapp.com/avatars/{self.god}/b0df2621a8f5b5155a561cca35a3e79e.webp?size=1024"
        self.logerrormode = False

    async def reload(self):
        self.bot.unload_extension("SeasonPerms")
        self.bot.load_extension("SeasonPerms")
        self.bot.unload_extension("RankPerms")
        self.bot.load_extension("RankPerms")
        self.bot.unload_extension("GenPerms")
        self.bot.load_extension("GenPerms")
        self.bot.unload_extension("CosPerms")
        self.bot.load_extension("CosPerms")
        self.bot.unload_extension("Help")
        self.bot.load_extension("Help")
        self.bot.unload_extension("GodPerms")
        self.bot.load_extension("GodPerms")
        while not self.bot.cogs_ready.all_ready():
            await sleep(0.5)

    def merge(self, list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list

    def not_expired(self, type, ctx) -> bool:
        if type == 1:
            currperm = self.rankperms
            usrend = currperm[str(ctx.message.author.id)][list(
                currperm[str(ctx.message.author.id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True
        elif type == 2:
            currperm = self.seasonperms
            usrend = currperm[str(ctx.message.author.id)][list(
                currperm[str(ctx.message.author.id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True
        elif type == 3:
            currperm = self.genperms
            usrend = currperm[str(ctx.message.author.id)][list(
                currperm[str(ctx.message.author.id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True
        elif type == 4:
            currperm = self.cosperms
            usrend = currperm[str(ctx.message.author.id)][list(
                currperm[str(ctx.message.author.id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True

    @Cog.listener()
    async def on_ready(self):
        self.startepoch = time()
        self.uptime = time() - self.startepoch
        self.clocker = "seconds"
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("GodPerms")

        with open("jsondata/restart.json") as f:
            data = json.load(f)
        global logerrormode
        logerrormode = data[0]['outputerror']

        #self.status = cycle(["You", "Me", "$help", "God's Plan", "with your feelings", f"Raping {len(self.bot.guilds)} servers"], 'Uptime: ')
        self.change_status.start()
        self.rm_unsentmedia.start()

    @tasks.loop(seconds=3)
    async def change_status(self):
        self.uptime = time()-self.startepoch
        if self.uptime < 60:
            self.currentuptime = self.uptime
        if self.uptime > 60 and self.uptime < 3600:
            self.currentuptime = self.uptime/60
            self.clocker = "minutes"
        if self.uptime > 3600 and self.uptime < 86400:
            self.currentuptime = self.uptime/3600
            self.clocker = "hours"
        elif self.currentuptime > 86400:
            self.currentuptime = self.uptime/86400
            self.clocker = "days"
        self.status = cycle(
            ["$help | Uptime: {:.2f} {}".format(self.currentuptime, self.clocker)])
        await self.bot.change_presence(activity=Game(next(self.status)))

    @tasks.loop(seconds=3600)
    async def rm_unsentmedia(self):
        if os.name == "nt":
            os.system("del /Q unsentmedia\*")
        elif os.name == "posix":
            os.system("rm unsentmedia/*")

    async def givesafuck(self, ctx):
        await ctx.send(file=File('pictures/givesafuck.jpg'))

    @command(help="$pushperms 1 @God", brief="pushes permissions for a user, num = 1/2/3/4/all")
    async def pushperms(self, ctx, num, user: discord.User, time: float = 30):
        if ctx.message.author.id in self.godperms:
            id = user.id
            key = {'1': 'rank perms', '2': 'season perms',
                   '3': 'gen perms', '4': 'cos perms', 'all': 'any perms'}
            if num == '1' or num == "all":
                if time == 0 and str(id) not in self.rankperms:
                    self.rankperms[str(id)] = {str(datetime.now()): None}
                elif time == 0:
                    self.rankperms[str(id)][list(
                        self.rankperms[str(id)].keys())[0]] = None
                elif str(id) not in self.rankperms:
                    self.rankperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()+timedelta(days=time))}
                else:
                    rawdate = parse(self.rankperms[str(id)][list(
                        self.rankperms[str(id)].keys())[0]])
                    if rawdate < datetime.now():
                        rawdate = datetime.now()
                    rawdate += timedelta(days=time)
                    date = str(rawdate)
                    self.rankperms[str(id)][list(
                        self.rankperms[str(id)].keys())[0]] = date
            if num == '2' or num == "all":
                if time == 0 and str(id) not in self.seasonperms:
                    self.seasonperms[str(id)] = {str(datetime.now()): None}
                elif time == 0:
                    self.seasonperms[str(id)][list(
                        self.seasonperms[str(id)].keys())[0]] = None
                elif str(id) not in self.seasonperms:
                    self.seasonperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()+timedelta(days=time))}
                else:
                    rawdate = parse(self.seasonperms[str(id)][list(
                        self.seasonperms[str(id)].keys())[0]])
                    if rawdate < datetime.now():
                        rawdate = datetime.now()
                    rawdate += timedelta(days=time)
                    date = str(rawdate)
                    self.seasonperms[str(id)][list(
                        self.seasonperms[str(id)].keys())[0]] = date
            if num == '3' or num == "all":
                if time == 0 and str(id) not in self.genperms:
                    self.genperms[str(id)] = {str(datetime.now()): None}
                elif time == 0:
                    self.genperms[str(id)][list(
                        self.genperms[str(id)].keys())[0]] = None
                elif str(id) not in self.genperms:
                    self.genperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()+timedelta(days=time))}
                else:
                    rawdate = parse(self.genperms[str(id)][list(
                        self.genperms[str(id)].keys())[0]])
                    if rawdate < datetime.now():
                        rawdate = datetime.now()
                    rawdate += timedelta(days=time)
                    date = str(rawdate)
                    self.genperms[str(id)][list(
                        self.genperms[str(id)].keys())[0]] = date
            if num == '4' or num == "all":
                if time == 0 and str(id) not in self.cosperms:
                    self.cosperms[str(id)] = {str(datetime.now()): None}
                elif time == 0:
                    self.cosperms[str(id)][list(
                        self.cosperms[str(id)].keys())[0]] = None
                elif str(id) not in self.cosperms:
                    self.cosperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()+timedelta(days=time))}
                else:
                    rawdate = parse(self.cosperms[str(id)][list(
                        self.cosperms[str(id)].keys())[0]])
                    if rawdate < datetime.now():
                        rawdate = datetime.now()
                    rawdate += timedelta(days=time)
                    date = str(rawdate)
                    self.cosperms[str(id)][list(
                        self.cosperms[str(id)].keys())[0]] = date
            else:
                await ctx.send("Invalid num.")
                return
            await ctx.send(f'{user.mention} now has {key[num]}')
            jj = {'rankperms': self.rankperms, 'seasonperms': self.seasonperms,
                  'genperms': self.genperms, 'cosperms': self.cosperms}
            with open("jsondata/perms.json", 'w') as f:
                json.dump(jj, f, indent=2)
            print('reloading')
            await self.reload()
        else:
            await self.givesafuck(ctx)

    @command(help="$pullperms 1 @God", brief="pulls permissions from a user")
    async def pullperms(self, ctx, num, user: discord.User, time: float = 30):
        if ctx.message.author.id in self.godperms:
            id = user.id
            key = {'1': 'rank perms', '2': 'season perms',
                   '3': 'gen perms', '4': 'cos perms', 'all': 'any perms'}
            if num == '1' or num == "all":
                if time == 0 and str(id) not in self.rankperms:
                    self.rankperms[str(id)] = {str(
                        datetime.now()): str(datetime.now())}
                elif time == 0:
                    self.rankperms[str(id)][list(self.rankperms[str(id)].keys())[
                        0]] = str(datetime.now())
                elif str(id) not in self.rankperms:
                    self.rankperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()-timedelta(days=time))}
                else:
                    rawdate = parse(self.rankperms[str(id)][list(
                        self.rankperms[str(id)].keys())[0]])
                    rawdate -= timedelta(days=time)
                    date = str(rawdate)
                    self.rankperms[str(id)][list(
                        self.rankperms[str(id)].keys())[0]] = date
            if num == '2' or num == "all":
                if time == 0 and str(id) not in self.seasonperms:
                    self.seasonperms[str(id)] = {str(
                        datetime.now()): str(datetime.now())}
                elif time == 0:
                    self.seasonperms[str(id)][list(self.seasonperms[str(id)].keys())[
                        0]] = str(datetime.now())
                elif str(id) not in self.seasonperms:
                    self.seasonperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()-timedelta(days=time))}
                else:
                    rawdate = parse(self.seasonperms[str(id)][list(
                        self.seasonperms[str(id)].keys())[0]])
                    rawdate -= timedelta(days=time)
                    date = str(rawdate)
                    self.seasonperms[str(id)][list(
                        self.seasonperms[str(id)].keys())[0]] = date
            if num == '3' or num == "all":
                if time == 0 and str(id) not in self.genperms:
                    self.genperms[str(id)] = {str(
                        datetime.now()): str(datetime.now())}
                elif time == 0:
                    self.genperms[str(id)][list(self.genperms[str(id)].keys())[
                        0]] = str(datetime.now())
                elif str(id) not in self.genperms:
                    self.genperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()-timedelta(days=time))}
                else:
                    rawdate = parse(self.genperms[str(id)][list(
                        self.genperms[str(id)].keys())[0]])
                    rawdate -= timedelta(days=time)
                    date = str(rawdate)
                    self.genperms[str(id)][list(
                        self.genperms[str(id)].keys())[0]] = date
            if num == '4' or num == "all":
                if time == 0 and str(id) not in self.cosperms:
                    self.cosperms[str(id)] = {str(
                        datetime.now()): str(datetime.now())}
                elif time == 0:
                    self.cosperms[str(id)][list(self.cosperms[str(id)].keys())[
                        0]] = str(datetime.now())
                elif str(id) not in self.cosperms:
                    self.cosperms[str(id)] = {str(datetime.now()): str(
                        datetime.now()-timedelta(days=time))}
                else:
                    rawdate = parse(self.cosperms[str(id)][list(
                        self.cosperms[str(id)].keys())[0]])
                    rawdate -= timedelta(days=time)
                    date = str(rawdate)
                    self.cosperms[str(id)][list(
                        self.cosperms[str(id)].keys())[0]] = date
            else:
                await ctx.send("Invalid num.")
                return
            await ctx.send(f'{user.mention} no longer has {key[num]}')
            jj = {'rankperms': self.rankperms, 'seasonperms': self.seasonperms,
                  'genperms': self.genperms, 'cosperms': self.cosperms}
            with open("jsondata/perms.json", 'w') as f:
                json.dump(jj, f, indent=2)
            await self.reload()
        else:
            await self.givesafuck(ctx)

    @command(help="$showperms", brief="shows who has perms")
    @cooldown(5, 60, BucketType.user)
    async def showperms(self, ctx):
        if ctx.message.author.id in self.godperms:
            with open('jsondata/perms.json') as f:
                data = json.load(f)
            allperms = ['<@{}>'.format(i) for i in self.allperms]
            menu = MenuPages(source=HelpMenu(
                ctx, allperms), delete_message_after=True, timeout=200.0)
            await menu.start(ctx)
        else:
            await self.givesafuck(ctx)

    @command(help="$iopen pictures/retard.jpg", brief="opens a local file")
    @cooldown(1, 10, BucketType.user)
    async def iopen(self, ctx, img: str):
        if ctx.message.author.id in self.godperms:
            await ctx.send(file=File(img))

    @command(help="$dmspam @God 100", brief="spams the dms lol")
    @cooldown(10, 60, BucketType.user)
    async def dmspam(self, ctx, user: discord.User = "", num: int = 1):
        if ctx.message.author.id in [self.god, 1, 1]:
            try:
                n = 0
                while n < num:
                    n += 1
                    await user.send("""
Fuck you bitch ass, pussy ass nigga
Ugly ass nigga, dark ass nigga
Black ass nigga, bitch ass nigga
Orphan ass nigga, thot ass mom havin' ass nigga
STD havin' ass nigga, walkin' STD ass nigga
Fake Dior wearin' ass nigga
Fake ass clothes wearin' ass nigga
Broke ass nigga, bitch ass nigga
Family ain't never had no mother fuckin' portions ass nigga
"I was supposed to be an abortion" ass nigga
Dirty ass nigga, bum ass nigga
Black ass nigga, ugly ass nigga
Dumb ass nigga
I hope yo' ass get ran over, bitch ass nigga
Fuck you, nigga
""")

            except Exception as e:
                await ctx.send(repr(e))
        else:
            await self.givesafuck(ctx)

    @command(help="$leave 1", brief="leaves a server given a server id")
    async def leave(self, ctx, guildinput):
        if ctx.message.author.id == self.god:
            try:
                guildid = int(guildinput)
            except:
                await ctx.send("Invalid guild: failed to convert to int")
            try:
                guild = self.bot.get_guild(guildid)
            except:
                await ctx.send("Invalid guild")
            try:
                await guild.leave()
                await ctx.send(f"left {guild.name}")
            except:
                await ctx.send("Error leaving")

    @command(help="$echo you're a retard", brief="repeats back what you say")
    @cooldown(3, 20, BucketType.user)
    async def echo(self, ctx, *, args):
        if ctx.message.author.id == self.god or ctx.message.author.id == 391896531747340298:
            await ctx.send(args)

    @command(help="$restart", brief="restarts the bot")
    @cooldown(1, 1200, BucketType.user)
    async def restart(self, ctx, password=False):
        if ctx.message.author.id == self.god or password:
            await ctx.send("Welcome God")
            await ctx.send("Restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            await ctx.send("Enter the password:")
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content != "No":
                await ctx.send("Expelling Intruders...")
            else:
                await ctx.invoke(self.bot.get_command('restart'), password=True)

    @command(help='$exit', brief='kills the bot', aliases=['kill', 'shutdown'])
    async def exit(self, ctx, password=False):
        if ctx.message.author.id == self.god or password:
            await ctx.send("Shutting down....")
            sys.exit()
        else:
            await ctx.send("Enter the password:")
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content != "NiggersRBad":
                await ctx.send("Expelling Intruders...")
            else:
                await ctx.send("Welcome God")
                await ctx.invoke(self.bot.get_command('exit'), password=True)

    @command(help="$spam", brief="spam lol")
    @cooldown(1, 20, BucketType.user)
    async def spam(self, ctx):
        if ctx.message.author.id == self.god:
            await ctx.send('''a\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\n
                                a\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\n''')

    @command(help="$serverlist", brief="shows a list of every server the bot is in")
    @cooldown(1, 20, BucketType.user)
    async def serverlist(self, ctx):
        if ctx.message.author.id == self.god:
            s = time()
            z = await self.bot.application_info()
            servers = list(self.bot.guilds)
            sttr = ""
            for server in servers:
                sttr += f"ID: {server.id} Name: {server.name}\n"
            embed = Embed(title='Server List',
                          color=random_hex(), timestamp=datetime.utcnow())
            embed.set_author(name='Queried by {}'.format(
                ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            embed.add_field(name='{}\'s servers'.format(
                z.name), value=f'**{sttr}**')
            e = time()
            embed.set_footer(
                text='{:.2f} seconds • Made by Gulag#2001'.format(e-s), icon_url=self.bot.get_cog("GodPerms").gods_url)
            await ctx.send(embed=embed, delete_after=20.0)

    @command(help='$channellist 1', brief='shows all channels in a server', aliases=['clist'])
    @cooldown(5, 60, BucketType.user)
    async def channellist(self, ctx, serverID: int):
        if ctx.message.author.id == self.god:
            s = time()
            z = await self.bot.fetch_guild(serverID)
            chans = await z.fetch_channels()
            sttr = ''
            for chan in chans[:10]:
                sttr += f'ID: {chan.id} Name: {chan.name}\n'
            embed = Embed(title='Channel List',
                          color=random_hex(), timestamp=datetime.utcnow())
            embed.set_author(name='Queried by {}'.format(
                ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            embed.add_field(name='{}\'s channels'.format(
                z.name), value=f'**{sttr}**')
            e = time()
            embed.set_footer(
                text='{:.2f} seconds • Made by Gulag#2001'.format(e-s), icon_url=self.bot.get_cog("GodPerms").gods_url)
            await ctx.send(embed=embed, delete_after=20.0)

    @command(name='inv')
    async def create_inv(self, ctx, channelID: int):
        if ctx.message.author.id == self.god:
            s = time()
            z = await self.bot.fetch_channel(channelID)
            inv = await z.create_invite()
            await ctx.send(inv)

    @command(help="$blacklist #2PP", brief="(un)blacklists a tag")
    async def blacklist(self, ctx, tag, arg1):
        if ctx.message.author.id == self.god:
            try:
                Account(tag)
                with open("jsondata/private.json") as f:
                    data = json.load(f)
                if tag[0] != "#":
                    tag = "#"+tag
                tag = tag.upper()
                if arg1 == "1":
                    data.append(tag)
                    await ctx.send("{} was blacklisted".format(tag))
                elif arg1 == "2":
                    data.remove(tag)
                    await ctx.send("{} was un-blacklisted".format(tag))
                else:
                    await ctx.send("Invalid argument")
                    return
                data = list(set(data))
                with open("jsondata/private.json", "w") as f:
                    json.dump(data, f)
            except Exception as e:
                await ctx.send("Pardon nigga? Invalid/Banned tag retard.")

    @command(help="$cmembers 1", brief="see who's in a server id")
    @cooldown(1, 20, BucketType.user)
    async def cmembers(self, ctx, id):
        if ctx.message.author.id in self.godperms:
            s = time()
            z = await self.bot.fetch_guild(id)
            sttr = ''
            async for mem in z.fetch_members(limit=1000):
                sttr += "<@!{}>, {}\n".format(mem.id, mem.name)
            embed = Embed(title='Members in {}'.format(
                z.name), color=random_hex(), timestamp=datetime.utcnow())
            embed.set_author(name='Queried by {}'.format(
                ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            embed.add_field(name='{}\'s members'.format(
                z.name), value=f'**{sttr}**')
            e = time()
            embed.set_footer(
                text='{:.2f} seconds • Made by Gulag#2001'.format(e-s), icon_url=self.bot.get_cog("GodPerms").gods_url)
            await ctx.send(embed=embed, delete_after=20.0)

    @command(help="$shell echo hello > hello.txt", brief="run shell commands")
    @cooldown(1, 10, BucketType.user)
    async def shell(self, ctx, *, args):
        if ctx.message.author.id == self.god:
            await ctx.send(os.popen(args).read())

    @command(help="$phish", brief="basic help guide for noobies")
    @cooldown(3, 60, BucketType.user)
    async def phish(self, ctx):
        if str(ctx.message.author.id) in self.genperms or str(ctx.message.author.id) in self.cosperms or str(ctx.message.author.id) in self.seasonperms or str(ctx.message.author.id) in self.rankperms:
            await ctx.send('```Here are some good tips on what commands to use...\ndeadranks - find dead 13s\nseasons - find name changes\nreceipt - fake receipt to get an acc\nprevlocalssum - find locals for an acc\ncreation - find when an acc was made\ndevices - finds devices for a local\n```')

    @command(help="$ball", brief="nuke command lol", aliases=['banall'])
    async def ball(self, ctx):
        if ctx.message.author.id in self.godperms:
            guild = ctx.message.guild
            for member in list(ctx.message.guild.members):
                try:
                    if member.id not in [self.god, 1, 1]:
                        await guild.ban(member)
                        print("User " + member.name + " has been banned")
                except Exception as e:
                    print(repr(e))
            print("Action Completed: ball")

    @command(help="$kall", brief="nuke command lol (kicking)", aliases=['kickall'])
    async def kall(self, ctx):
        if ctx.message.author.id in self.godperms:
            guild = ctx.message.guild
            for member in list(ctx.message.guild.members):
                try:
                    if member.id != self.god:
                        await guild.kick(member)
                        print("User " + member.name + " has been kicked")
                except Exception as e:
                    print(repr(e))
            print("Action Completed: kall")

    @command(name="unbanme", help="$unban 1", brief="unban myself from guild")
    async def self_unban(self, ctx, id):
        if ctx.message.author.id in self.godperms:
            guild = self.bot.fetch_guild(id)
            guild.unban(ctx.message.author)
            return

    @command(help="$nick God @Gulag_Recroot", brief="change nicknames")
    async def nick(self, ctx, nickN, usr: discord.Member = ""):
        if ctx.message.author.id == self.god:
            if not usr:
                usr = ctx.message.author
            # await self.bot.change_nickname(usr, nick)
            try:
                await usr.edit(nick=nickN)
            except Exception as e:
                print(repr(e))

    @command()
    async def getmsgs(self, ctx, channelid):
        try:
            z = await self.bot.fetch_channel(channelid)
            async for message in z.history(limit=20):
                print(message.content)
        except Exception as e:
            print(repr(e))

    @command(help="$delchannels", brief="deletes all channels in a guild")
    async def delchannels(self, ctx):
        if ctx.message.author.id == self.god:
            for c in ctx.guild.channels:  # iterating through each guild channel
                await c.delete()

    @command(help="$delguild", brief="delete a guild?")
    async def delguild(self, ctx, id):
        if ctx.message.author.id == self.god:
            gid = await self.bot.fetch_guild(id)
            await gid.delete()

    @command(help="$createchannel ok", brief="create a channel in a guild")
    async def createchannel(self, ctx, id, chnname):
        if ctx.message.author.id == self.god:
            gid = await self.bot.fetch_guild(id)
            await gid.create_text_channel(chnname)

    @command(help="$price @God", brief="gets your monthly bot cost price")
    @cooldown(1, 10, BucketType.user)
    async def price(self, ctx, id: discord.Member = ""):
        s = time()
        if not id:
            id = ctx.message.author
        embed = Embed(title="Referrals", description="**Showing {}'s referrals**".format(
            id.mention), timestamp=datetime.utcnow(), color=random_hex())
        embed.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        if not (a := db.field("SELECT referred FROM referral WHERE UserID = ?", id.id)):
            a = 0
            db.execute(
                "INSERT OR IGNORE INTO referral (UserID) VALUES (?)", id.id)
            db.commit()
        else:
            (a := db.field("SELECT referred FROM referral WHERE UserID = ?", id.id))
        if a == 0:
            price = 50
        elif a == 1:
            price = 45
        elif a >= 2:
            price = 40
        referids = db.field(
            "SELECT referredids FROM referral WHERE UserID = ?", id.id)
        referids = ["<@{}>".format(i)
                    for i in referids.split("~") if i != "x" and i]
        embed.add_field(name="{} Referrals, Price = ${} a month".format(
            a, price), value="{}".format(referids), inline=False)
        e = time()
        embed.set_footer(text='{:.2f} seconds • Made by Gulag#2001'.format(
            e-s), icon_url=self.bot.get_cog("GodPerms").gods_url)
        await ctx.send(embed=embed, delete_after=20.0)

    @command(help="$refer @God", brief="link a user as your referral")
    @cooldown(1, 60, BucketType.user)
    async def refer(self, ctx, id: discord.Member = ""):
        if ctx.channel.id != 1:
            await ctx.send("Use this in the referrals channel")
            return
        if not id:
            await ctx.send("Tag someone that you referred!")
            return
        await ctx.send("{}, {} is indicating that they referred you to this bot. If this is true, please type 'confirm', else ignore this message".format(id.mention, ctx.message.author.mention))

        def check(m) -> bool:
            return m.content.lower() == "confirm" and m.channel == ctx.channel and m.author.id == id.id and m.author.id != ctx.message.author.id
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
            allreferredpeople = [int(j) for k in [i.split("~") for i in db.column(
                "SELECT referredids FROM referral") if i != "x"] for j in k]
            link = list(zip(db.column("SELECT * FROM referral"),
                        db.column("SELECT referredids FROM referral")))
            if (a := db.field("SELECT referred FROM referral WHERE UserID = ?", ctx.message.author.id)):
                a += 1
                db.execute(
                    "UPDATE referral SET referred = ? WHERE UserID = ?", a, ctx.message.author.id)
                referids = db.field(
                    "SELECT referredids FROM referral WHERE UserID = ?", ctx.message.author.id)
                referids = [i for i in referids.split("~") if i != "x" and i]
                if str(msg.author.id) not in referids and msg.author.id not in allreferredpeople:
                    referids.append(str(msg.author.id))
                elif msg.author.id in allreferredpeople:
                    for i in link:
                        if str(msg.author.id) in i[1]:
                            u = i[0]
                    await ctx.send("{} has already been referred by <@{}>".format(msg.author.mention, u))
                    return
                else:
                    await ctx.send("You've already referred {} before, nice try".format(msg.author.mention))
                    return
                referids = "~".join(referids)
                db.execute("UPDATE referral SET referredids = ? WHERE UserID = ?",
                           referids, ctx.message.author.id)
                db.commit()
            else:
                db.execute(
                    "INSERT OR IGNORE INTO referral (UserID) VALUES (?)", ctx.message.author.id)
                a = 1
                db.execute(
                    "UPDATE referral SET referred = ? WHERE UserID = ?", a, ctx.message.author.id)
                referids = db.field(
                    "SELECT referredids FROM referral WHERE UserID = ?", ctx.message.author.id)
                referids = [i for i in referids.split("~") if i != "x" and i]
                if str(msg.author.id) not in referids and msg.author.id not in allreferredpeople:
                    referids.append(str(msg.author.id))
                elif msg.author.id in allreferredpeople:
                    for i in link:
                        if str(msg.author.id) in i[1]:
                            u = i[0]
                    await ctx.send("{} has already been referred by <@{}>".format(msg.author.mention, u))
                    return
                else:
                    await ctx.send("You've already referred {} before, nice try".format(msg.author.mention))
                    return
                referids = "~".join(referids)
                db.execute("UPDATE referral SET referredids = ? WHERE UserID = ?",
                           referids, ctx.message.author.id)
                db.commit()
            await ctx.send("Confirmation received, updating database")
        except asyncio.TimeoutError:
            await ctx.send("{}, your referral time expired".format())

    def fix(self, tag) -> str:
        if tag[0] != '#':
            tag = '#'+tag
        tag = tag.upper()
        return tag

    @command(name='atag', help='$atag 2PP', brief='adds a tag to private databse')
    async def add_tag(self, ctx, tag):
        if ctx.message.author.id == self.god:
            tag = self.fix(tag)
            z = Account(tag)
            try:
                await z.get_data()
                name = z.name
                th = z.th
                if not name:
                    await ctx.send("Invalid tag")
                    return
                db.execute(
                    "INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
                db.execute(
                    'UPDATE Keychains SET Name = ? WHERE Tag = ?', name, tag)
                db.execute(
                    'UPDATE Keychains SET TownHall = ? WHERE Tag = ?', th, tag)
                db.commit()
                await ctx.send("I have added {} to your database".format(tag))
            except:
                await ctx.send("This tag is not valid or banned.")
        else:
            await self.givesafuck(ctx)

    @command(name='adevices', help='$adevices 2PP iPhone 4 iPad', brief='sets devices for a tag in database')
    async def add_devices(self, ctx, tag, *, devices):
        if ctx.message.author.id == self.god:
            tag = self.fix(tag)
            olddev = db.field(
                "SELECT Devices FROM Keychains WHERE Tag = ?", tag)
            if olddev:
                devices = (olddev + " " + devices).strip()
            db.execute("INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
            db.execute(
                'UPDATE Keychains SET Devices = ? WHERE Tag = ?', devices, tag)
            db.commit()
            await ctx.send("I have set {}'s devices to {}".format(tag, devices))
        else:
            await self.givesafuck(ctx)

    @command(name='alocal', help='$alocal US', brief='sets a local for a tag in database')
    async def add_local(self, ctx, tag, local):
        if ctx.message.author.id == self.god:
            tag = self.fix(tag)
            db.execute("INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
            db.execute(
                'UPDATE Keychains SET Local = ? WHERE Tag = ?', local, tag)
            db.commit()
            await ctx.send("I have set {}'s local to {}".format(tag, local))
        else:
            await self.givesafuck(ctx)

    @command(name='acreation', help='$acreation 2PP 2012-05-01', brief='sets creation for a tag in database')
    async def add_creation(self, ctx, tag, creation):
        if ctx.message.author.id == self.god:
            if '-' not in creation:
                await ctx.send("Invalid creation")
                return
            tag = self.fix(tag)
            db.execute("INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
            db.execute(
                'UPDATE Keychains SET CreationDate = ? WHERE Tag = ?', creation, tag)
            db.commit()
            await ctx.send("I have set {}'s creation date to {}".format(tag, creation))
        else:
            await self.givesafuck(ctx)

    @command(name='alastactive', help='$alastactive 2PP 2021-01-01', brief='sets last active for a tag in database')
    async def add_lastactive(self, ctx, tag, lastactive):
        if ctx.message.author.id == self.god:
            if '-' not in lastactive:
                await ctx.send("Invalid creation")
                return
            tag = self.fix(tag)
            db.execute("INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
            db.execute('UPDATE Keychains SET LastActive = ? WHERE Tag = ?',
                       lastactive, tag)
            db.commit()
            await ctx.send("I have set {}'s last active date to {}".format(tag, lastactive))
        else:
            await self.givesafuck(ctx)

    @command(name='areceipt', help='$areceipt 2PP', brief='sets receipt for a tag in database, upload receipt after using')
    async def add_receipt(self, ctx, tag):
        def check(reaction, user) -> bool:
            return str(reaction.emoji) == "✅" and reaction.message.channel == ctx.channel and not user.bot

        if ctx.message.author.id == self.god:
            tag = self.fix(tag)
            if f'{tag}.png' in os.listdir('Receipts'):
                filename = f'./Receipts/{tag}.png'
                db.execute(
                    "INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
                db.execute('UPDATE Keychains SET Receipt = ? WHERE Tag = ?',
                           filename, tag)
                db.commit()
                msg = await ctx.send(f'{filename} already exists in your database, would you like to update it? If so, send another receipt.')
                await msg.add_reaction('✅')
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
                except asyncio.TimeoutError:
                    return
                os.remove(filename)
                await ctx.invoke(self.bot.get_command('areceipt'), tag=tag)
            elif f'{tag}.jpg' in os.listdir('Receipts'):
                filename = f'./Receipts/{tag}.jpg'
                db.execute(
                    "INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
                db.execute('UPDATE Keychains SET Receipt = ? WHERE Tag = ?',
                           filename, tag)
                db.commit()
                msg = await ctx.send(f'{filename} already exists in your database, would you like to update it? If so, send another receipt.')
                await msg.add_reaction('✅')
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
                except asyncio.TimeoutError:
                    return
                os.remove(filename)
                await ctx.invoke(self.bot.get_command('add_receipt'), tag=tag)
            else:
                msg = await ctx.send(f'There is no receipt for {tag}, please upload one')

                def check(message) -> bool:
                    attachments = message.attachments
                    if len(attachments) == 0:
                        return False
                    attachment = attachments[0]
                    return attachment.filename.endswith(('.jpg', '.png')) and message.author.id == ctx.message.author.id
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=20.0)
                except asyncio.TimeoutError:
                    await ctx.send('Time expired')
                    return
                image = msg.attachments[0]
                filepath = ''
                async with aiohttp.ClientSession() as session:
                    url = image.url
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            filepath = './Receipts/{}.png'.format(tag)
                            f = await aiofiles.open(filepath, mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                if filepath:
                    db.execute(
                        "UPDATE Keychains SET Receipt = ? WHERE Tag = ?", filepath, tag)
                    db.commit()
                    await ctx.send("I have received your image and stored it in {}".format(filepath))
        else:
            await self.givesafuck(ctx)

    @command(name='aemail', help='$aemail 2PP n@gmail.com', brief='sets email for a tag in database')
    async def add_email(self, ctx, tag, email):
        if ctx.message.author.id == self.god:
            tag = self.fix(tag)
            db.execute("INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
            db.execute(
                'UPDATE Keychains SET Email = ? WHERE Tag = ?', email, tag)
            db.commit()
            await ctx.send("I have set {}'s email to {}".format(tag, email))
        else:
            await self.givesafuck(ctx)

    @command(name='anc', help='$anc 2PP 2012-05-01', brief='sets name change for a tag in database')
    async def add_nc(self, ctx, tag, *, namechanges):
        if ctx.message.author.id == self.god:
            tag = self.fix(tag)
            db.execute("INSERT OR IGNORE INTO Keychains (Tag) VALUES (?)", tag)
            ncs = db.field(
                "SELECT NameChanges FROM Keychains WHERE Tag = ?", tag)
            if ncs:
                ncs += "\u200b\n"+namechanges
            else:
                ncs = namechanges
            ncs = ' '.join(list(set(ncs.split("\u200b"))))
            db.execute(
                'UPDATE Keychains SET NameChanges = ? WHERE Tag = ?', ncs, tag)
            db.commit()
            await ctx.send("I have set {}'s name changes to {}".format(tag, ncs))
        else:
            await self.givesafuck(ctx)

    @command(name='kc', help='$kc 2PP', brief='gets kc for a tag from database')
    async def get_kc(self, ctx, tag):
        if ctx.message.author.id == self.god:
            s = time()
            tag = self.fix(tag)
            file = ''
            (a, b, c, d, e, f, g, h, i, j) = db.record(
                "SELECT * FROM Keychains WHERE Tag = ?", tag)
            z = Account(a)
            await z.get_data()
            if b.strip() != z.name:
                b = z.name
                db.execute(
                    'UPDATE Keychains SET Name = ? WHERE Tag = ?', z.name, tag)
            if int(c) != z.th:
                c = z.th
                db.execute(
                    'UPDATE Keychains SET TownHall = ? WHERE Tag = ?', z.th, tag)
            filej = './Receipts/{}.jpg'.format(tag)
            filep = './Receipts/{}.png'.format(tag)
            if isfile(filej) or isfile(filep) and h not in [filej, filep]:
                if isfile(filej):
                    db.execute("UPDATE Keychains SET Receipt = ? WHERE Tag = ?", filej, tag)
                elif isfile(filep):
                    db.execute("UPDATE Keychains SET Receipt = ? WHERE Tag = ?", filep, tag)
                else:
                    await ctx.send("error...file is {}".format())
            db.commit()
            if j:
                j = j.replace('\u200b', '')
            if a:
                embed = Embed(
                    title="{}'s Data".format(tag), color=random_hex(), timestamp=datetime.utcnow())
                embed.set_author(name="Queried by {}".format(
                    ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="**Tag:**",
                                value=f'**{a}**', inline=False)
                embed.add_field(name="**Name:**",
                                value=f'**{b}**', inline=False)
                embed.add_field(name="**Town Hall:**",
                                value=f'**{c}**', inline=False)
                embed.add_field(name="**Creation Date:**",
                                value=f'**{d}**', inline=False)
                embed.add_field(name="**Local:**",
                                value=f'**{e}**', inline=False)
                embed.add_field(name="**Devices:**",
                                value=f'**{f}**', inline=False)
                embed.add_field(name="**Last Active:**",
                                value=f'**{g}**', inline=False)
                embed.add_field(name="**Receipt:**",
                                value=f'**{h}**', inline=False)
                embed.add_field(name="**Email:**",
                                value=f'**{i}**', inline=False)
                embed.add_field(name='**Name Changes**:',
                                value=f'**{j}**', inline=False)
                if h != './Receipts/':
                    if isfile(h):
                        file = File(h)
                    else:
                        await ctx.send("There's a receipt path in the db but the receipt itself doesn't exist...")
                e = time()
                embed.set_footer(text='{:.2f} seconds • Made by Gulag#2001'.format(
                    e-s), icon_url=self.bot.get_cog("GodPerms").gods_url)
                if file:
                    await ctx.send(embed=embed, delete_after=20.0)
                    await ctx.send(file=file, delete_after=20.0)
                    return
                await ctx.send(embed=embed, delete_after=20.0)
            else:
                await ctx.send("No data for {} in your database".format(tag))
        else:
            await self.givesafuck(ctx)
    
    @command(name='adelete', help='$adelete 2PP', brief='deletes a tag from database, confirmation required')
    async def delete_db_tag(self, ctx, tag):

        def check(reaction, user) -> bool:
            return str(reaction.emoji) == "✅" and reaction.message.channel == ctx.channel and not user.bot

        if ctx.message.author.id == self.god:
            tag = self.fix(tag)
            msg = await ctx.send(f'Are you sure you want to delete {tag} from your database? React with a ✅ if so')
            await msg.add_reaction('✅')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
            except asyncio.TimeoutError:
                return
            db.execute("DELETE FROM Keychains WHERE Tag = ?", tag)
            db.commit()
            await ctx.send(f"I have deleted {tag} from your database.")
            
    @command(name='atags', help='$atags', brief='gets all tags in kc database')
    async def get_all_db_tags(self, ctx):
        if ctx.message.author.id == self.god:
            tags = db.column("SELECT * FROM Keychains")
            names = db.column("SELECT Name FROM Keychains")
            menu = MenuPages(source=HelpMenu(
                ctx, self.merge(tags, names)), delete_message_after=True, timeout=200.0)
            await menu.start(ctx)
    
    @command(name='giveall', help='$giveall @Buyer', brief='gives everyone a certain role')
    async def give_all_a_role(self, ctx, role: discord.Role):
        async for member in ctx.guild.fetch_members(limit=200):
            try:
                if not member.bot:
                    await member.add_roles(role)
                    print("Gave {} the default role".format(member.name))
            except Exception as e:
                print(repr(e))
        print("Done")
    
    @command(name='addagent', help='$addagent George V', brief='adds an agent to the Agent database')
    async def add_agent_to_db(self, ctx, *, agentname):
        if ctx.message.author.id == self.god:
            db.execute("INSERT OR IGNORE INTO Agents (Name) VALUES (?)", agentname)
            db.commit()
            await ctx.send("I added {} to the Agents database".format(agentname))
        else:
            await self.givesafuck(ctx)

def setup(bot):
    bot.add_cog(GodPerms(bot))
