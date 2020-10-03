import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys

import pymongo
from pymongo import MongoClient

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Kick
    @commands.command()
    @commands.has_permissions( administrator = True )
    async def kick( self, ctx, member: discord.Member, *, reason = None, guild: discord.Guild = None ):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed( title = '**Kick**', colour = 0xff0000  )
        await ctx.channel.purge( limit = 1 )

        await member.kick( reason = reason )

        emb.set_author( name = guild, icon_url = guild.icon_url )
        emb.add_field( name = '**Kicked user was**', value = '**{}**'.format( member.mention ), inline=False )
        emb.set_thumbnail( url = member.avatar_url )
        emb.add_field( name = "**Roles were**", value = '**{}**'.format( member.roles ).replace( '[' , '' ).replace( ']' , '' ).replace( '<' , '' ).replace( '>' , '' ).replace( "'" , '' ).replace( 'Role' , '' ).replace( 'id=' , '' ).replace( 'name=' , '' ).replace( '1' , '' ).replace( '2' , '' ).replace( '3' , '' ).replace( '4' , '' ).replace( '5' , '' ).replace( '6' , '' ).replace( '7' , '' ).replace( '8' , '' ).replace( '9' , '' ).replace( '0' , '' ).replace('"', '').replace("ud", ''), inline=False )
        emb.set_footer( text = 'Was kicked by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["command-channels"]
        guild_id = ctx.guild.id
        author = ctx.author
        gld_id = {"_id": guild_id}

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    #Ban
    @commands.command()
    @commands.has_permissions( administrator = True )
    async def ban( self, ctx, member: discord.Member, *, reason = None, guild: discord.Guild = None ):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed( title = 'Ban', colour = 0xff0000  )
        await ctx.channel.purge( limit = 1 )

        await member.ban( reason = reason )

        emb.set_author( name = guild, icon_url = guild.icon_url )
        emb.add_field( name = '**Baned user was**', value = '**{}**'.format( member.mention ), inline=False )
        emb.set_thumbnail( url = member.avatar_url )
        emb.set_footer( text = 'Was banned by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
        emb.add_field( name = "**Roles were**", value = '**{}**'.format( member.roles ).replace( '[' , '' ).replace( ']' , '' ).replace( '<' , '' ).replace( '>' , '' ).replace( "'" , '' ).replace( 'Role' , '' ).replace( 'id=' , '' ).replace( 'name=' , '' ).replace( '1' , '' ).replace( '2' , '' ).replace( '3' , '' ).replace( '4' , '' ).replace( '5' , '' ).replace( '6' , '' ).replace( '7' , '' ).replace( '8' , '' ).replace( '9' , '' ).replace( '0' , '' ).replace('"', '').replace("ud", ''), inline=False )

        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["command-channels"]
        guild_id = ctx.guild.id
        author = ctx.author
        gld_id = {"_id": guild_id}

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    #Unban
    @commands.command()
    @commands.has_permissions( administrator = True )
    async def unban( self, ctx, *, member, guild: discord.Guild = None ):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed( title = '**Unban**', colour = 0x55ffee )
        await ctx.channel.purge( limit = 1 )

        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            user = ban_entry.user

            await ctx.guild.unban( user )

            emb.set_author( name = guild, icon_url = guild.icon_url )
            emb.add_field( name = '**Unbaned user was**', value = '**{}**'.format( user ), inline=False )
            emb.set_thumbnail( url = user.avatar_url )
            emb.set_footer( text = 'Was unbanned by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

            mongo_url = ""
            cluster = MongoClient(mongo_url)
            db = cluster["servers"]
            collection = db["command-channels"]
            guild_id = ctx.guild.id
            author = ctx.author
            gld_id = {"_id": guild_id}

            cmdch = collection.find(gld_id)
            for cmdchannel in cmdch:
                cur_channel = cmdchannel["Command_channel"]

            if collection.count_documents(gld_id) == 0:
                await ctx.send(embed = emb)
            else:
                channel = self.bot.get_channel( cur_channel )
                await channel.send( embed = emb)

            return

    @kick.error
    async def kick_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .kick @name**' )
        if isinstance( error, commands.MissingPermissions ):
            await ctx.send( f"{ ctx.author.name } you don't have permission to use this command." )
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .kick @name**' )

    @ban.error
    async def ban_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .ban @name**' )
        if isinstance( error, commands.MissingPermissions ):
            await ctx.send( f"{ ctx.author.name } you don't have permission to use this command." )
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .ban @name**' )

    @unban.error
    async def unban_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .unban @name**' )
        if isinstance( error, commands.MissingPermissions ):
            await ctx.send( f"{ ctx.author.name } you don't have permission to use this command." )
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .unban @name**' )

def setup(bot):
    bot.add_cog(AdminCommands(bot))
