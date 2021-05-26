from .A import *
from dateutil.parser import parse
from discord import Embed
from discord.ext.commands import BucketType, Cog, command, cooldown
from discord.ext.menus import MenuPages, ListPageSource
from typing import List, Optional


def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []
    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f'[{key}]' if "=" in str(value)
                          or "NoneType" in str(value) else f'<{key}>')
    params = " ".join(params)
    return f"```${cmd_and_aliases} {params}```"


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        super().__init__(data, per_page=5)
        self.god = 1
        self.gods_url = f"https://cdn.discordapp.com/avatars/{self.god}/b0df2621a8f5b5155a561cca35a3e79e.webp?size=1024"

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)
        embed = Embed(title="**Help**", description="**Welcome to the help dialog!\n\nFor more info on a specific command, \
                        run $help <commandname>\n\nUse the buttons at the bottom to navigate this page\n--------------------\n**",
                      color=random_hex(), timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {}".format(
            self.ctx.message.author.name), icon_url=self.ctx.message.author.avatar_url)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f'Showing {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands you can use • Made by Gulag#2001', icon_url=self.gods_url)

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []
        
        for entry in entries:
            fields.append((entry.brief or "No description", syntax(entry)))

        return await self.write_page(menu, fields)


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        with open('jsondata/perms.json') as f:
            data = json.load(f)
        self.rankperms = data['rankperms']
        self.seasonperms = data['seasonperms']
        self.genperms = data['genperms']
        self.cosperms = data['cosperms']
        self.allperms = list(set(list(self.rankperms.keys(
        )) + list(self.seasonperms.keys()) + list(self.genperms.keys()) + list(self.cosperms.keys())))
        self.god = 1
        self.godperms = self.bot.get_cog("GodPerms").godperms
        self.gods_url = f"https://cdn.discordapp.com/avatars/{self.god}/b0df2621a8f5b5155a561cca35a3e79e.webp?size=1024"

    def not_expired(self, type, id) -> bool:
        currperm = self.rankperms
        if str(id) not in currperm:
            return False
        if type == 1:
            currperm = self.rankperms
            usrend = currperm[str(id)][list(currperm[str(id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True
        elif type == 2:
            currperm = self.seasonperms
            usrend = currperm[str(id)][list(currperm[str(id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True
        elif type == 3:
            currperm = self.genperms
            usrend = currperm[str(id)][list(currperm[str(id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True
        elif type == 4:
            currperm = self.cosperms
            usrend = currperm[str(id)][list(currperm[str(id)].keys())[0]]
            if usrend == None:
                return True
            usrendraw = parse(usrend)
            if datetime.now() > usrendraw:
                return False
            else:
                return True

    def has_perms(self, id) -> bool:
        return True if (self.not_expired(1, id) and self.not_expired(2, id) and self.not_expired(3, id) and self.not_expired(4, id)) else False

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Help")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`", description=f'***__{command.brief}__***\n{syntax(command)}', color=random_hex(), timestamp=datetime.utcnow())
        if type(ctx) != discord.member.Member:
            embed.set_author(name='Queried by {}'.format(
                ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="**Command Syntax**", value=f'**{command.help}**')
        embed.set_footer(text='Made by Gulag#2001',
                         icon_url=self.gods_url)
        await ctx.send(embed=embed)

    @command(name='help', help="$help acc", brief="| means alias, <> means required, [] means optional", aliases=['h'])
    @cooldown(5, 60, BucketType.user)
    async def show_help(self, ctx, cmd=None):
        self.ba = self.bot.get_cog('Basic')
        self.fe = self.bot.get_cog('ForEveryone')
        self.rp = self.bot.get_cog('RankPerms')
        self.sp = self.bot.get_cog('SeasonPerms')
        self.gp = self.bot.get_cog('GenPerms')
        self.cp = self.bot.get_cog('CosPerms')
        self.db = self.bot.get_cog('DB')
        self.mu = self.bot.get_cog('Music')
        self.gd = self.bot.get_cog("GodPerms")

        channelids = [i.id for i in (ctx.channel.members) if not i.bot]
        allperms = self.allperms
        invalid = [str(i) for i in channelids if not self.has_perms(i)]
        if cmd is None:
            cmds = []  # initializes cmds list
            if len(invalid) <= 1:
                if ctx.message.author.id in self.godperms:
                    cmds += self.gd.get_commands()
                if str(ctx.message.author.id) in self.rankperms:  # checks
                    cmds += self.rp.get_commands()
                if str(ctx.message.author.id) in self.seasonperms:
                    cmds += self.sp.get_commands()
                    cmds += self.db.get_commands()
                if str(ctx.message.author.id) in self.genperms:
                    cmds += self.gp.get_commands()
                if str(ctx.message.author.id) in self.cosperms:
                    cmds += self.cp.get_commands()
                cmds.sort(key=lambda x: x.name)  # sort bought commands
            elif len(invalid) > 1 and str(ctx.message.author.id) in self.allperms:
                # sorts db/basic/foreveryone commands individually
                await ctx.send("Since there are non-buyers here, I'll only show basic commands")
            s2 = sorted((self.fe.get_commands()+self.ba.get_commands() +
                        self.mu.get_commands()), key=lambda x: x.name)
            cmds += s2
            cmds = self.get_commands() + cmds  # help first
            menu = MenuPages(source=HelpMenu(
                ctx, list(cmds)), delete_message_after=True, timeout=200.0)  # create duh menu
            await menu.start(ctx)  # send

        else:
            if (command := get(self.bot.commands, name=cmd)):
                access = "You don't have access to that command"
                if (command.cog_name == "RankPerms" and str(ctx.message.author.id) not in self.rankperms) or (command.cog_name == "SeasonPerms" and str(ctx.message.author.id) not in self.seasonperms) or \
                   (command.cog_name == "GenPerms" and str(ctx.message.author.id) not in self.genperms) or (command.cog_name == "CosPerms" and str(ctx.message.author.id) not in self.cosperms) or (command.cog_name == "GodPerms" and (ctx.message.author.id) not in self.godperms):
                    await ctx.send(access)
                    return

                if len(invalid) > 1 and command.cog_name in ['RankPerms', 'SeasonPerms', 'GenPerms', 'CosPerms', 'GodPerms']:
                    await ctx.message.delete()
                    await ctx.send("Non-buyers are in this channel, dming you the info...")
                    await self.cmd_help(ctx.message.author, command)
                else:
                    await self.cmd_help(ctx, command)

            elif (c := cmd.lower()) in ['cosperms', 'seasonperms', 'genperms', 'rankperms', 'db', 'music', 'foreveryone', 'basic', 'godperms']:
                keydict = {'cosperms': 'CosPerms', 'rankperms': 'RankPerms', 'seasonperms': 'SeasonPerms', 'genperms': 'GenPerms',
                           'basic': 'Basic', 'foreveryone': "ForEveryone", 'godperms': "GodPerms", 'db': "DB", 'music': "Music"}
                if (c == 'cosperms' and str(ctx.message.author.id) not in self.cosperms) or (c == 'genperms' and str(ctx.message.author.id) not in self.genperms) or (c == 'seasonperms' and str(ctx.message.author.id) not in self.seasonperms) or \
                        (c == 'rankperms' and str(ctx.message.author.id) not in self.rankperms) or (c == 'godperms' and str(ctx.message.author.id) not in self.godperms):
                    await ctx.send("You can't access that cog menu")
                    return
                else:
                    if c in keydict:
                        c2 = keydict[c]
                        cmds = []
                        if len(invalid) > 1 and str(ctx.message.author.id) in self.allperms and c in ['rankperms', 'cosperms', 'seasonperms', 'genperms', 'godperms']:
                            await ctx.send("There are non-buyers here, check a cog somewhere else")
                            return
                        cmds += self.bot.get_cog(c2).get_commands()
                        cmds.sort(key=lambda x: x.name)
                        menu = MenuPages(source=HelpMenu(
                            ctx, list(cmds)), delete_message_after=True, timeout=200.0)  # create duh menu
                        await menu.start(ctx)  # send
                    else:
                        await ctx.send("Invalid Cog, run $cogs for a list of cogs.")
                        return
            else:
                await ctx.send("That command does not exist.")

    @command(help="$cogs", brief="gets all cogs, try $help <cogname>")
    @cooldown(1, 60, BucketType.user)
    async def cogs(self, ctx):
        s = time()
        embed = Embed(title="List of Cogs", color=random_hex(),
                      timestamp=datetime.utcnow())
        embed.set_author(name="Queried by {}".format(
            ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        if str(ctx.message.author.id) in self.allperms:
            embed.add_field(
                name="Cogs:", value="Basic\nDB\nForEveryone\nMusic\nCosPerms\nGenPerms\nRankPerms\nSeasonPerms\n")
        else:
            embed.add_field(
                name="Cogs:", value="Basic\nDB\nForEveryone\nMusic\n")
        e = time()
        embed.set_footer(text='{:.2f} seconds • Made by Gulag#2001'.format(
            e-s), icon_url=self.bot.get_cog("GodPerms").gods_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
