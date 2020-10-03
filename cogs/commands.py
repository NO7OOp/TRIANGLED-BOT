import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys

import pymongo
from pymongo import MongoClient

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # User info
    @commands.command(aliases = ['usinfo'])
    async def userinfo(self, ctx, member: discord.Member = None, guild: discord.Guild = None):
        member = ctx.author if not member else member
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(description="**{}'s info**".format(
            member.mention), colour=member.color)
        await ctx.channel.purge(limit=1)
        channel = ctx.channel.id

        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["levels"]
        guild_id = ctx.guild.id
        author_id = member.id
        author = member
        myid = str(author_id)
        myid = myid + str(guild_id)

        gld_myid = {"_id": myid}
        gld_id = {"_id": guild_id}

        exp = collection.find(gld_myid)
        for xp in exp:
            cur_xp = xp["xp"]

        lvl = collection.find(gld_myid)
        for level in lvl:
            lvl_start = level["Level"]

        emb.set_author(name=guild, icon_url=guild.icon_url)
        emb.add_field(name="**Level is**", value=f'**{lvl_start}**')
        emb.add_field(name='** **', value='** **')
        emb.add_field(name="**Experience is**", value=f"**{cur_xp}**")
        emb.add_field(name="**Status is**", value='**{}**'.format(
            member.status).replace('dnd', '**Do not disturb**'))
        emb.add_field(name='** **', value='** **')
        if member.activity is not None:
            emb.add_field(name="**Activity is**", value='**{}**'.format(member.activity.name))
        else:
            emb.add_field(name="**Activity is**".format(
                member.mention), value='**Nothing**')
        emb.add_field(name="**Roles are**", value='**{}**'.format(member.roles).replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace("'", '').replace('Role', '').replace('id=', '').replace(
            'name=', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('"', '').replace("ud", ''), inline=False)
        emb.set_thumbnail(url=member.avatar_url)

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
    async def help(self, ctx, arg = None, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        embcolor = 0x55ffee
        await ctx.channel.purge(limit=1)
        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["prefixes"]
        guild_id = ctx.guild.id
        author = ctx.author
        gld_id = {"_id": guild_id}

        pfx = collection.find(gld_id)
        for prefix in pfx:
            cur_prefix = prefix["Prefix"]

        if arg is None:
            emb = discord.Embed(title=f"**For aditional information {cur_prefix}help [command-name]**", colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Message control :wrench:**', value=f'```{cur_prefix}clear \n{cur_prefix}warn \n{cur_prefix}mute \n{cur_prefix}unmute```')
            emb.add_field(name = "**Bot's settings 🦾**", value = f"```{cur_prefix}setprefix \n{cur_prefix}setmute\n{cur_prefix}setwlch\n{cur_prefix}setwlrole\n{cur_prefix}setlevelch\n{cur_prefix}setcmdch```")
            emb.add_field(name = "**Member 👥**", value = f"```\n{cur_prefix}kick\n{cur_prefix}ban\n{cur_prefix}unban\n{cur_prefix}userinfo\n```")
            emb.add_field(name = "**Role control 🛂**", value = f"```{cur_prefix}addrole \n{cur_prefix}removerole\n```")
            emb.set_footer(text='Was interesting for {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        elif arg == 'clear' or arg == 'cl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command clear**', value=f"You need to write {cur_prefix}clear then amount as here ``{cur_prefix}clear 1``\nThis command is to delete messages as fast as bot's can.")
        elif arg == 'mute':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command mute**', value=f'You need to write {cur_prefix}mute then member as here ``{cur_prefix}mute @member-name``\nThis command is to mute member.')
        elif arg == 'unmute':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command unmute**', value=f'You need to write {cur_prefix}unmute then member as here ``{cur_prefix}unmute @member-name``\nThis command is to unmute member which was muted.')
        elif arg == 'setprefix' or arg == 'setpfx':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command setprefix**', value=f'You need to write {cur_prefix}setprefix then prefix as here ``{cur_prefix}setprefix !``\nThis command is to give per guild to change its prefix for this bot.')
        elif arg == 'setmute':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command setmute**', value=f'You need to write {cur_prefix}setmute then channel as here ``{cur_prefix}setmute @role-name``\nThis command is to give chance to set role for muted users per guild.')
        elif arg == 'setwelcomechannel' or arg == 'setwlch':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command setwlch**', value=f'You need to write {cur_prefix}setwlch then channel as here ``{cur_prefix}setwlch #channel-name``\nThis command is to set welcome channel for new users')
        elif arg == 'setwelcomerole' or arg == 'setwlrl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command setwlrole**', value=f'You need to write {cur_prefix}setwlrole then role as here ``{cur_prefix}setmute @role-name``\nThis command is to set welcome channel for new users.')
        elif arg == 'setcommandchannel' or arg == 'setcmdch':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command setcmdch**', value=f'You need to write {cur_prefix}setcmdch then channel as here ``{cur_prefix}setcmdch #channel-name``\nThis command is to set command channel.')
        elif arg == 'setlevelchannel' or arg == 'setlvlch':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command setcmd**', value=f'You need to write {cur_prefix}setlevelch then channel as here ``{cur_prefix}setlevelch #channel-name``\nThis command is to set level channel to show level up embed there.')
        elif arg == 'userinfo' or arg == 'usinfo':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command userinfo**', value=f"You need to write {cur_prefix}userinfo then member as here ``{cur_prefix}userinfo @member or {cur_prefix}userinfo``\nThis command is to see a member's info.")
        elif arg == 'kick':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command kick**', value=f'You need to write {cur_prefix}kick then member as here ``{cur_prefix}kick @member``\nThis command is to kick a member.')
        elif arg == 'ban':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command ban**', value=f'You need to write {cur_prefix}ban then member as here ``{cur_prefix}ban @member``\nThis command is to ban a member.')
        elif arg == 'unban':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command unban**', value=f'You need to write {cur_prefix}unban then member as here ``{cur_prefix}unban @member``\nThis command is to unban a member.')
        elif arg == 'addrole' or arg == 'addrl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command addrole**', value=f"You need to write {cur_prefix}addrole then member  and role as here ``{cur_prefix}addrole @member @role``\nThis command is to add role to a member")
        elif arg == 'removerole' or arg == 'removerl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Help with command removerole**', value=f"You need to write {cur_prefix}removerole then member and role as here ``{cur_prefix}removerole @member @role``\nThis command is to remove role from a member")
        else:
            emb = discord.Embed(colour = 0x55ffee)

            emb.set_author(name=guild, icon_url=guild.icon_url)
            emb.add_field(name='**Error**', value=f"Something went wrong, please try again correctly.")

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ ctx.author.name } something gone wrong make sure that you have wrote the name correctly **ex: .userinfo @name** or make sure that user is the part of this server.')


def setup(bot):
    bot.add_cog(Commands(bot))
