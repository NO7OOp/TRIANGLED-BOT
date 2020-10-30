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

class RoleCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['addrl'])
    @commands.has_permissions(manage_roles = True)
    async def addrole(self, ctx, member: discord.Member = None, role: discord.Role = None, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)

        role_names = []
        for role1 in member.roles:
            role_names.append(role1.name)
        role_names = ', '.join(role_names)

        if role in member.roles:
            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.set_thumbnail(url = member.avatar_url)
            emb.add_field(name = f'Add role',
                        value = f'{member.mention} already have role **{role}**', inline = False)
            emb.add_field(name = f"**Roles were**", value = f"{role_names}")
            emb.set_footer(text = 'Was requested to add by {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
        else:
            await member.add_roles(role)
            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.set_thumbnail(url = member.avatar_url)
            emb.add_field(name = f'Add role',
                        value = f'**{role}** role added to user {member.mention}', inline = False)
            emb.add_field(name = "**Roles were**", value = f'**{role_names}**')
            emb.set_footer(text = 'Was added by {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

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

    @commands.command(aliases = ['removerl'])
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, ctx, member: discord.Member = None, role: discord.Role = None, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)

        role_names = []
        for role1 in member.roles:
            role_names.append(role1.name)
        role_names = ', '.join(role_names)

        if role in member.roles:
            await member.remove_roles(role)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.set_thumbnail(url = member.avatar_url)
            emb.add_field(name = f'Remove role',
                        value = f"**{role}** role removed from {member.mention} user role", inline = False)
            emb.add_field(name = "**Roles were**", value = f'**{role_names}**')
            emb.set_footer(text = 'Was removed by {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
        else:
            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.set_thumbnail(url = member.avatar_url)
            emb.add_field(name = f'Remove role',
                        value = f"{member.mention} don't have role **{role}**", inline = False)
            emb.add_field(name = f"**Roles are**", value = f'**{role_names}**')
            emb.set_footer(text = 'Was requested to remove by {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

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
