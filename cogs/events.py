import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys

import pymongo
from pymongo import MongoClient

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Auto role
    @commands.Cog.listener()
    async def on_member_join( self, member ):
        emb = discord.Embed( colour = 0x55ffee )

        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["welcome-channels"]
        guild = member.guild
        guild_id = member.guild.id

        gld_id = {"_id": guild_id}

        wch = collection.find(gld_id)
        for welcome in wch:
            cur_channel = welcome["Welcome_channel"]

        channel = self.bot.get_channel( cur_channel )

        collection = db["welcome-roles"]

        wrl = collection.find(gld_id)
        for welcomerole in wrl:
            cur_wlrole = welcomerole["Welcome_role"]

        if collection.count_documents(gld_id) != 0:
            role = discord.utils.get( member.guild.roles, id = cur_wlrole )
            await member.add_roles( role )
        else:
            return

        emb.set_author( name = guild.name, icon_url = guild.icon_url )
        emb.add_field( name = "**Say Hello to**", value = '**{}**'.format( member.mention ), inline=False )
        emb.set_thumbnail( url = member.avatar_url )

        await channel.send( embed = emb)

    #Cool Removing
    @commands.Cog.listener()
    async def on_member_remove( self, member ):
        emb = discord.Embed( title = '**Member left us**', colour = 0xff0000  )

        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["welcome-channels"]
        guild_id = member.guild.id
        guild = member.guild
        author_id = member.id
        author = member
        myid = str(author_id)
        myid = myid + str(guild_id)

        gld_myid = {"_id": myid}
        gld_id = {"_id": guild_id}

        wch = collection.find(gld_id)
        for welcome in wch:
            cur_channel = welcome["Welcome_channel"]
            channel = self.bot.get_channel( cur_channel )

        collection = db["levels"]


        exp = collection.find(gld_myid)
        for xp in exp:
            cur_xp = xp["xp"]

        lvl = collection.find(gld_myid)
        for level in lvl:
            lvl_start = level["Level"]

        if collection.count_documents(gld_myid) != 0:
            user_info = {"_id": myid, "AuthorID": author_id, "GuildID": guild_id, "Level": lvl_start, "xp": cur_xp}
            collection.delete_one(user_info)
            emb.set_author( name = guild.name, icon_url = guild.icon_url )
            emb.add_field( name = "**Say GoodBye to**", value = '**{}**'.format( member.mention ), inline=False )
            emb.add_field(name="**Level was**", value=f'**{lvl_start}**', inline=False)
            emb.add_field(name="**Experience was**", value=f"**{cur_xp}**", inline=False)
            emb.set_thumbnail( url = member.avatar_url )
            emb.add_field( name = "**Roles were**", value = '**{}**'.format( member.roles ).replace( '[' , '' ).replace( ']' , '' ).replace( '<' , '' ).replace( '>' , '' ).replace( "'" , '' ).replace( 'Role' , '' ).replace( 'id=' , '' ).replace( 'name=' , '' ).replace( '1' , '' ).replace( '2' , '' ).replace( '3' , '' ).replace( '4' , '' ).replace( '5' , '' ).replace( '6' , '' ).replace( '7' , '' ).replace( '8' , '' ).replace( '9' , '' ).replace( '0' , '' ).replace('"', '').replace("ud", ''), inline=False )
        else:
            emb.set_author( name = guild.name, icon_url = guild.icon_url )
            emb.add_field( name = "**Say GoodBye to**", value = '**{}**'.format( member.mention ), inline=False )
            emb.add_field(name="**Level was**", value=f'**1**', inline=False)
            emb.add_field(name="**Experience was**", value=f"**0**", inline=False)
            emb.set_thumbnail( url = member.avatar_url )
            emb.add_field( name = "**Roles were**", value = '**{}**'.format( member.roles ).replace( '[' , '' ).replace( ']' , '' ).replace( '<' , '' ).replace( '>' , '' ).replace( "'" , '' ).replace( 'Role' , '' ).replace( 'id=' , '' ).replace( 'name=' , '' ).replace( '1' , '' ).replace( '2' , '' ).replace( '3' , '' ).replace( '4' , '' ).replace( '5' , '' ).replace( '6' , '' ).replace( '7' , '' ).replace( '8' , '' ).replace( '9' , '' ).replace( '0' , '' ).replace('"', '').replace("ud", ''), inline=False )

        await channel.send( embed = emb)

    #Guild Join
    @commands.Cog.listener()
    async def on_guild_join( self, guild ):
        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["prefixes"]
        guild_id = guild.id

        gld_id = {"_id": guild_id}

        if collection.count_documents({}) == 0:
            prefix_info = {"_id": guild_id, "Prefix": '.'}
            collection.insert_one(prefix_info)

        if collection.count_documents(gld_id) == 0:
            prefix_info = {"_id": guild_id, "Prefix": '.'}
            collection.insert_one(prefix_info)

    #Guild Join
    @commands.Cog.listener()
    async def on_guild_remove( self, guild ):
        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["prefixes"]
        guild_id = guild.id

        gld_id = {"_id": guild_id}

        pfx = collection.find(gld_id)
        for prefix in pfx:
            cur_prefix = prefix["Prefix"]

        prefix_info = {"_id": guild_id, "Prefix": cur_prefix}

        collection.delete_one(prefix_info)

        collection = db["mute-roles"]

        mtr = collection.find(gld_id)
        for muterole in mtr:
            cur_role = muterole["Mute_role"]

            if cur_role is not None:
                mtrole_info = {"_id": guild_id, "Mute_role": cur_role}

                collection.delete_one(mtrole_info)
            else:
                return

        collection = db["welcome-channels"]

        wch = collection.find(gld_id)
        for welcome in wch:
            cur_channel = welcome["Welcome_channel"]

            if cur_channel is not None:
                wlch_info = {"_id": guild_id, "Welcome_channel": cur_channel}

                collection.delete_one(wlch_info)
            else:
                return

        collection = db["welcome-roles"]

        wch = collection.find(gld_id)
        for welcomerole in wch:
            cur_wlrole = welcomerole["Welcome_role"]

            if cur_wlrole is not None:
                welcomerole_info = {"_id": guild_id, "Welcome_role": cur_wlrole}

                collection.delete_one(welcomerole_info)
            else:
                return

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

            if cur_channel is not None:
                cmd_info = {"_id": guild_id, "Command_channel": cur_channel}

                collection.delete_one(cmd_info)
            else:
                return

        collection = db["levels"]

        gld_id = {"GuildID": guild_id}

        exp = collection.find(gld_id)
        for xp in exp:
            cur_xp = xp["xp"]

        lvl = collection.find(gld_id)
        for level in lvl:
            lvl_start = level["Level"]

            if lvl_start is not None:
                user_info = {"GuildID": guild_id, "Level": lvl_start, "xp": cur_xp}

                collection.delete_one(user_info)
            else:
                return

    #Leveling system
    @commands.Cog.listener()
    async def on_message( self, ctx ):
        emb = discord.Embed(colour = 0x55ffee)
        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["levels"]
        author_id = ctx.author.id
        guild_id = ctx.guild.id
        author = ctx.author
        guild = ctx.guild
        myid = str(author_id)
        myid = myid + str(guild_id)

        gld_id = {"_id": guild_id}
        gld_myid = {"_id": myid}

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

            if cur_xp >= round(5 * (lvl_start ** 4 / 5)):
                collection.update({"_id": myid, "AuthorID": author_id, "GuildID": guild_id}, {"$set": {"Level": new_level, "xp": 0}})
                emb.set_author(name = author.name, icon_url = author.avatar_url)
                emb.add_field(name = "Level", value = f"{author.name} was leveled up to {new_level} level.")
                emb.set_thumbnail(url=author.avatar_url)
                emb.set_footer(text=f'Was leveled up in {guild.name} server.', icon_url=guild.icon_url)

                collection = db["role-channels"]

                rolech = collection.find(gld_id)
                for rolechannel in rolech:
                    cur_channel = rolechannel["Role_channel"]

                if collection.count_documents(gld_id) == 0:
                    await ctx.channel.send(embed = emb)
                else:
                    channel = self.bot.get_channel( cur_channel )
                    await channel.send( embed = emb)



def setup(bot):
    bot.add_cog(Events(bot))
