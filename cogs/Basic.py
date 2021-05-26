from discord import Embed, File, Object
from discord.ext.commands import BucketType, Cog, Greedy, check, command, cooldown
from .A import *
from db import db

class Basic(Cog):  # not clash related, can delete if not needed...
    def __init__(self, bot):
        self.bot = bot
        self.god = 1
        self.gods_url = f"https://cdn.discordapp.com/avatars/{self.god}/b0df2621a8f5b5155a561cca35a3e79e.webp?size=1024"
        self.godperms = [1, self.god]
        self.commands = [i for i in self.get_commands()]

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Basic")
    
    def is_godorperms():
        def predicate(ctx):
            return ctx.guild is not None and (ctx.author.id == 1 or ctx.author.guild_permissions.manage_guild)
        return check(predicate)

    async def givesafuck(self, ctx):
        await ctx.send(file=File('pictures/givesafuck.jpg'))

    @command(help='$hello you are Recruit', brief="says hello")
    @cooldown(1, 10, BucketType.user)
    async def hello(self, ctx, *args):
        arg = ''
        for j in args:
            arg += j+" "
        arg = arg.replace("@everyone", '`@everyone`').replace("@here", '`@here`')
        await ctx.send(f'Hello <@{ctx.author.id}>, {arg}')

    @command(help="$beggar", brief="shows a beggar lol")
    @cooldown(1, 10, BucketType.user)
    async def beggar(self, ctx):
        await ctx.send(file=File('videos/beggar.mov'))

    @command(help="$biggerloser", brief="shows a biggerloser lol")
    @cooldown(1, 10, BucketType.user)
    async def biggerloser(self, ctx):
        await ctx.send(file=File('pictures/biggerloser.jpg'))

    @command(help="$bird", brief="shows a bird lol", aliases=['eagle'])
    @cooldown(1, 10, BucketType.user)
    async def bird(self, ctx):
        await ctx.send(file=File('pictures/bird.jpg'))

    @command(help="$loser", brief="shows a loser lol")
    @cooldown(1, 10, BucketType.user)
    async def loser(self, ctx):
        await ctx.send(file=File('pictures/loser.jpg'))

    @command(help="$pussyslayer", brief='shows a pussyslayer lol')
    @cooldown(1, 10, BucketType.user)
    async def pussyslayer(self, ctx):
        await ctx.send(file=File('pictures/pussyslayer.jpg'))

    @command(help="$virgin", brief='shows a virgin lol')
    @cooldown(1, 10, BucketType.user)
    async def virgin(self, ctx):
        await ctx.send(file=File('pictures/virgin.jpg'))

    @command(help="$gayretard", brief="shows a gay retard lol")
    @cooldown(1, 10, BucketType.user)
    async def gayretard(self, ctx):
        await ctx.send(file=File('pictures/gayretard.jpg'))

    @command(help="$pardonn", brief="pardon nigga?")
    @cooldown(1, 10, BucketType.user)
    async def pardonn(self, ctx):
        await ctx.send(file=File("videos/pardonnigga.mov"))

    @command(help="$ear", brief="shows ears lol")
    @cooldown(1, 10, BucketType.user)
    async def ear(self, ctx):
        await ctx.send(file=File("videos/ear.gif"))

    @command(help="$stfu", brief="stfu")
    @cooldown(1, 10, BucketType.user)
    async def stfu(self, ctx):
        if (n := random.randint(0, 1)):
            await ctx.send(file=File("videos/stfu.mov"))
        else: 
            await ctx.send(file=File("pictures/stfu2.jpg"))

    @command(help="$sorry", brief="sorry lol")
    @cooldown(1, 10, BucketType.user)
    async def sorry(self, ctx):
        await ctx.send(file=File("videos/sorry.mov"))
    
    @command(help="$ripbozo", brief="rip bozo lol", aliases=['bozo', 'rip'])
    @cooldown(1, 10, BucketType.user)
    async def ripbozo(self, ctx):
        await ctx.send(file=File("videos/ripbozo.mp4"))

    @command(help="$downbad 5", brief="shows someone down bad lol")
    @cooldown(1, 10, BucketType.user)
    async def downbad(self, ctx):
        await ctx.send(content="<@684110707197083656>\n", file=File("pictures/downbad.jpg"))

    @command(help="$shitburners", brief="shows who makes shit burners lol")
    @cooldown(1, 10, BucketType.user)
    async def shitburners(self, ctx):
        await ctx.send(content="<@684110707197083656>\n", file=File("pictures/shitburners.jpg"))

    @command(help="$fonem", brief="ON FONEM!!", aliases=['blood', 'crip', 'gang', 'cuh', 'onbaby', 'foenem', 'folksnem'])
    @cooldown(1, 10, BucketType.user)
    async def fonem(self, ctx):
        await ctx.send(content="ON CRIP ON GANG ON BLOOD ON CUH ON FOENEM", file=File("pictures/ON.jpg"))

    @command(help="$quote", brief='sends a random quote')
    @cooldown(1, 10, BucketType.user)
    async def quote(self, ctx):
        await ctx.send(f'{get_quote()}')

    @command(help="$ping", brief="ping!", aliases=['pong'])
    @cooldown(1, 10, BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f"**Pong! Latency: {round(self.bot.latency*1000)}ms**")

    @command(help="$when 1", brief="gets when a discord ID was made")
    @cooldown(1, 10, BucketType.user)
    async def when(self, ctx, id:int):
        if type(id) != int:
            try:
                id = id.split("<@!")[1][:-1]
            except:
                await ctx.send("Nigger use a valid type")
                return
        await ctx.send(Object(id).created_at.strftime("%m/%d/%Y %I:%M:%S %p UTC"))

    @command(help="$clr 10 @God", brief="clears messages")
    @cooldown(1, 10, BucketType.user)
    async def clr(self, ctx, amount: int, member: discord.Member = None):
        await ctx.message.delete()
        msg = []
        if ctx.message.author.id in self.godperms:
            if not member:
                await ctx.channel.purge(limit=amount)
            else:
                async for m in ctx.channel.history():
                    if len(msg) == amount:
                        break
                    elif m.author == member:
                        msg.append(m)
                await ctx.channel.delete_message(msg)
        else:
            await self.givesafuck(ctx)

    @command(help="$pp @God", brief="gets the profile pic of a user", aliases=['av'])
    @cooldown(1, 10, BucketType.user)
    async def pp(self, ctx, user: discord.User):
        await ctx.send(user.avatar_url)

    @command(help="$memory", brief="shows my system memory stats")
    @cooldown(1, 10, BucketType.user)
    async def memory(self, ctx):
        s = time()
        embed = Embed(title="Memory Stats", color=random_hex(), timestamp=datetime.utcnow())
        embed.set_author(name='Queried by {}'.format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        a = psutil.virtual_memory()
        total = a[0]*10**9/2**30/1000000000
        free = a[1]*10**9/2**30/1000000000
        used = a[3]*10**9/2**30/1000000000
        percent = a[2]
        embed.add_field(name="**{}% used**".format(percent),
                        value="**Total Memory: {:.2f} GB\nUsed Memory: {:.2f} GB\nFree Memory: {:.2f} GB\n**".format(total, used, free))
        e = time()
        embed.set_footer(text='{:.2f} seconds • Made by Gulag#2001'.format(
            e-s), icon_url=self.gods_url)
        await ctx.send(embed=embed)

    @command(help="$kick @Retard", brief="kicks someone")
    @cooldown(1, 10, BucketType.user)
    @commands.check_any(is_godorperms())
    async def kick(self, ctx, mems: Greedy[discord.Member], *, reason=''):
        await ctx.message.delete()
        for mem in mems:
            if mem.id == self.god:
                continue
            await mem.kick(reason=reason)
        kicked = ", ".join(x.name for x in mems)
        await ctx.send("Kicked {}".format(kicked))
    
    @command(pass_context=True, help="$ban @Retard", brief="bans someone")
    @cooldown(1, 10, BucketType.user)
    @commands.check_any(is_godorperms())
    async def ban(self, ctx, mems: Greedy[discord.Member], *, reason=''):
        await ctx.message.delete()
        for mem in mems:
            if mem.id == self.god:
                continue
            await mem.ban(reason=reason)
        banned = ", ".join(x.name for x in mems)
        await ctx.send("Banned {}".format(banned))
    
    @command(pass_context=True, help="$ban @Retard", brief="bans someone")
    @cooldown(1, 10, BucketType.user)
    @commands.check_any(is_godorperms())
    async def unban(self, ctx, mems: Greedy[discord.Member], *, reason=''):
        await ctx.message.delete()
        for mem in mems:
            if mem.id == self.god:
                continue
            await mem.unban(reason=reason)
        unbanned = ", ".join(x.name for x in mems)
        await ctx.send("Unbanned {}".format(unbanned))

    @command(name='retard', help="$retard 5", brief="shows a retard")
    @cooldown(1, 30, BucketType.channel)
    async def show_retard(self, ctx, nums: int):
        if ctx.message.author.id != 781296929602404362:
            if nums > 5:
                await ctx.send("Limit is 5 idiot.")
            else:
                name = "<@1>\n"
                name *= nums
                await ctx.send(content=name)
                for i in range(nums):
                    await ctx.send(file=File('pictures/retard.png'))

    @command(help="$tylenol", brief='Zeke\'s bitch')
    @cooldown(1, 10, BucketType.user)
    async def tylenol(self, ctx):
        if ctx.message.author.id in [1, 1]:
            await ctx.send('Tasty!')
        else:
            await ctx.send('Not for you nigger')

    @command(name='god', help="$god", brief='tells you who God is', aliases=['God'])
    @cooldown(1, 10, BucketType.user)
    async def saygod(self, ctx):
        await ctx.send("Gulag_Recroot#6800 aka Unk")

    @command(help="$randomkc", brief="sends a random kc")
    @cooldown(1, 10, BucketType.user)
    async def randomkc(self, ctx):
        if ctx.message.author.id != 1:
            await ctx.send(fakekc())
        else:
            await self.givesafuck(ctx)

    @command(help="$dead #2PP", brief="shows if a tag is dead or not")
    @cooldown(1, 10, BucketType.user)
    async def dead(self, ctx, tag):
        tag = await Account(tag).get_data()
        await ctx.send(tag.dead)

    @command(help="$boat #2PP", brief="shows builder hall info")
    @cooldown(1, 10, BucketType.user)
    async def boat(self, ctx, tag):
        await ctx.send(Account(tag).bh)

    @command(help="$countries A", brief="gets country code", aliases=['country'])
    @cooldown(1, 10, BucketType.user)
    async def countries(self, ctx, arg):
        s = time()
        embed = Embed(
            title='Country Codes - Country', color=random_hex(), timestamp=datetime.utcnow())
        embed.set_author(name='Queried by {}'.format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        with open('jsondata/countries.json') as f:
            countries = json.load(f)
        if type(arg) == str and len(arg) == 1:
            for i in countries.keys():
                if i[0] == arg:
                    embed.add_field(name='{}'.format(
                        i), value='{}'.format(countries[i]), inline=False)
        elif type(arg) == str and len(arg) == 2:
            embed.add_field(name='{}'.format(arg), value='{}'.format(
                countries[arg]), inline=False)
        e = time()
        embed.set_footer(text='{:.2f} seconds • Made by Gulag#2001'.format(
            e-s), icon_url=self.gods_url)
        await ctx.send(embed=embed, delete_after=30.0)

    @command(help="$currencies US", brief="gets currency symbols from a starting letter", aliases=['currency'])
    @cooldown(1, 10, BucketType.user)
    async def currencies(self, ctx, arg):
        s = time()
        embed = Embed(
            title='Country Codes - Country', color=random_hex(), timestamp=datetime.utcnow())
        embed.set_author(name='Queried by {}'.format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        with open('jsondata/currencies.json', encoding='utf-8') as f:
            data = json.load(f)
        if len(arg) == 1:
            for i in data.keys():
                if i[0] == arg:
                    embed.add_field(name='{}'.format(i), value='{} - {} - {}'.format(
                        data[i]['name'], data[i]['symbol'], data[i]['symbol_native']), inline=False)
        if len(arg) == 3:
            embed.add_field(name='{}'.format(arg), value='{} - {} - {}'.format(
                data[arg]['name'], data[arg]['symbol'], data[arg]['symbol_native']), inline=False)
        e = time()
        embed.set_footer(text='{:.2f} seconds • Made by Gulag#2001'.format(
            e-s), icon_url=self.gods_url)
        await ctx.send(embed=embed, delete_after=30.0)

    @command(help="$butter", brief="butter lol")
    @cooldown(1, 30, BucketType.channel)
    async def butter(self, ctx):
        await ctx.send('''<@1>
    <@1>
    <@1>
    <@1>
    <@1>
    <@1>
    <@1>
    <@1>
    <@1>
    <@1>
            ''', file=File('pictures/butter.jpg'))

    @command(help="$bitch", brief="bitch lol")
    @cooldown(1, 30, BucketType.channel)
    async def bitch(self, ctx):
        await ctx.send('''Fuck you bitch ass, pussy ass nigga
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
    Pussy ass nigga, dumb ass, bitch ass, idiotic ass nigga
    Stupid, dumb, goofy, remedial, ug- idiotic ass nigga
    Goofy ass boy
    Fuck you, nigga''')

    @command(help="$oldest 3", brief="shows oldest user by rank")
    @cooldown(5, 10, BucketType.user)
    async def oldest(self, ctx, num: int, limit=1000):
        oldest = 100000000000000000000000
        agearr = []
        async for mem in ctx.guild.fetch_members(limit=limit):
            if mem.id < oldest:
                oldest = mem.id
            agearr.append(mem.id)
        agearr.sort()
        def ordinal(n) -> str: return "%d%s" % (
            n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])
        await ctx.send("{} Oldest user here is <@{}>, made on {}".format(ordinal(num), agearr[num-1], Object(agearr[num-1]).created_at.strftime("%m/%d/%Y %I:%M %p UTC")))

    @command(help="$youngest 3", brief="opposite of oldest")
    @cooldown(5, 10, BucketType.user)
    async def youngest(self, ctx, num: int = None, limit=1000):
        youngest = 0
        agearr = []
        async for mem in ctx.guild.fetch_members(limit=limit):
            if mem.id > youngest:
                youngest = mem.id
            agearr.append(mem.id)
        agearr.sort(reverse=True)
        def ordinal(n) -> str: return "%d%s" % (
            n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])
        await ctx.send("{} Youngest user here is <@{}>, made on {}".format(ordinal(num), agearr[num-1], Object(agearr[num-1]).created_at.strftime("%m/%d/%Y %I:%M %p UTC")))

    @command(help="$xp 202", brief="calculates xp for the next lvl")
    @cooldown(1, 10, BucketType.user)
    async def xp(self, ctx, lvl):
        try:
            lvl = int(lvl)
            if lvl <= 200:
                await ctx.send(f'It takes {(lvl-1)*50:,} xp to go from lvl {lvl} to lvl {lvl+1}')
            elif lvl < 300 and lvl > 200:
                await ctx.send(f'It takes {(lvl-200)*500+9500:,} xp to go from lvl {lvl} to lvl {lvl+1}')
            elif lvl > 300:
                await ctx.send(f'It takes {(lvl-300)*1000+60000:,} xp to go from lvl {lvl} to lvl {lvl+1}')
        except:
            await ctx.send("Use a number retard")

    @command(help="$totalxp 202", brief="calculates cumulative xp")
    @cooldown(1, 10, BucketType.user)
    async def totalxp(self, ctx, lvl):
        try:
            lvl = int(lvl)
            if lvl <= 201:
                await ctx.send(f'It takes {(lvl-1)*(lvl-2)*25+30:,} xp cumulatively to get to lvl {lvl}')
            elif lvl >= 202 and lvl <= 299:
                await ctx.send(f'It takes {250*((lvl-200)**2)+9250*(lvl-200)+985530:,} xp cumulatively to get to lvl {lvl}')
            elif lvl > 299:
                await ctx.send(f'It takes {500*((lvl-300)**2)+59500*(lvl-300)+4410530:,} xp cumulatively to get to lvl {lvl}')
        except:
            await ctx.send("Use a number retard")

    @command(help="$nigger", brief='tells you who a nigger is lol')
    async def nigger(self, ctx):
        await ctx.send(f'<@{ctx.message.author.id}> is a nigger')

    @command(name='log', help="$log", brief='changes logging mode, default is off')
    @cooldown(1, 10, BucketType.user)
    @commands.check_any(is_godorperms())
    async def change_log_mode(self, ctx):
        logmode = db.field("SELECT Logging FROM guilds WHERE GuildID = ?", ctx.message.guild.id)
        logmode ^= 1
        db.execute("UPDATE guilds SET Logging = ? WHERE GuildID = ?", logmode, ctx.guild.id)
        db.commit()
        if logmode:
            await ctx.send("Your logging is now on.")
        else:
            await ctx.send("Your logging is now off.")
    
    @command(name='snipe', help='$snipe', brief='gets the last deleted message')
    @cooldown(1, 10, BucketType.user)
    @commands.check_any(is_godorperms())
    async def get_last_message(self, ctx):
        last_m = db.field("SELECT Snipe FROM guilds WHERE GuildID = ?", ctx.message.guild.id)
        await ctx.send("<:4k:838988581362991174>")
        await ctx.send(f"{last_m}")
    
    @command(name='editsnipe', help='$editsnipe', brief='gets the last edited message')
    @cooldown(1, 10, BucketType.user)
    @commands.check_any(is_godorperms())
    async def get_last_edit(self, ctx):
        last_e = db.field("SELECT Editsnipe FROM guilds WHERE GuildID = ?", ctx.message.guild.id)
        await ctx.send("<:4k:838988581362991174>")
        await ctx.send(f'{last_e}')

def setup(bot):
    bot.add_cog(Basic(bot))
