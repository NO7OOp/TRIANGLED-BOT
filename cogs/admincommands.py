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

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Kick
    @commands.command()
    @commands.has_permissions( administrator = True )
    async def kick( self, ctx, member: discord.Member, *, reason = None, guild: discord.Guild = None ):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0xff0000)

        if member == ctx.author:
            ctx.send("You can not kick yourself.")
        else:
            await member.kick( reason = reason )

            if reason is None:
                reason = 'Not mentioned'

            role_names = []
            for role in member.roles:
                role_names.append(role.name)
            role_names = ', '.join(role_names)

            collection = db["level-status"]
            guild_id = ctx.guild.id
            author_id = member.id
            myid = str(author_id)
            myid = myid + str(guild_id)
            gld_id = {"_id": guild_id}

            gld_myid = {"_id": myid}

            if collection.count_documents(gld_id) == 0:
                collection = db["levels"]

                if collection.count_documents(gld_myid) !=  0:
                    user_info = {"_id": myid}
                    collection.delete_one(user_info)

                emb.set_author( name = guild, icon_url = guild.icon_url )
                emb.add_field( name = '**Kicked user was**', value = '**{}**'.format( member.mention ), inline = False )
                emb.add_field( name = '**Reason was**', value = f'**{reason}**')
                emb.set_thumbnail( url = member.avatar_url )
                emb.add_field(name="**Roles were**", value=f'**{role_names}**', inline = False )
                emb.set_footer( text = 'Was kicked by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
            else:
                levelstat = collection.find(gld_id)
                for levelstatus in levelstat:
                    cur_stat = levelstatus["Status"]

                    if cur_stat == 'off':
                        collection = db["levels"]

                        if collection.count_documents(gld_myid) !=  0:
                            user_info = {"_id": myid}
                            collection.delete_one(user_info)

                        emb.set_author( name = guild, icon_url = guild.icon_url )
                        emb.add_field( name = '**Kicked user was**', value = '**{}**'.format( member.mention ), inline = False )
                        emb.add_field( name = '**Reason was**', value = f'**{reason}**')
                        emb.set_thumbnail( url = member.avatar_url )
                        emb.add_field(name="**Roles were**", value=f'**{role_names}**', inline = False )
                        emb.set_footer( text = 'Was kicked by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
                    elif cur_stat == 'on':
                        collection = db["levels"]

                        exp = collection.find(gld_myid)
                        for xp in exp:
                            cur_xp = xp["xp"]

                        lvl = collection.find(gld_myid)
                        for level in lvl:
                            lvl_start = level["Level"]

                        emb.set_author( name = guild, icon_url = guild.icon_url )
                        emb.add_field( name = '**Kicked user was**', value = '**{}**'.format( member.mention ), inline = False )
                        if collection.count_documents(gld_myid) !=  0:
                            emb.add_field(name = "**Level was**", value = f'**{lvl_start}**')
                            emb.add_field(name = '** **', value = '** **')
                            emb.add_field(name = "**Experience was**", value = f"**{cur_xp}**")
                            user_info = {"_id": myid, "AuthorID": author_id, "GuildID": guild_id, "Level": lvl_start, "xp": cur_xp}
                            collection.delete_one(user_info)
                        else:
                            emb.add_field(name = "**Level was**", value = f'**1**')
                            emb.add_field(name = '** **', value = '** **')
                            emb.add_field(name = "**Experience was**", value = f"**0**")
                        emb.add_field( name = '**Reason was**', value = f'**{reason}**')
                        emb.set_thumbnail( url = member.avatar_url )
                        emb.add_field(name="**Roles were**", value=f'**{role_names}**', inline = False )
                        emb.set_footer( text = 'Was kicked by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

            collection = db["command-channels"]

            cmdch = collection.find(gld_id)
            for cmdchannel in cmdch:
                cur_channel = cmdchannel["Command_channel"]

            if collection.count_documents(gld_id) == 0:
                await ctx.send(embed = emb)
            else:
                channel = self.bot.get_channel( cur_channel )
                await channel.send( embed = emb)

            await member.send(embed = emb)

    #Ban
    @commands.command()
    @commands.has_permissions( administrator = True )
    async def ban( self, ctx, member: discord.Member, *, reason = None, guild: discord.Guild = None ):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0xff0000)

        if member == ctx.author:
            ctx.send("You can not ban yourself.")
        else:
            await member.ban( reason = reason )

            if reason is None:
                reason = 'Not mentioned'

            role_names = []
            for role in member.roles:
                role_names.append(role.name)
            role_names = ', '.join(role_names)

            collection = db["level-status"]
            guild_id = ctx.guild.id
            author_id = member.id
            myid = str(author_id)
            myid = myid + str(guild_id)
            gld_id = {"_id": guild_id}

            gld_myid = {"_id": myid}

            if collection.count_documents(gld_id) == 0:
                collection = db["levels"]

                if collection.count_documents(gld_myid) !=  0:
                    user_info = {"_id": myid}
                    collection.delete_one(user_info)

                emb.set_author( name = guild, icon_url = guild.icon_url )
                emb.add_field( name = '**Banned user was**', value = '**{}**'.format( member.mention ), inline = False )
                emb.add_field( name = '**Reason was**', value = f'**{reason}**')
                emb.set_thumbnail( url = member.avatar_url )
                emb.add_field(name="**Roles were**", value=f'**{role_names}**', inline = False )
                emb.set_footer( text = 'Was banned by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
            else:
                levelstat = collection.find(gld_id)
                for levelstatus in levelstat:
                    cur_stat = levelstatus["Status"]

                    if cur_stat == 'off':
                        collection = db["levels"]

                        if collection.count_documents(gld_myid) !=  0:
                            user_info = {"_id": myid}
                            collection.delete_one(user_info)

                        emb.set_author( name = guild, icon_url = guild.icon_url )
                        emb.add_field( name = '**Banned user was**', value = '**{}**'.format( member.mention ), inline = False )
                        emb.add_field( name = '**Reason was**', value = f'**{reason}**')
                        emb.set_thumbnail( url = member.avatar_url )
                        emb.add_field(name="**Roles were**", value=f'**{role_names}**', inline = False )
                        emb.set_footer( text = 'Was banned by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
                    elif cur_stat == 'on':
                        collection = db["levels"]

                        exp = collection.find(gld_myid)
                        for xp in exp:
                            cur_xp = xp["xp"]

                        lvl = collection.find(gld_myid)
                        for level in lvl:
                            lvl_start = level["Level"]

                        emb.set_author( name = guild, icon_url = guild.icon_url )
                        emb.add_field( name = '**Banned user was**', value = '**{}**'.format( member.mention ), inline = False )
                        if collection.count_documents(gld_myid) !=  0:
                            emb.add_field(name = "**Level was**", value = f'**{lvl_start}**')
                            emb.add_field(name = '** **', value = '** **')
                            emb.add_field(name = "**Experience was**", value = f"**{cur_xp}**")
                            user_info = {"_id": myid, "AuthorID": author_id, "GuildID": guild_id, "Level": lvl_start, "xp": cur_xp}
                            collection.delete_one(user_info)
                        else:
                            emb.add_field(name = "**Level was**", value = f'**1**')
                            emb.add_field(name = '** **', value = '** **')
                            emb.add_field(name = "**Experience was**", value = f"**0**")
                        emb.add_field( name = '**Reason was**', value = f'**{reason}**')
                        emb.set_thumbnail( url = member.avatar_url )
                        emb.add_field(name="**Roles were**", value=f'**{role_names}**', inline = False )
                        emb.set_footer( text = 'Was banned by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

            collection = db["command-channels"]

            cmdch = collection.find(gld_id)
            for cmdchannel in cmdch:
                cur_channel = cmdchannel["Command_channel"]

            if collection.count_documents(gld_id) == 0:
                await ctx.send(embed = emb)
            else:
                channel = self.bot.get_channel( cur_channel )
                await channel.send( embed = emb)

            await member.send(embed = emb)

    #Unban
    @commands.command()
    @commands.has_permissions( administrator = True )
    async def unban(self, ctx, *, member, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed( colour = 0x55ffee )
        guild_id = ctx.guild.id
        gld_id = {"_id": guild_id}

        banned_users = await ctx.guild.bans()
        
        member = int(member.replace('<@!', '').replace('>', ''))
        for i in banned_users:
            if member == i.user.id:
                user = i.user

                await ctx.guild.unban(user)

                emb.set_author( name = guild, icon_url = guild.icon_url )
                emb.add_field( name = '**Unbaned user was**', value = '**{}**'.format( user ), inline = False )
                emb.set_thumbnail( url = user.avatar_url )
                emb.set_footer( text = 'Was unbanned by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

                collection = db["command-channels"]

                cmdch = collection.find(gld_id)
                for cmdchannel in cmdch:
                    cur_channel = cmdchannel["Command_channel"]

                if collection.count_documents(gld_id) == 0:
                    await ctx.send(embed = emb)
                else:
                    channel = self.bot.get_channel( cur_channel )
                    await channel.send( embed = emb)
            # else:
            #     emb.set_author( name = guild, icon_url = guild.icon_url )
            #     emb.add_field( name = '**User**', value = "**{} isn't banned**".format( user ), inline = False )
            #     emb.set_thumbnail( url = user.avatar_url )
            #     emb.set_footer( text = 'Was requested to unban by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

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