import asyncio
import random
import string
from .A import *
from captcha.image import ImageCaptcha
from dateutil.parser import parse
from discord import Embed, File
from discord.ext.commands import BucketType, CheckFailure, cooldown, has_permissions, command, Cog
from discord.ext import menus
from discord.ext.menus import ListPageSource, MenuPages
from db import db
from html import unescape

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
            embed = Embed(title="**Menu**", description="**Agent Score Leaderboard**",
                        color=random_hex(), timestamp=datetime.utcnow())
            embed.set_author(name="Queried by {}".format(
                self.ctx.message.author.name), icon_url=self.ctx.message.author.avatar_url)
            embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
            embed.set_footer(
                text=f'Showing {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} agents', icon_url=self.gods_url)

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)
            return embed
        except Exception as e:
            print(repr(e))

    async def format_page(self, menu, entries):
        try:
            fields = []
            for entry in entries:
                fields.append((entry[0], "**"+str(entry[1])+" points**"))
            return await self.write_page(menu, fields)
        except Exception as e:
            print(repr(e))

class ForEveryone(Cog):  # coc commands
    def __init__(self, bot):
        self.bot = bot
        self.god = 1
        self.gods_url = f"https://cdn.discordapp.com/avatars/{self.god}/b0df2621a8f5b5155a561cca35a3e79e.webp?size=1024"
        self.godperms = [1, self.god]
        self.commands = [i for i in self.get_commands()]
        self.updatearr = []

    @tasks.loop(seconds=600)
    async def updatetags(self):
        self.updatearr = list(set(self.updatearr))
        if self.updatearr:
            await self.bot.stdout.send("Updating {} tags".format(len(self.updatearr)))
            await update(self.updatearr)
        self.updatearr = []

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("ForEveryone")
        self.updatetags.start()

    def is_godorperms():
        def predicate(ctx):
            return ctx.guild is not None and (ctx.author.id == 1 or ctx.author.guild_permissions.manage_messages)
        return commands.check(predicate)

    async def givesafuck(self, ctx):
        await ctx.send(file=File('pictures/givesafuck.jpg'))

    def isgod(self, ctx) -> bool:
        if ctx.message.author.id == self.god:
            return True
        return False

    def random_hex(self) -> int:
        return random.randint(0, 16777215)

    @command(help="$acc #2PP", brief="gets account info")
    @cooldown(1, 10, BucketType.user)
    async def acc(self, ctx, tag):
        if blacklisted(tag) and not self.isgod(ctx):
            await ctx.send("Tag is blacklisted", delete_after=5)
            return
        s = time()
        embed = Embed(title='Account Info', color=self.random_hex(),
                      timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        if tag == '':
            await ctx.send("Put a tag after $acc like $acc #2PP")
        else:
            try:
                # old embed.add_field(name='**{}**'.format(z.tag.upper()), value=f'**Name: {z.name} \nTH: {z.th} \nXP: {z.xp} \nWar Stars: {z.ws} \nBest :trophy:: {z.pb}\nClan: {z.clan} \nClan Tag: {z.clantag} \nBH: {z.bh}\n[CoS Link]({z.coslink})\n[CC Link]({z.cclink})\n[Open In Game]({z.openlink})**')
                z = Account(tag)
                await z.get_data()
                embed.add_field(name="**{}**".format(z.tag.upper()),
                                value=f"**Name: {z.name}\nTH: {z.th}\nXP: {z.xp}\n:star:: {z.ws}\n:trophy:: {z.cups}\nBest :trophy:: {z.pb}\n:sailboat:: {z.bh}\nClan: {z.clanname}\n**", inline=False)
                embed.add_field(
                    name="**Links**", value=f"**[CoS Link]({z.coslink})\n[CC Link]({z.cclink})\n[Open In Game]({z.openlink})**", inline=False)
                embed.set_thumbnail(url=z.leagueurl)
                self.updatearr.append(z)
                e = time()
                embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
                    e-s), icon_url=self.gods_url)
            except Exception as e:
                embed.add_field(name="**Pardon Nigga?**",
                                value="**Invalid/Banned Tag Retard**")
                e = time()
                embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
                    e-s), icon_url=self.gods_url)
                await ctx.send(embed=embed)
                return 0
            if z.hasclan:
                clanembed = Embed(
                    title="Clan Info", color=self.random_hex(), timestamp=datetime.utcnow())
                clanembed.set_author(name="Queried by {}".format(
                    ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
                if z.clanbadgeurl:
                    clanembed.set_image(url=z.clanbadgeurl)
                try:
                    clanembed.set_thumbnail(
                        url="https://flagcdn.com/256x192/{}.png".format(z.clancountrycode.lower()))
                except Exception as e:
                    pass
                if z._clandata.public_war_log:
                    clanembed.add_field(name="**{} - {}/50**".format(z.clantag.upper(), z._clandata.member_count),
                                        value=f'**Name: {z.clanname}\nLevel: {z.clanlevel}\nPrivacy: {z._clandata.type}\nWins: {z._clandata.war_wins}\nLosses: {z._clandata.war_losses}\nTies: {z._clandata.war_ties}\nStreak: {z._clandata.war_win_streak}\n**', inline=False)
                else:
                    clanembed.add_field(name="**{} - {}/50**".format(z.clantag.upper(), z._clandata.member_count),
                                        value=f'**Name: {z.clanname}\nLevel: {z.clanlevel}\nPrivacy: {z._clandata.type}\nWins: {z._clandata.war_wins}\nStreak: {z._clandata.war_win_streak}\n**', inline=False)
                clanembed.add_field(
                    name="**Description**", value="**__{}__**".format(z._clandata.description), inline=False)
                clanembed.add_field(
                    name="**Links**", value=f"**[CoS Link]({z.clancoslink})\n[CC Link]({z.clancclink})\n[Open In Game]({z.clanopenlink})**", inline=False)
                e = time()
                clanembed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
                    e-s), icon_url=self.gods_url)

            class MyMenu(menus.Menu):
                async def send_initial_message(self, ctx, channel):
                    return await channel.send(embed=embed)

                @menus.button('\U0001f1e8')
                async def on_c(self, payload):
                    await self.message.edit(embed=clanembed)

                @menus.button('\U0001f1e6')
                async def on_a(self, payload):
                    await self.message.edit(embed=embed)

                @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
                async def on_stop(self, payload):
                    self.stop()
                    await self.message.delete()

            try:
                clanembed
                m = MyMenu()
                await m.start(ctx)
            except:
                await ctx.send(embed=embed)

    @command(help="$othermems #2PP", brief='shows other clan members of a person', aliases=['Othermems'])
    @cooldown(1, 10, BucketType.user)
    async def othermems(self, ctx, arg):
        if blacklisted(arg) and ctx.message.author.id != self.god:
            await ctx.send("Tag is blacklisted")
            return
        if arg[0] == '#':
            arg = arg[1:]
        try:
            z = Account(arg)
            await z.get_data()
            zc = z.clanmembers
            await ctx.send('{}'.format(zc))
        except:
            try:
                z = Account(arg)
                await z.get_data()
                await ctx.send('{} is clanless'.format(z.name))
            except:
                await ctx.send('Invalid/Banned tag retard')

    @command(name='mems', help="$mems #2PP", brief='shows clan members', aliases=['Mems'])
    @cooldown(1, 10, BucketType.user)
    async def fetch_members(self, ctx, tag, limit: int = 9):
        s = time()
        bb = False
        embed = Embed(
            title="Members of Clan {}".format(tag.upper()), color=random_hex(), timestamp=datetime.utcnow())
        embed.set_author(name='Queried by {}'.format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        if tag[0] == '#':
            tag = tag[1:]
        try:
            z = Account(tag)
            await z.get_clan_data(tag, limit)
            if len(z.clanmembers) < 1000:
                embed.add_field(name="**Members:**",
                                value="**{}**".format(z.clanmembers))
                bb = True
            else:
                await ctx.send("Clan member list is too long, I will dm you the info instead.")
            e = time()
            embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
                e-s), icon_url=self.gods_url)
            if bb:
                await ctx.send(embed=embed)
            else:
                await ctx.author.send(z.clanmembers)
        except Exception as e:
            await ctx.send('Invalid clan retard')

    @command(name='yopmail', help="$yopmail example", brief="get yopmail codes lol", aliases=['yop'])
    @cooldown(1, 2, BucketType.guild)
    async def fetch_yopmail_emails(self, ctx, mail):
        idar = []
        godsserver = await self.bot.fetch_guild(1)
        gods2ndserver = await self.bot.fetch_guild(1)
        async for mem in godsserver.fetch_members(limit=1000):
            idar.append(mem.id)
        async for mem in gods2ndserver.fetch_members(limit=1000):
            idar.append(mem.id)
        if ctx.message.author.id in idar:
            s = time()
            embed = Embed(
                title="Emails for {}".format(mail), color=random_hex(), timestamp=datetime.utcnow())
            embed.set_author(name='Queried by {}'.format(
                ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            z = Yopmail(mail)
            emails = z.emails
            for i in z.emails:
                if " ".join(i.split("/")[1:]).strip() != "":
                    embed.add_field(name="{}".format(i.split(
                        "/")[0]), value="```{}```".format(" ".join(i.split("/")[1:]).strip()), inline=False)
            e = time()
            embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
                e-s), icon_url=self.gods_url)
            await ctx.send(embed=embed)

    @command(help="$version", brief="shows the version", aliases=['ver'])
    @cooldown(1, 10, BucketType.user)
    async def version(self, ctx):
        await ctx.send(self.bot.VERSION)

    @command(help="$prefix +", brief="change your server prefix", name="prefix")
    @cooldown(1, 10, BucketType.user)
    @commands.check_any(is_godorperms())
    async def prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("The prefix can't be more than 5 characters")
        else:
            db.execute(
                "UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            db.commit()
            await ctx.send(f'Prefix set to {new}.')

    @prefix.error
    async def prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need the Manage Messages permission to do that.")

    @command(help="$cap", brief="play a captcha game!", aliases=['cap'])
    @cooldown(1, 10, BucketType.channel)
    async def captcha(self, ctx):
        s = time()
        ltrs = string.ascii_letters + "123456789"
        cap = "".join(random.choice(ltrs) for i in range(random.randint(4, 6)))
        captch = ImageCaptcha(fonts=['ProductSans-Regular.ttf'])
        captch.write(cap, 'tmp/currentcaptcha.png')
        embed = Embed(title="Captcha", color=random_hex(),
                      timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="**Hello!**", value="{}, you are required to solve this captcha.\n**NOTE: It is case sensitive.**".format(
            ctx.message.author.mention), inline=False)
        file = File("tmp/currentcaptcha.png", filename='capt.png')
        embed.set_image(url="attachment://capt.png")
        e = time()
        embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)
        await ctx.send(file=file, embed=embed)

        def check(m) -> bool:
            return m.content.replace("0", "O").replace("C", "c").replace("V", "v").replace("W", "w").replace("O", "o").replace("S", "s").replace("Z", "z").replace("M", "m").replace("X", "x") == cap.replace("C", "c").replace("V", "v").replace("W", "w").replace("O", "o").replace("S", "s").replace("Z", "z").replace("M", "m").replace("X", "x'") \
                and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30.0)
            await ctx.send("Good job {}! You earned 1 point.".format(msg.author.mention))
            if (a := db.field("SELECT score FROM captcha WHERE UserID = ?", msg.author.id)):
                a += 1
                db.execute(
                    "UPDATE captcha SET score = ? WHERE UserID = ?", a, msg.author.id)
            else:
                a = 1
                db.execute(
                    "INSERT OR IGNORE INTO captcha (UserID) VALUES (?)", msg.author.id)
                db.execute(
                    "UPDATE captcha SET score = ? WHERE UserID = ?", a, msg.author.id)
            db.commit()
        except asyncio.TimeoutError:
            await ctx.send("Time expired. It was {}. Run $captcha again if you want".format(cap))

    @command(help="$hardcap", brief="play a hard captcha game!", aliases=['hardcap'])
    @cooldown(1, 10, BucketType.channel)
    async def hardcaptcha(self, ctx):
        s = time()
        ltrs = string.ascii_letters + "123456789"
        cap = "".join(random.choice(ltrs)
                      for i in range(random.randint(8, 10)))
        captch = ImageCaptcha(fonts=['ProductSans-Regular.ttf'])
        captch.write(cap, 'tmp/currentcaptcha.png')
        embed = Embed(title="Hard Captcha", color=random_hex(),
                      timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {} {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="**Hello!**", value="{}, you are required to solve this captcha.\n**NOTE: It is case sensitive.**".format(
            ctx.message.author.mention), inline=False)
        file = File("tmp/currentcaptcha.png", filename='capt.png')
        embed.set_image(url="attachment://capt.png")
        e = time()
        embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)
        await ctx.send(file=file, embed=embed)

        def check(m) -> bool:
            return m.content.replace("0", "O").replace("C", "c").replace("V", "v").replace("W", "w").replace("O", "o").replace("S", "s").replace("Z", "z").replace("M", "m").replace("X", "x'") == cap.replace("C", "c").replace("V", "v").replace("W", "w").replace("O", "o").replace("S", "s").replace("Z", "z").replace("M", "m").replace("X", "x'") \
                and m.channel == ctx.channel
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30.0)
            await ctx.send("Good job {}! You earned 3 points.".format(msg.author.mention))
            if (a := db.field("SELECT score FROM captcha WHERE UserID = ?", msg.author.id)):
                a += 3
                db.execute(
                    "UPDATE captcha SET score = ? WHERE UserID = ?", a, msg.author.id)
            else:
                a = 3
                db.execute(
                    "INSERT OR IGNORE INTO captcha (UserID) VALUES (?)", msg.author.id)
                db.execute(
                    "UPDATE captcha SET score = ? WHERE UserID = ?", a, msg.author.id)
            db.commit()
        except asyncio.TimeoutError:
            await ctx.send("Time expired. It was {}. Run $captcha again if you want".format(cap))

    @command(help="$score @God", brief="gets user score for all gamemodes")
    @cooldown(1, 10, BucketType.user)
    async def score(self, ctx, id: discord.User = None):
        if not id:
            id = ctx.message.author
        if type(id) == discord.User or type(id) == discord.Member:
            grabid = id.id
        else:
            grabid = id
        a = db.field("SELECT score FROM captcha WHERE UserID = ?", grabid)
        b = db.field("SELECT score FROM anagram WHERE UserID = ?", grabid)
        c = db.field("SELECT score FROM trivia WHERE UserID = ?", grabid)
        if not a:
            a = 0
        if not b:
            b = 0
        if not c:
            c = 0
        await ctx.send("**{}'s Stats:\nCaptcha Score: {}\nAnagram Score: {}\nTrivia Score: {}**".format(id.mention, a, b, c))
        return

    @command(help="$lb", brief="gets leaderboards for each game mode", aliases=['lb'])
    @cooldown(1, 10, BucketType.channel)
    async def leaderboard(self, ctx):
        s = time()

        a = db.records("SELECT * FROM captcha")
        b = sorted(a, key=lambda x: x[1], reverse=True)
        c = db.records("SELECT * FROM anagram")
        d = sorted(c, key=lambda x: x[1], reverse=True)
        e = db.records("SELECT * FROM trivia")
        f = sorted(e, key=lambda x: x[1], reverse=True)

        st2prnt = "\n".join(
            ["{}: <@{}> | {}".format(i+1, b[i][0], b[i][1]) for i in range(len(b[:10]))])
        st2prnt2 = "\n".join(
            ["{}: <@{}> | {}".format(i+1, d[i][0], d[i][1]) for i in range(len(d[:10]))])
        st2prnt3 = "\n".join(
            ["{}: <@{}> | {}".format(i+1, f[i][0], f[i][1]) for i in range(len(f[:10]))])
        captchaembed = Embed(
            title="Captcha Leaderboard", color=random_hex(), timestamp=datetime.utcnow())
        captchaembed.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        captchaembed.add_field(name="Name  |  Score    ",
                               value="**{}**".format(st2prnt))

        anagramembed = Embed(
            title="Anagram Leaderboard", color=random_hex(), timestamp=datetime.utcnow())
        anagramembed.set_author(name="Queried by {} {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        anagramembed.add_field(name="Name  |  Score    ",
                               value="**{}**".format(st2prnt2))

        triviaembed = Embed(
            title="Trivia Leaderboard", color=random_hex(), timestamp=datetime.utcnow())
        triviaembed.set_author(name="Queried by {} {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        triviaembed.add_field(name="Name  |  Score    ",
                              value="**{}**".format(st2prnt3))

        e = time()
        captchaembed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)
        anagramembed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)
        triviaembed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)

        class MyMenu(menus.Menu):
            async def send_initial_message(self, ctx, channel):
                return await channel.send(embed=captchaembed)

            @menus.button('\U0001f1e8')  # c
            async def on_c(self, payload):
                await self.message.edit(embed=captchaembed)

            @menus.button('\U0001f1e6')  # a
            async def on_a(self, payload):
                await self.message.edit(embed=anagramembed)

            @menus.button('\U0001f1f9')  # t
            async def on_t(self, payload):
                await self.message.edit(embed=triviaembed)

            @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
            async def on_stop(self, payload):
                self.stop()
                await self.message.delete()

        m = MyMenu()
        await m.start(ctx)

    @command(help="$anagram", brief="play an anagram game!", aliases=['ang'])
    @cooldown(1, 10, BucketType.channel)
    async def anagram(self, ctx):
        s = time()
        with open("30k.txt") as f:
            words = f.read().split("\n")[:-1]
        words = [i.strip() for i in words]
        word = random.choice(words)
        while True:
            w1 = list(word)
            random.shuffle(w1)
            shuffled = "".join(w1)
            if shuffled != word:
                break
        skore = max(int(len(word)/3), 1)
        embed = Embed(title="Anagram", color=random_hex(),
                      timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="**Hello!**", value="{}, you are required to solve this anagram.\nThe shuffled word is: **{}**".format(
            ctx.message.author.mention, shuffled), inline=False)
        e = time()
        embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)
        await ctx.send(embed=embed)

        def check(m) -> bool:
            return m.content.lower() == word and m.channel == ctx.channel
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30.0)
            await ctx.send("Good job {}! You earned {} points".format(msg.author.mention, skore))
            if (a := db.field("SELECT score FROM anagram WHERE UserID = ?", msg.author.id)):
                a += skore
                db.execute(
                    "UPDATE anagram SET score = ? WHERE UserID = ?", a, msg.author.id)
            else:
                a = skore
                db.execute(
                    "INSERT OR IGNORE INTO anagram (UserID) VALUES (?)", msg.author.id)
                db.execute(
                    "UPDATE anagram SET score = ? WHERE UserID = ?", a, msg.author.id)
            db.commit()
        except asyncio.TimeoutError:
            await ctx.send("Time expired. It was {}. Run $anagram again if you want".format(word))

    @command(help="$trivia", brief="play a trivia question!")
    @cooldown(1, 10, BucketType.user)
    async def trivia(self, ctx):
        s = time()
        req = requests.get(
            "https://opentdb.com/api.php?amount=1").json()['results'][0]
        category = req['category']
        difficulty = req['difficulty']
        question = req['question']
        _type = req['type']
        answer = unescape(req['correct_answer']).strip()
        wrong = req['incorrect_answers']
        if type(wrong) == list:
            lst = wrong + [answer]
            random.shuffle(lst)
            choices = "\n".join(lst)
        else:
            lst = [wrong] + [answer]
            random.shuffle(lst)
            choices = "\n".join(lst)
        choices = unescape(choices)
        question = unescape(question)
        embed = Embed(title="Trivia", color=random_hex(),
                      timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {}, Category: {}, Difficulty: {}".format(
            ctx.message.author.name, category, difficulty), icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="**{}**".format(question), value="{}\n**{}**".format(
            ctx.message.author.mention, choices), inline=False)
        e = time()
        embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)
        await ctx.send(embed=embed)

        def check(m) -> bool:
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=20.0)
            if msg.content.lower() != answer.lower():
                await ctx.send("{}, you suck! It was {}. Try another question with $trivia.".format(msg.author.mention, answer))
                return
            else:
                await ctx.send("Good job {}! You earned 1 point".format(msg.author.mention))
            if (a := db.field("SELECT score FROM trivia WHERE UserID = ?", msg.author.id)):
                a += 1
                db.execute(
                    "UPDATE trivia SET score = ? WHERE UserID = ?", a, msg.author.id)
            else:
                a = 1
                db.execute(
                    "INSERT OR IGNORE INTO trivia (UserID) VALUES (?)", msg.author.id)
                db.execute(
                    "UPDATE trivia SET score = ? WHERE UserID = ?", a, msg.author.id)
            db.commit()
        except asyncio.TimeoutError:
            await ctx.send("Time expired. It was {}. Run $trivia again if you want".format(answer))

    @command(help="$invite", brief="gets bot invite link", aliases=['invite'])
    async def link(self, ctx):
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=801558267284815892&permissions=8&scope=bot")
        return

    @command(help="$time", brief="shows time data for bot perms")
    @cooldown(1, 10, BucketType.user)
    async def time(self, ctx, usr: discord.User = ""):
        if not usr:
            usr = ctx.message.author
        s = time()
        embed = Embed(title="Time Left", color=random_hex(),
                      timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        if str(usr.id) not in (all1 := self.bot.get_cog("GodPerms").allperms):
            await ctx.send("You don't have any perms lmao")
            return
        startone = list(self.bot.get_cog(
            "GodPerms").rankperms[str(usr.id)].keys())[0]
        endone = self.bot.get_cog("GodPerms").rankperms[str(usr.id)][startone]
        if endone != None:
            deltaone = str(parse(endone) - datetime.now())
        else:
            deltaone = "Infinite"
        starttwo = list(self.bot.get_cog(
            "GodPerms").seasonperms[str(usr.id)].keys())[0]
        endtwo = self.bot.get_cog("GodPerms").rankperms[str(usr.id)][starttwo]
        if endtwo != None:
            deltatwo = str(parse(endtwo) - datetime.now())
        else:
            deltatwo = "Infinite"
        startthree = list(self.bot.get_cog(
            "GodPerms").genperms[str(usr.id)].keys())[0]
        endthree = self.bot.get_cog(
            "GodPerms").rankperms[str(usr.id)][startthree]
        if endthree != None:
            deltathree = str(parse(endthree) - datetime.now())
        else:
            deltathree = "Infinite"
        startfour = list(self.bot.get_cog(
            "GodPerms").cosperms[str(usr.id)].keys())[0]
        endfour = self.bot.get_cog(
            "GodPerms").rankperms[str(usr.id)][startfour]
        if endfour != None:
            deltafour = str(parse(endfour) - datetime.now())
        else:
            deltafour = "Infinite"
        embed.add_field(name="**{}'s Stats**".format(usr.name), value="**RankPerms: \n\tStart: {}\n\tEnd: {}\n\tRemaining: {}\n\nSeasonPerms: \n\tStart: {}\n\tEnd: {}\n\tRemaining: {}\n\nGenPerms: \n\tStart: {}\n\tEnd: {}\n\tRemaining: {}\n\nCosPerms: \n\tStart: {}\n\tEnd: {}\n\tRemaining: {}\n**".format(
            startone, endone, deltaone, starttwo, endtwo, deltatwo, startthree, endthree, deltathree, startfour, endfour, deltafour), inline=False)
        e = time()
        embed.set_footer(text="{:.2f} seconds • Made by Gulag#2001".format(
            e-s), icon_url=self.gods_url)
        await ctx.send(embed=embed)

    @command(name='check')
    @cooldown(1, 10, BucketType.channel)
    async def repcheck(self, ctx, usr=""):
        s = time()
        img = "https://repcord.io/logo.png"
        if not usr:
            usr = str(ctx.message.author.id)
        if "<@!" in usr:
            usr = usr.split("<@!")[1][:-1]
        elif "<@" in usr:
            usr = usr.split("<@")[1][:-1]
        received, given = ("https://api.repcord.io/api/user/retrieved/{}".format(
            usr), "https://api.repcord.io/api/user/given/{}".format(usr))
        async with aiohttp.ClientSession() as session1:
            async with session1.get(received) as respreceived:
                htmlreceived = await respreceived.text()
        async with aiohttp.ClientSession() as session2:
            async with session2.get(given) as respgiven:
                htmlgiven = await respgiven.text()
        datareceived = json.loads(htmlreceived)['data']
        datagiven = json.loads(htmlgiven)['data']
        embedreceived = Embed(
            title="Repcord Stats (Received)", color=random_hex(), timestamp=datetime.now())
        embedgiven = Embed(
            title="Repcord Stats (Given)", color=random_hex(), timestamp=datetime.now())
        embedreceived.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        embedgiven.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        embedreceived.set_thumbnail(url=img)
        embedgiven.set_thumbnail(url=img)
        for rep in datareceived[:10]:
            nam = "Timestamp: {}".format(rep['timestamp'])
            val = "<@{}> said {}".format(rep['userid'], rep['comment'])
            embedreceived.add_field(name=nam, value=val, inline=False)
        for rep in datagiven[:10]:
            nam = "Timestamp: {}".format(rep['timestamp'])
            val = "<@{}> said {}".format(rep['userid'], rep['comment'])
            embedgiven.add_field(name=nam, value=val, inline=False)
        e = time()
        embedreceived.set_footer(
            text="{:.2f} seconds".format(e-s), icon_url=self.gods_url)
        embedgiven.set_footer(text="{:.2f} seconds".format(
            e-s), icon_url=self.gods_url)

        class MyMenu(menus.Menu):
            async def send_initial_message(self, ctx, channel):
                return await channel.send(embed=embedreceived)

            @menus.button('\U0001f1f7')
            async def on_r(self, payload):
                await self.message.edit(embed=embedreceived)

            @menus.button('\U0001f1ec')
            async def on_g(self, payload):
                await self.message.edit(embed=embedgiven)

            @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
            async def on_stop(self, payload):
                self.stop()
                await self.message.delete()

        m = MyMenu()
        await m.start(ctx)

    @command(name='typeracer', help="$typeracer", brief='starts a type racing game w/ your friends')
    @cooldown(1, 10, BucketType.user)
    async def typeracer_game(self, ctx):
        msg = await ctx.send("A typeracer game has begun! Please react if you want to join in! (Max of 5 racers allowed)")
        await msg.add_reaction('✅')
        usrarr = []

        def check(reaction, user) -> bool:
            return str(reaction.emoji) == "✅" and reaction.message.channel == ctx.channel and not user.bot and user not in usrarr

        def check2(m) -> bool:
            if m.author in usrarr and m.content.strip() == paragraph or m.content.strip() == encrypted:
                usrarr.remove(m.author)
                return True

        def wpm(char):
            return char*((60/(time()-s))/5)

        try:
            _, user1 = await self.bot.wait_for("reaction_add", check=check, timeout=15.0)
            usrarr.append(user1)
            _, user2 = await self.bot.wait_for("reaction_add", check=check, timeout=15.0)
            usrarr.append(user2)
            _, user3 = await self.bot.wait_for("reaction_add", check=check, timeout=15.0)
            usrarr.append(user3)
            _, user4 = await self.bot.wait_for("reaction_add", check=check, timeout=15.0)
            usrarr.append(user4)
            _, user5 = await self.bot.wait_for("reaction_add", check=check, timeout=15.0)
            usrarr.append(user5)
        except asyncio.TimeoutError:
            pass

        await ctx.send('The race will begin soon! The racers are {}'.format(", ".join(usr.mention for usr in usrarr)))
        url = "http://metaphorpsum.com/paragraphs/1/{}".format(
            random.randint(2, 3))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                paragraph = await response.text()
        characters = len(paragraph)
        encrypted = paragraph.replace(" ", " \u200b")
        codeblock = f"```{encrypted}```"
        await ctx.send("Ready..Set..GO! Here is what you must type:\n{}".format(codeblock))
        s = time()

        try:
            msg1 = await self.bot.wait_for('message', check=check2, timeout=120.0)
            if msg1.content.strip() == encrypted:
                await msg1.channel.send("You're a bitch for trying to copy the message, you're disqualified lmao.")
            else:
                await ctx.send("{} finished with an average wpm of {:.2f}".format(msg1.author.mention, wpm(characters)))
            await msg1.delete()
            msg2 = await self.bot.wait_for('message', check=check2, timeout=120.0)
            if msg2.content.strip() == encrypted:
                await msg2.channel.send("You're a bitch for trying to copy the message, you're disqualified lmao.")
            else:
                await ctx.send("{} finished with an average wpm of {:.2f}".format(msg2.author.mention, wpm(characters)))
            await msg2.delete()
            msg3 = await self.bot.wait_for('message', check=check2, timeout=120.0)
            if msg3.content.strip() == encrypted:
                await msg3.channel.send("You're a bitch for trying to copy the message, you're disqualified lmao.")
            else:
                await ctx.send("{} finished with an average wpm of {:.2f}".format(msg3.author.mention, wpm(characters)))
            await msg3.delete()
            msg4 = await self.bot.wait_for('message', check=check2, timeout=120.0)
            if msg4.content.strip() == encrypted:
                await msg4.channel.send("You're a bitch for trying to copy the message, you're disqualified lmao.")
            else:
                await ctx.send("{} finished with an average wpm of {:.2f}".format(msg4.author.mention, wpm(characters)))
            await msg4.delete()
            msg5 = await self.bot.wait_for('message', check=check2, timeout=120.0)
            if msg5.content.strip() == encrypted:
                await msg5.channel.send("You're a bitch for trying to copy the message, you're disqualified lmao.")
            else:
                await ctx.send("{} finished with an average wpm of {:.2f}".format(msg5.author.mention, wpm(characters)))
            await msg5.delete()

        except asyncio.TimeoutError:
            pass
        await ctx.send("The race is over!")

    @command(name='rep', help='$rep George V', brief='reps an agent from sc')
    async def rep_agent(self, ctx, *, agentname):
        if ctx.guild.id == 1:
            if type(a := db.field("SELECT Score FROM Agents WHERE Name = ?", agentname)) == int:
                repped = db.field(
                    "SELECT Repped FROM Agents WHERE Name = ?", agentname)
                repped = [i for i in repped.split("~") if i]
                negged = db.field(
                    "SELECT Negged FROM Agents WHERE Name = ?", agentname)
                negged = [i for i in negged.split("~") if i]
                if str(ctx.message.author.id) in repped:
                    await ctx.send("You've already repped {} idiot.".format(agentname))
                    return
                elif str(ctx.message.author.id) in negged:
                    await ctx.send("You negged this agent before, updating your neg to a rep...")
                    a += 1
                    negged.remove(str(ctx.message.author.id))
                    negged = "~".join(repped)
                    db.execute(
                        "UPDATE Agents SET Negged = ? WHERE Name = ?", negged, agentname)
                a += 1
                db.execute(
                    "UPDATE Agents SET Score = ? WHERE Name = ?", a, agentname)
                repped.append(str(ctx.message.author.id))
                repped = "~".join(repped)
                db.execute("UPDATE Agents SET Repped = ? WHERE Name = ?",
                           repped, agentname)
                db.commit()
                await ctx.send("You repped {} for 1 point.".format(agentname))
            else:
                await ctx.send("Invalid agent, ask Unk to add them if they're not in the database yet")
                return
        else:
            await self.givesafuck(ctx)

    @command(name='neg', help='$neg George V', brief='negs an agent from sc')
    async def neg_agent(self, ctx, *, agentname):
        if ctx.guild.id == 1:
            if type(a := db.field("SELECT Score FROM Agents WHERE Name = ?", agentname)) == int:
                repped = db.field(
                    "SELECT Repped FROM Agents WHERE Name = ?", agentname)
                repped = [i for i in repped.split("~") if i]
                negged = db.field(
                    "SELECT Negged FROM Agents WHERE Name = ?", agentname)
                negged = [i for i in negged.split("~") if i]
                if str(ctx.message.author.id) in negged:
                    await ctx.send("You've already negged {} idiot.".format(agentname))
                    return
                elif str(ctx.message.author.id) in repped:
                    await ctx.send("You repped this agent before, updating your rep to a neg...")
                    a -= 1
                    repped.remove(str(ctx.message.author.id))
                    repped = "~".join(repped)
                    db.execute(
                        "UPDATE Agents SET Repped = ? WHERE Name = ?", repped, agentname)
                a -= 1
                db.execute(
                    "UPDATE Agents SET Score = ? WHERE Name = ?", a, agentname)
                negged.append(str(ctx.message.author.id))
                negged = "~".join(negged)
                db.execute("UPDATE Agents SET Negged = ? WHERE Name = ?",
                           negged, agentname)
                db.commit()
                await ctx.send("You negged {} for 1 point.".format(agentname))
            else:
                await ctx.send("Invalid agent, ask Unk to add them if they're not in the database yet")
                return
        else:
            await self.givesafuck(ctx)

    @command(name='agent', help='$agent George V', brief='checks an agents score')
    async def get_agent_score(self, ctx, *, agentname):
        if ctx.guild.id == 1:
            if (a := db.record("SELECT * FROM Agents WHERE Name = ?", agentname)):
                await ctx.send("{} has a score of {} points".format(a[0], a[1]))
            else:
                await ctx.send("Invalid agent, ask Unk to add them if they're not in the database yet")
                return
        else:
            await self.givesafuck(ctx)

    @command(name='agents', help='$agents', brief='shows all agent scores')
    async def get_agents_scores(self, ctx):
        if ctx.guild.id == 1:
            merged = db.records("SELECT * FROM Agents")
            merged = sorted(merged, key=lambda x: x[1], reverse=True)
            menu = MenuPages(source=HelpMenu(
                ctx, merged), delete_message_after=True, timeout=200.0)
            await menu.start(ctx)
        else:
            await self.givesafuck(ctx)


def setup(bot):
    bot.add_cog(ForEveryone(bot))
