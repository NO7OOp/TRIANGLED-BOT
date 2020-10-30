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

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['usinfo'])
    async def userinfo(self, ctx, member: discord.Member = None, guild: discord.Guild = None):
        member = ctx.author if not member else member
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(description = "**{}'s info**".format(member.mention), colour = member.color)

        collection = db["level-status"]
        guild_id = ctx.guild.id
        author_id = member.id
        myid = str(author_id)
        myid = myid + str(guild_id)

        gld_myid = {"_id": myid}
        gld_id = {"_id": guild_id}

        role_names = []
        for role in member.roles:
            role_names.append(role.name)
        role_names = ', '.join(role_names)

        if collection.count_documents(gld_id) == 0:
            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = "**Status is**", value = '**{}**'.format(member.status).replace('dnd', '**Do not disturb**'))
            emb.add_field(name = '** **', value = '** **')
            if member.activity is not None:
                emb.add_field(name = "**Activity is**", value = '**{}**'.format(member.activity.name))
            else:
                emb.add_field(name = "**Activity is**", value = '**Nothing**')
            emb.add_field(name="**Roles are**", value=f'**{role_names}**')
            emb.set_thumbnail(url = member.avatar_url)
            emb.set_footer( text = 'Was interesting for {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
        else:
            levelstat = collection.find(gld_id)
            for levelstatus in levelstat:
                cur_stat = levelstatus["Status"]

                if cur_stat != 'on' and cur_stat == 'off':
                    emb.set_author(name = guild, icon_url = guild.icon_url)
                    emb.add_field(name = "**Status is**", value = '**{}**'.format(member.status).replace('dnd', '**Do not disturb**'))
                    emb.add_field(name = '** **', value = '** **')
                    if member.activity is not None:
                        emb.add_field(name = "**Activity is**", value = '**{}**'.format(member.activity.name))
                    else:
                        emb.add_field(name = "**Activity is**", value = '**Nothing**')
                    emb.add_field(name="**Roles are**", value=f'**{role_names}**')
                    emb.set_thumbnail(url = member.avatar_url)
                    emb.set_footer( text = 'Was interesting for {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
                elif cur_stat == 'on' and cur_stat != 'off':
                    collection = db["levels"]

                    exp = collection.find(gld_myid)
                    for xp in exp:
                        cur_xp = xp["xp"]

                    lvl = collection.find(gld_myid)
                    for level in lvl:
                        lvl_start = level["Level"]

                    emb.set_author(name = guild, icon_url = guild.icon_url)
                    if collection.count_documents(gld_myid) !=  0:
                        emb.add_field(name = "**Level is**", value = f'**{lvl_start}**')
                        emb.add_field(name = '** **', value = '** **')
                        emb.add_field(name = "**Experience is**", value = f"**{cur_xp}**")
                    else:
                        emb.add_field(name = "**Level is**", value = f'**1**')
                        emb.add_field(name = '** **', value = '** **')
                        emb.add_field(name = "**Experience is**", value = f"**0**")
                    emb.add_field(name = "**Status is**", value = '**{}**'.format(member.status).replace('dnd', '**Do not disturb**'))
                    emb.add_field(name = '** **', value = '** **')
                    if member.activity is not None:
                        emb.add_field(name = "**Activity is**", value = '**{}**'.format(member.activity.name))
                    else:
                        emb.add_field(name = "**Activity is**", value = '**Nothing**')
                    emb.add_field(name="**Roles are**", value=f'**{role_names}**')
                    emb.set_thumbnail(url = member.avatar_url)
                    emb.set_footer( text = 'Was interesting for {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
                else:
                    return

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
        
        collection = db["prefixes"]
        guild_id = ctx.guild.id
        gld_id = {"_id": guild_id}

        pfx = collection.find(gld_id)
        for prefix in pfx:
            cur_prefix = prefix["Prefix"]

        if arg is None:
            emb = discord.Embed(title = f"**For aditional information {cur_prefix}help [command-name]**", colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Message control :wrench:**', value = f'```clear \nmute \nunmute \ninvite```')
            emb.add_field(name = "**Member 👥**", value = f"```\nkick \nban \nunban \nuserinfo \naddrole \nremoverole ```")
            emb.add_field(name = "**Bot's settings 🦾**", value = f"```setprefix \nsetmuterole \nsetwelcomechannel \nsetwelcomerole \nsetlevelchannel \nsetlevelstatus \nsetcommandchannel```", inline = True)
            emb.set_footer(text = 'Was interesting for {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
        elif arg == 'clear' or arg == 'cl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command clear**', value = f"You need to write {cur_prefix}clear or cl then amount as here ``{cur_prefix}clear 1``\nThis command is to delete messages as fast as bot can.")
        elif arg == 'mute':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command mute**', value = f'You need to write {cur_prefix}mute then member as here ``{cur_prefix}mute @member-name``\nThis command is to mute member.')
        elif arg == 'unmute':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command unmute**', value = f'You need to write {cur_prefix}unmute then member as here ``{cur_prefix}unmute @member-name``\nThis command is to unmute member which was muted.')
        elif arg == 'setprefix' or arg == 'setpfx':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command setprefix**', value = f'You need to write {cur_prefix}setprefix or setpfx then prefix as here ``{cur_prefix}setprefix !``\nThis command is to give guild owner to change prefix for this bot.')
        elif arg == 'setmuterole' or arg == 'setmuterl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command setmuterole**', value = f'You need to write {cur_prefix}setmuterole or setmuterl then channel as here ``{cur_prefix}setmuterole @role-name``\nThis command is to give chance to set role for muted users per guild.')
        elif arg == 'setwelcomechannel' or arg == 'setwlch':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command setwelcomechannel**', value = f'You need to write {cur_prefix}setwelcomechannel or setwlch then channel as here ``{cur_prefix}setwelcomechannel #channel-name``\nThis command is to set welcome channel for new users')
        elif arg == 'setwelcomerole' or arg == 'setwlrl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command setwelcomerole**', value = f'You need to write {cur_prefix}setwelcomerole or setwlrl then role as here ``{cur_prefix}setwelcomerole @role-name``\nThis command is to set welcome channel for new users.')
        elif arg == 'setcommandchannel' or arg == 'setcmdch':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command setcommandchannel**', value = f'You need to write {cur_prefix}setcommandchannel or setcmdch then channel as here ``{cur_prefix}setcommandchannel #channel-name``\nThis command is to set command channel.')
        elif arg == 'setlevelchannel' or arg == 'setlvlch':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command setlevelchannel**', value = f'You need to write {cur_prefix}setlevelchannel or setlvlch then channel as here ``{cur_prefix}setlevelchannel #channel-name``\nThis command is to set level channel to show level up embed there.')
        elif arg == 'userinfo' or arg == 'usinfo':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command userinfo**', value = f"You need to write {cur_prefix}userinfo or usinfo then member as here ``{cur_prefix}userinfo @member or {cur_prefix}userinfo``\nThis command is to see a member's info.")
        elif arg == 'kick':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command kick**', value = f'You need to write {cur_prefix}kick then member as here ``{cur_prefix}kick @member``\nThis command is to kick a member.')
        elif arg == 'ban':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command ban**', value = f'You need to write {cur_prefix}ban then member as here ``{cur_prefix}ban @member``\nThis command is to ban a member.')
        elif arg == 'unban':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command unban**', value = f'You need to write {cur_prefix}unban then member as here ``{cur_prefix}unban @member``\nThis command is to unban a member.')
        elif arg == 'addrole' or arg == 'addrl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command addrole**', value = f"You need to write {cur_prefix}addrole or addrl then member  and role as here ``{cur_prefix}addrole @member @role``\nThis command is to add role to a member")
        elif arg == 'removerole' or arg == 'removerl':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command removerole**', value = f"You need to write {cur_prefix}removerole or removerl then member and role as here ``{cur_prefix}removerole @member @role``\nThis command is to remove role from a member")
        elif arg == 'invite' or arg == 'link':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command invite**', value = f"You need to write {cur_prefix}invite or link then bot or server as here ``{cur_prefix}invite bot/server``\nThis command is to get bot's or server's link")
        elif arg == 'setlevelstatus' or arg == 'setlvlst':
            emb = discord.Embed(colour = embcolor)

            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Help with command setlevelstatus**', value = f"You need to write {cur_prefix}setlevelstatus or setlvlst then on or off as here ``{cur_prefix}setlvlst on [to use level system]/[to turn off that fu*ken leveling system]``\nThis command is to turn on or turn off leveling system")
        else:
            emb = discord.Embed(colour = 0xff0000)
            emb.set_author(name = guild, icon_url = guild.icon_url)
            emb.add_field(name = '**Error**', value = f"Something went wrong, please try again correctly.")

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @commands.command(aliases = ['setcmdch'])
    @commands.has_permissions(administrator = True)
    async def setcommandchannel(self, ctx, channel, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        
        collection = db["command-channels"]
        guild_id = ctx.guild.id
        cmd_ch = int(channel.replace("<#", "").replace(">", ""))

        gld_id = {"_id": guild_id}
        cmdch = {"Command_channel": cmd_ch}

        if collection.count_documents({}) == 0:
            cmd_info = {"_id": guild_id, "Command_channel": cmd_ch}
            collection.insert_one(cmd_info)

        if collection.count_documents(gld_id) == 0:
            cmd_info = {"_id": guild_id, "Command_channel": cmd_ch}
            collection.insert_one(cmd_info)

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]
            new_channel = cmd_ch

        if collection.count_documents(gld_id) == 0:
            collection.update({"_id": guild_id}, {"$set": {"Command_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's command channel have been setted to: **{channel}")
        elif cur_channel == cmd_ch:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's command channel already is: **{channel}")
        elif cur_channel is not None:
            collection.update({"_id": guild_id}, {"$set": {"Command_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's command channel have been changed to: **{channel}")
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @setcommandchannel.error
    async def setcommandchannel_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setcmdch #channel**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setcmdch #channel**' )

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ ctx.author.name } something gone wrong make sure that you have wrote the name correctly **ex: .userinfo @name**|make sure that user is the part of this server.')

def setup(bot):
    bot.add_cog(Commands(bot))
