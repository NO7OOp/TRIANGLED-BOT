import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys

import pymongo
from pymongo import MongoClient

class RoleCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Add role by command
    @commands.command(aliases = ['addrl'])
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member = None, role: discord.Role = None, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        await ctx.channel.purge(limit=1)

        if role in member.roles:

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.set_thumbnail(url=member.avatar_url)
            emb.add_field(name=f'Add role',
                        value=f'{member.mention} already have role **{role}**', inline=False)
            emb.add_field(name=f"**Roles were**", value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
                'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)
            emb.set_footer(text='Was requested to add by {}'.format(
                ctx.author.name), icon_url=ctx.author.avatar_url)

        else:

            await member.add_roles(role)
            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.set_thumbnail(url=member.avatar_url)
            emb.add_field(name=f'Add role',
                        value=f'{member.mention} now have role **{role}**', inline=False)
            emb.add_field(name=f"**Roles are**", value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
                'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)
            emb.set_footer(text='Was requested to add by {}'.format(
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

    # Remove role by command
    @commands.command(aliases = ['removerl'])
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member = None, role: discord.Role = None, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        await ctx.channel.purge(limit=1)

        if role in member.roles:
            await member.remove_roles(role)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.set_thumbnail(url=member.avatar_url)
            emb.add_field(name=f'Remove role',
                        value=f"{member.mention} already don't have role **{role}**", inline=False)
            emb.add_field(name=f"**Roles were**", value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
                'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)
            emb.set_footer(text='Was removed by {}'.format(
                ctx.author.name), icon_url=ctx.author.avatar_url)

        else:
            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.set_thumbnail(url=member.avatar_url)
            emb.add_field(name=f'Remove role',
                        value=f"{member.mention} don't have role **{role}**", inline=False)
            emb.add_field(name=f"**Roles are**", value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
                'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)
            emb.set_footer(text='Was removed by {}'.format(
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

    # #Add reaction
    # @commands.command(aliases = ['addra'])
    # @commands.has_permissions(manage_roles=True)
    # async def addreaction( self, ctx, messageid, emoji1 = None, role1 = None, emoji2 = None, role2 = None, emoji3 = None, role3 = None, member: discord.Member = None,guild: discord.Guild = None, ):
    #     guild = ctx.guild if not guild else guild
    #     member = ctx.author if not member else member
    #     emb = discord.Embed(title='**React for role**', colour=member.color)
    #     await ctx.channel.purge(limit=1)
    #
    #     mongo_url = "mongodb+srv://OOp:Armannikoyan2004@triangled.zexks.mongodb.net/servers?retryWrites=true&w=majority"
    #     cluster = MongoClient(mongo_url)
    #     db = cluster["servers"]
    #     collection = db["reaction"]
    #     author_id = ctx.author.id
    #     guild_id = ctx.guild.id
    #
    #     if emoji1 is None:
    #         emb.set_author(name=guild, icon_url=guild.icon_url)
    #         emb.add_field(name = "Error", value = "You need to input 1st emoji")
    #     elif role1 is None:
    #         emb.set_author(name=guild, icon_url=guild.icon_url)
    #         emb.add_field(name = "Error", value = "You need to input 1st role")
    #     elif emoji2 is not None and role2 is None:
    #         emb.set_author(name=guild, icon_url=guild.icon_url)
    #         emb.add_field(name = "Error", value = "You need to input 2nd role")
    #     elif emoji2 is not None and role2 is None:
    #         emb.set_author(name=guild, icon_url=guild.icon_url)
    #         emb.add_field(name = "Error", value = "You need to input 2nd role")
    #     elif emoji3 is not None and role3 is None:
    #         emb.set_author(name=guild, icon_url=guild.icon_url)
    #         emb.add_field(name = "Error", value = "You need to input 3rd role")
    #     else:
    #         if emoji2 is None and role2 is None:
    #             reaction_INFO = {"_id": guild_id, "authorid": author_id, "messageid": messageid, "emoji1": emoji1, "role1": role1.replace("<@&", "").replace('>', '')}
    #             collection.insert_one(reaction_INFO)
    #         elif emoji3 is None and role3 is None:
    #             reaction_INFO = {"_id": guild_id, "authorid": author_id, "messageid": messageid, "emoji1": emoji1, "role1": role1.replace("<@&", "").replace('>', ''), "emoji2": emoji2, "role2": role2.replace("<@&", "").replace('>', '')}
    #             collection.insert_one(reaction_INFO)
    #         else:
    #             reaction_INFO = {"_id": guild_id, "authorid": author_id, "messageid": messageid, "emoji1": emoji1, "role1": role1.replace("<@&", "").replace('>', ''), "emoji2": emoji2, "role2": role2.replace("<@&", "").replace('>', ''), "emoji3": emoji3, "role3": role3.replace("<@&", "").replace('>', '')}
    #             collection.insert_one(reaction_INFO)
    #
    #     await ctx.send(embed=emb)

    @addrole.error
    async def add_role_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'{ ctx.author.name } please type correct **ex: .addrole @name @role**')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ ctx.author.name } you don''t'' have permission to use this command.')
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ ctx.author.name } please type correct **ex: .addrole @name @role**')

    @removerole.error
    async def remove_role_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'{ ctx.author.name } please type correct **ex: .addrole @name @role**')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't **have permission** to use this command.")
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ ctx.author.name } please type correct **ex: .addrole @name @role**')


def setup(bot):
    bot.add_cog(RoleCommands(bot))
