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

class Level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message( self, ctx ):
        emb = discord.Embed(colour = 0x55ffee)
        
        collection = db["level-status"]
        author_id = ctx.author.id
        guild_id = ctx.guild.id
        author = ctx.author
        guild = ctx.guild
        myid = str(author_id)
        myid = myid + str(guild_id)

        gld_id = {"_id": guild_id}
        gld_myid = {"_id": myid}

        levelstat = collection.find(gld_id)
        for levelstatus in levelstat:
            cur_stat = levelstatus["Status"]

            if cur_stat == 'off' or collection.count_documents(gld_myid) == 0:
                return
            elif cur_stat == 'on':  
                collection = db["levels"]

                if ctx.author == self.bot.user:
                    return
                elif ctx.author.bot:
                    return

                if collection.count_documents({}) == 0:
                    user_info = {"_id": myid, "AuthorID": author_id, "GuildID": guild_id, "Level": 1, "xp": 0}
                    collection.insert_one(user_info)
                elif collection.count_documents(gld_myid) == 0:
                    user_info = {"_id": myid, "AuthorID": author_id, "GuildID": guild_id, "Level": 1, "xp": 0}
                    collection.insert_one(user_info)

                exp = collection.find(gld_myid)
                for xp in exp:
                    cur_xp = xp["xp"]
                    new_xp = cur_xp + 1
                    collection.update({"_id": myid, "AuthorID": author_id, "GuildID": guild_id}, {"$set": {"xp": new_xp}})

                lvl = collection.find(gld_myid)
                for level in lvl:
                    lvl_start = level["Level"]
                    new_level = lvl_start + 1

                    if cur_xp >=  round(5 * (lvl_start ** 4 / 5)):
                        collection.update({"_id": myid, "AuthorID": author_id, "GuildID": guild_id}, {"$set": {"Level": new_level, "xp": 0}})
                        emb.set_author(name = author.name, icon_url = author.avatar_url)
                        emb.add_field(name = "Level", value = f"{author.name} was leveled up to {new_level} level.")
                        emb.set_thumbnail(url = author.avatar_url)
                        emb.set_footer(text = f'Was leveled up in {guild.name} server.', icon_url = guild.icon_url)

                        collection = db["level-channels"]

                        levelch = collection.find(gld_id)
                        for levelchannel in levelch:
                            cur_channel = levelchannel["Level_channel"]

                        if collection.count_documents(gld_id) == 0:
                            await ctx.channel.send(embed = emb)
                        else:
                            channel = self.bot.get_channel( cur_channel )
                            await channel.send( embed = emb)

    @commands.command(aliases = ['setlvlch'])
    @commands.has_permissions(administrator = True)
    async def setlevelchannel(self, ctx, channel, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        
        collection = db["level-channels"]
        guild_id = ctx.guild.id
        level_ch = int(channel.replace("<#", "").replace(">", ""))

        gld_id = {"_id": guild_id}

        if collection.count_documents({}) == 0:
            level_info = {"_id": guild_id, "Level_channel": level_ch}
            collection.insert_one(level_info)
        elif collection.count_documents(gld_id) == 0:
            level_info = {"_id": guild_id, "Level_channel": level_ch}
            collection.insert_one(level_info)

        levelch = collection.find(gld_id)
        for levelchannel in levelch:
            cur_channel = levelchannel["Level_channel"]
            new_channel = level_ch

        if collection.count_documents(gld_id) == 0:
            collection.update({"_id": guild_id}, {"$set": {"Level_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's level channel have been setted to: **{channel}")
        elif cur_channel == level_ch:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's level channel already is: **{channel}")
        elif cur_channel is not None:
            collection.update({"_id": guild_id}, {"$set": {"Level_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's level channel have been changed to: **{channel}")
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

    @commands.command(aliases = ['setlvlst'])
    @commands.has_permissions(administrator = True)
    async def setlevelstatus(self, ctx, stat, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        
        collection = db["level-status"]
        guild_id = ctx.guild.id

        gld_id = {"_id": guild_id}
        stat = str(stat)

        if stat == 'on' or stat == 'off':
            emb = discord.Embed(colour = 0x55ffee)

            if collection.count_documents({}) == 0:
                levelstat_info = {"_id": guild_id, "Status": stat}
                collection.insert_one(levelstat_info)
            elif collection.count_documents(gld_id) == 0:
                levelstat_info = {"_id": guild_id, "Status": stat}
                collection.insert_one(levelstat_info)

            levelstat = collection.find(gld_id)
            for levelstatus in levelstat:
                cur_stat = levelstatus["Status"]
                new_stat = stat

            if collection.count_documents(gld_id) == 0:
                collection.update({"_id": guild_id}, {"$set": {"Status": new_stat}})
                emb.set_author(name = guild.name, icon_url = guild.icon_url)
                emb.add_field(name = "**Successful**", value = f"**Your server's level status have been setted to: **{stat}")  
            elif cur_stat == stat:
                emb.set_author(name = guild.name, icon_url = guild.icon_url)
                emb.add_field(name = "**Error**", value = f"**Your server's level status already is: **{stat}")
            elif cur_stat is not None:
                collection.update({"_id": guild_id}, {"$set": {"Status": new_stat}})
                emb.set_author(name = guild.name, icon_url = guild.icon_url)
                emb.add_field(name = "**Successful**", value = f"**Your server's level status have been changed to: **{stat}")            
            else:
                emb.set_author(name = guild.name, icon_url = guild.icon_url)
                emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")
        else:
            emb = discord.Embed(colour = 0xff0000)
            emb.add_field(name = '**Error**', value = "Something went wrong please type the command correct for aditional information type help setlevelstatus or setlvlst")

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @setlevelchannel.error
    async def setlevelchannel_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setlvlch #channel**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setlvlch #channel**' )
    
    @setlevelstatus.error
    async def setlevelstatus_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setlevelstatus on/off**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setlevelstatus on/off**' )

def setup(bot):
    bot.add_cog(Level(bot))
