import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys
import pymongo
from pymongo import MongoClient

sys.path.insert(1, '../TRIANGLED')
import config

mongo_url = config.mongo_url
cluster = MongoClient(mongo_url)
db = cluster["servers"]

class MessageCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Clear message
    @commands.command(aliases = ['cl'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount: int, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild

        emb = discord.Embed(colour = 0x55ffee)
        await ctx.channel.purge(limit = amount + 1)

        emb.set_author(name = guild, icon_url = guild.icon_url)
        emb.add_field(name = '**Was requested to delete**',
                      value = '**{} messages**'.format(amount), inline = False)
        emb.set_thumbnail(url = self.bot.user.avatar_url)
        emb.set_footer(text = 'Was requested by {}'.format(
            ctx.author.name), icon_url = ctx.author.avatar_url)

        
        collection = db["command-channels"]
        guild_id = ctx.guild.id
        gld_id = {"_id": guild_id}

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ ctx.author.name } please specify the number of messages to clear **ex: .clear 100**')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have permission to use this command.")

def setup(bot):
    bot.add_cog(MessageCommands(bot))
