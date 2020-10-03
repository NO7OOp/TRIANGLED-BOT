import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys

import pymongo
from pymongo import MongoClient

class MessageCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Clear message
    @commands.command(aliases = ['cl'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild

        emb = discord.Embed(title='**Clear**', colour = 0x55ffee)
        await ctx.channel.purge(limit=amount + 1)

        emb.set_author(name=guild, icon_url=guild.icon_url)
        emb.add_field(name='**Was requested to delete**',
                      value='**{} messages**'.format(amount), inline=False)
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        emb.set_footer(text='Was requested by {}'.format(
            ctx.author.name), icon_url=ctx.author.avatar_url)

        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
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

    # Mute
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(title='**Mute**', colour=0xff0000 )
        await ctx.channel.purge(limit=1)

        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["mute-roles"]
        guild_id = ctx.guild.id
        author = ctx.author

        gld_id = {"_id": guild_id}

        mtr = collection.find(gld_id)
        for muterole in mtr:
            cur_role = muterole["Mute_role"]

        if collection.count_documents(gld_id) == 0:
            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Error**',
                            value="**Your server don't have role for mute, add it by command ``setmute``**", inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            emb.set_footer(text='Was requested to mute by {}'.format(
                ctx.author.name), icon_url=ctx.author.avatar_url)
        else:
            mute_role = discord.utils.get(ctx.message.guild.roles, id = cur_role)

            await member.add_roles(mute_role)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Muted user is**',
                          value='**{}**'.format(member.mention), inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            emb.set_footer(text='Was muted by {}'.format(
                ctx.author.name), icon_url=ctx.author.avatar_url)
            emb.add_field(name="**Roles were**", value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
                'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)


            collection = db["command-channels"]

            cmdch = collection.find(gld_id)
            for cmdchannel in cmdch:
                cur_channel = cmdchannel["Command_channel"]

            if collection.count_documents(gld_id) == 0:
                await ctx.send(embed = emb)
            else:
                channel = self.bot.get_channel( cur_channel )
                await channel.send( embed = emb)

    # Unmute
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(title='**Unmute**', colour = 0x55ffee)
        await ctx.channel.purge(limit=1)

        mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["mute-roles"]
        guild_id = ctx.guild.id
        author = ctx.author

        gld_id = {"_id": guild_id}

        mtr = collection.find(gld_id)
        for muterole in mtr:
            cur_role = muterole["Mute_role"]

        if collection.count_documents(gld_id) == 0:
            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Error**',
                            value="**Your server don't have role for mute, add it by command ``setmute``**", inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            emb.set_footer(text='Was requested to mute by {}'.format(
                ctx.author.name), icon_url=ctx.author.avatar_url)
        else:
            mute_role = discord.utils.get(ctx.message.guild.roles, id = cur_role)

            if mute_role in member.roles:
                await member.remove_roles(mute_role)

                emb.set_author(name=guild, icon_url=guild.icon_url)
                emb.add_field(name='**Unmuted user is**',
                              value='**{}**'.format(member.mention), inline=False)
                emb.set_thumbnail(url=member.avatar_url)
                emb.set_footer(text='Was unmuted by {}'.format(
                    ctx.author.name), icon_url=ctx.author.avatar_url)
                emb.add_field(name="**Roles are**".format(member.mention), value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
                    'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)

            else:
                emb.set_author(name=guild, icon_url=guild.icon_url)
                emb.add_field(name="**User**", value="**{}'s not muted**".format(
                    member.mention), inline=False)
                emb.set_thumbnail(url=member.avatar_url)
                emb.add_field(name="**Roles are**".format(member.mention), value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
                    'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)


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

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ ctx.author.name } please specify the number of messages to clear **ex: .clear 100**')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have permission to use this command.")

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
    bot.add_cog(MessageCommands(bot))
