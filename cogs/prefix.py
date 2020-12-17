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

class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['setpfx'])
    @commands.has_permissions(administrator = True)
    async def setprefix(self, ctx, prefix, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        
        collection = db["prefixes"]
        guild_id = ctx.guild.id
        guild_prefix = prefix

        gld_id = {"_id": guild_id}

        if collection.count_documents({}) == 0:
            prefix_info = {"_id": guild_id, "Prefix": guild_prefix}
            collection.insert_one(prefix_info)

        if collection.count_documents(gld_id) == 0:
            prefix_info = {"_id": guild_id, "Prefix": guild_prefix}
            collection.insert_one(prefix_info)

        pfx = collection.find(gld_id)
        for prefix in pfx:
            cur_prefix = prefix["Prefix"]
            new_prefix = guild_prefix

        if collection.count_documents == 0:
            collection.update({"_id": guild_id}, {"$set": {"Prefix": new_prefix}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's prefix have been changed to: ``{new_prefix}``**")
        elif cur_prefix == guild_prefix:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's prefix already is: ``{cur_prefix}``**")
        elif cur_prefix is not None:
            collection.update({"_id": guild_id}, {"$set": {"Prefix": new_prefix}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's prefix have been changed to: ``{new_prefix}``**")
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @setprefix.error
    async def setprefix_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setprefix [prefix]**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setprefix [prefix]**' )

def setup(bot):
    bot.add_cog(Prefix(bot))
