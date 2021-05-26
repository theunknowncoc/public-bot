import aiofiles
from discord.ext.commands.core import cooldown
from .A import *
from discord import Embed, File
from discord.ext.commands import BucketType, Cog, command
from db import db


class DB(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.god = 1
        self.gods_url = f"https://cdn.discordapp.com/avatars/{self.god}/b0df2621a8f5b5155a561cca35a3e79e.webp?size=1024"
        self.seasonperms = self.bot.get_cog("GodPerms").seasonperms

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("DB")

    async def givesafuck(self, ctx):
        await ctx.send(file=File('pictures/givesafuck.jpg'))

    def has_perms(self, ctx) -> bool:
        return True if (self.bot.get_cog("GodPerms").not_expired(1, ctx) or self.bot.get_cog("GodPerms").not_expired(2, ctx) or self.bot.get_cog("GodPerms").not_expired(3, ctx) or self.bot.get_cog("GodPerms").not_expired(4, ctx)) else False

    @command(name="store", help="$store #2PP", brief="stores tags in your personal database")
    async def store(self, ctx, tag):
        if self.has_perms(ctx):
            if len(tag) > 15 or len(tag) < 3:
                await ctx.send("Invalid tag.")
                return

            tag = tag.upper()
            tags = db.field("SELECT Tag FROM tags WHERE UserID = ?",
                            int(ctx.message.author.id))
            tags = [i for i in tags.split("~") if i != "x" and i]

            if (len(tags)) >= 50:
                await ctx.send("You hit your limit of 50 tags. Remove one to add more. Consult $mytags for your tags.")
                return
            if tag in tags:
                await ctx.send("Duplicate tag, try another one.")
                return

            tags.append(tag)
            tags = "~".join(tags)
            db.execute("UPDATE tags SET Tag = ? WHERE UserID = ?",
                       tags, int(ctx.message.author.id))
            db.commit()
            await ctx.send(f"Added {tag} to your database")
        else:
            await self.givesafuck(ctx)

    @command(name="mytags", help="$mytags", brief="shows the tags in your database")
    @cooldown(1, 20, BucketType.user)
    async def mytags(self, ctx):
        if self.has_perms(ctx):
            s = time()
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M %p EST")
            tags = db.field("SELECT Tag FROM tags WHERE UserID = ?",
                            int(ctx.message.author.id))
            tags = [i for i in tags.split("~") if i != "x" and i]
            embed = Embed(title='Tag Database', color=random_hex(),
                          timestamp=datetime.utcnow())
            embed.set_author(name='Queried by {}, {}'.format(
                ctx.message.author.name, dt_string), icon_url=ctx.message.author.avatar_url)
            embed.add_field(name='Your Tags',
                            value='**{}**'.format(tags), inline=False)
            e = time()
            embed.set_footer(text='{:.2f} seconds • Made by Gulag#2001'.format(
                e-s), icon_url=self.gods_url)
            await ctx.send(embed=embed)
        else:
            await self.givesafuck(ctx)

    @command(name="remove", help="$remove #2PP", brief="removes tags from your personal database")
    async def remove(self, ctx, tag):
        if self.has_perms(ctx):
            tags = db.field("SELECT Tag FROM tags WHERE UserID = ?",
                            int(ctx.message.author.id))
            tags = [i for i in tags.split("~") if i != "x" and i]
            try:
                tags.remove(tag.upper())
                tags = "~".join(tags)
                db.execute("UPDATE tags SET Tag = ? WHERE UserID = ?",
                           tags, int(ctx.message.author.id))
                db.commit()
                await ctx.send("Removed {} from your database".format(tag))
            except:
                await ctx.send("Please format your tag the same when you first stored it.")
        else:
            await self.givesafuck(ctx)


def setup(bot):
    bot.add_cog(DB(bot))
