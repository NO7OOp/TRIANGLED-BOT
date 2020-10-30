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

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member: discord.Member, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0xff0000 )

        collection = db["mute-roles"]
        guild_id = ctx.guild.id

        gld_id = {"_id": guild_id}

        mtr = collection.find(gld_id)
        for muterole in mtr:
            cur_role = muterole["Mute_role"]

        role_names = []
        for role in member.roles:
            role_names.append(role.name)
        role_names = ', '.join(role_names)

        if collection.count_documents(gld_id) == 0:
            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Error**',
                            value = "**Your server don't have role for mute, add it by command ``setmute``**", inline = False)
            emb.set_thumbnail(url = member.avatar_url)
            emb.set_footer(text = 'Was requested to mute by {}'.format(
                ctx.author.name), icon_url = ctx.author.avatar_url)
        else:
            mute_role = discord.utils.get(ctx.message.guild.roles, id = cur_role)

            await member.add_roles(mute_role)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Muted user is**',
                          value = '**{}**'.format(member.mention), inline = False)
            emb.set_thumbnail(url = member.avatar_url)
            emb.set_footer(text = 'Was muted by {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
            emb.add_field(name="**Roles were**", value=f'**{role_names}**')

            collection = db["command-channels"]

            cmdch = collection.find(gld_id)
            for cmdchannel in cmdch:
                cur_channel = cmdchannel["Command_channel"]

            if collection.count_documents(gld_id) == 0:
                await ctx.send(embed = emb)
            else:
                channel = self.bot.get_channel( cur_channel )
                await channel.send( embed = emb)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: discord.Member, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)

        collection = db["mute-roles"]
        guild_id = ctx.guild.id

        gld_id = {"_id": guild_id}

        mtr = collection.find(gld_id)
        for muterole in mtr:
            cur_role = muterole["Mute_role"]

        role_names = []
        for role in member.roles:
            role_names.append(role.name)
        role_names = ', '.join(role_names)

        if collection.count_documents(gld_id) == 0:
            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Error**',
                            value = "**Your server don't have role for mute, add it by command ``setmute``**", inline = False)
            emb.set_thumbnail(url = member.avatar_url)
            emb.set_footer(text = 'Was requested to mute by {}'.format(
                ctx.author.name), icon_url = ctx.author.avatar_url)
        else:
            mute_role = discord.utils.get(ctx.message.guild.roles, id = cur_role)

            if mute_role in member.roles:
                await member.remove_roles(mute_role)

                emb.set_author(name = guild, icon_url = guild.icon_url)
                emb.add_field(name = '**Unmuted user is**',
                              value = '**{}**'.format(member.mention), inline = False)
                emb.set_thumbnail(url = member.avatar_url)
                emb.add_field(name="**Roles were**", value=f'**{role_names}**')
                emb.set_footer(text = 'Was unmuted by {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
            else:
                emb.set_author(name = guild, icon_url = guild.icon_url)
                emb.add_field(name = "**User**", value = "**{}'s not muted**".format(member.mention), inline = False)
                emb.set_thumbnail(url = member.avatar_url)
                emb.add_field(name="**Roles are**", value=f'**{role_names}**')

            collection = db["command-channels"]

            cmdch = collection.find(gld_id)
            for cmdchannel in cmdch:
                cur_channel = cmdchannel["Command_channel"]

            if collection.count_documents(gld_id) == 0:
                await ctx.send(embed = emb)
            else:
                channel = self.bot.get_channel( cur_channel )
                await channel.send( embed = emb)

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @commands.command(aliases = ['setmuterl'])
    @commands.has_permissions(administrator = True)
    async def setmuterole(self, ctx, role, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        
        collection = db["mute-roles"]
        guild_id = ctx.guild.id
        mute_role = int(role.replace("<@&", "").replace(">", ""))

        gld_id = {"_id": guild_id}

        if collection.count_documents({}) == 0:
            mtrole_info = {"_id": guild_id, "Mute_role": mute_role}
            collection.insert_one(mtrole_info)
        elif collection.count_documents(gld_id) == 0:
            mtrole_info = {"_id": guild_id, "Mute_role": mute_role}
            collection.insert_one(mtrole_info)

        mtr = collection.find(gld_id)
        for muterole in mtr:
            cur_role = muterole["Mute_role"]
            new_role = mute_role

        if collection.count_documents == 0:
            collection.update({"_id": guild_id}, {"$set": {"Mute_role": new_role}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's mute role have been setted to: {role}**")
        elif cur_role == mute_role:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's mute role already is: {role}**")
        elif cur_role is not None:
            collection.update({"_id": guild_id}, {"$set": {"Mute_role": new_role}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's mute role have been changed to: {role}**")
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

    @setmuterole.error
    async def setmuterole_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setmuterl @role**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setmuterl @role**' )

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ ctx.author.name } please type correct **ex: .mute @name**')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Manage messages`` permission to use this command.")
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ ctx.author.name } you wrote something wrong please try again **ex: .mute @name**')

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ ctx.author.name } please type correct **ex: .unmute @name**')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Manage messages`` permission to use this command.")
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ ctx.author.name } you wrote something wrong please try again **ex: .unmute @name**')

def setup(bot):
    bot.add_cog(Mute(bot))
