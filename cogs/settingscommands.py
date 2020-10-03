import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import sys

import pymongo
from pymongo import MongoClient

class SettingsCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['setpfx'])
    @commands.has_permissions(administrator = True)
    async def setprefix(self, ctx, prefix, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(title='**Prefix**', colour = 0x55ffee)
        await ctx.channel.purge(limit=1)
        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["prefixes"]
        guild_id = ctx.guild.id
        guild_prefix = prefix
        author = ctx.author

        gld_id = {"_id": guild_id}
        gld_prefix = {"Prefix": guild_prefix}

        if collection.count_documents({}) == 0:
            prefix_info = {"_id": guild_id, "Prefix": guild_prefix}
            collection.insert_one(prefix_info)

        if collection.count_documents(gld_id) == 0:
            prefix_info = {"_id": guild_id, "Prefix": guild_prefix}
            collection.insert_one(prefix_info)

        pfx = collection.find(gld_id)
        for prefix in pfx:
            cur_prefix = prefix["Prefix"]
            new_prefix = guild_prefix

        if cur_prefix is not None:
            collection.update({"_id": guild_id}, {"$set": {"Prefix": new_prefix}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's prefix have been changed to: ``{new_prefix}``**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        elif cur_prefix == guild_prefix:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's prefix already is: ``{cur_prefix}``**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)

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
    @commands.has_permissions(administrator = True)
    async def setmute(self, ctx, role, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(title='**Mute role**', colour = 0x55ffee)
        await ctx.channel.purge(limit=1)
        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["mute-roles"]
        guild_id = ctx.guild.id
        mute_role = int(role.replace("<@&", "").replace(">", ""))
        author = ctx.author

        gld_id = {"_id": guild_id}
        mt_role = {"Mute_role": mute_role}

        if collection.count_documents({}) == 0:
            mtrole_info = {"_id": guild_id, "Mute_role": mute_role}
            collection.insert_one(mtrole_info)

        if collection.count_documents(gld_id) == 0:
            mtrole_info = {"_id": guild_id, "Mute_role": mute_role}
            collection.insert_one(mtrole_info)

        mtr = collection.find(gld_id)
        for muterole in mtr:
            cur_role = muterole["Mute_role"]
            new_role = mute_role

        if cur_role is not None:
            collection.update({"_id": guild_id}, {"$set": {"Mute_role": new_role}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's mute role have been changed to: {role}**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        elif cur_role == mute_role:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's mute role already is: {role}**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)


    @commands.command(aliases = ['setwlch'])
    @commands.has_permissions(administrator = True)
    async def setwelcomechannel(self, ctx, channel, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(title='**Welcome channel**', colour = 0x55ffee)
        await ctx.channel.purge(limit=1)
        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["welcome-channels"]
        guild_id = ctx.guild.id
        wl_ch = int(channel.replace("<#", "").replace(">", ""))
        author = ctx.author

        gld_id = {"_id": guild_id}
        wlch = {"Welcome_channel": wl_ch}

        if collection.count_documents({}) == 0:
            wlch_info = {"_id": guild_id, "Welcome_channel": wl_ch}
            collection.insert_one(wlch_info)

        if collection.count_documents(gld_id) == 0:
            wlch_info = {"_id": guild_id, "Welcome_channel": wl_ch}
            collection.insert_one(wlch_info)

        wch = collection.find(gld_id)
        for welcome in wch:
            cur_channel = welcome["Welcome_channel"]
            new_channel = wl_ch

        if cur_channel is not None:
            collection.update({"_id": guild_id}, {"$set": {"Welcome_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's welcome channel have been changed to: **{channel}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        elif cur_channel == wl_ch:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's welcome channel already is: **{channel}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)


    @commands.command(aliases = ['setwlrl'])
    @commands.has_permissions(administrator = True)
    async def setwelcomerole(self, ctx, role, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(title='**Welcome role**', colour = 0x55ffee)
        await ctx.channel.purge(limit=1)
        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["welcome-roles"]
        wl_role = int(role.replace("<@&", "").replace(">", ""))
        author = ctx.author
        guild_id = ctx.guild.id

        gld_id = {"_id": guild_id}
        wlrole = {"Welcome_role": wl_role}

        if collection.count_documents({}) == 0:
            welcomerole_info = {"_id": guild_id, "Welcome_role": wl_role}
            collection.insert_one(welcomerole_info)

        if collection.count_documents(gld_id) == 0:
            welcomerole_info = {"_id": guild_id, "Welcome_role": wl_role}
            collection.insert_one(welcomerole_info)

        wrl = collection.find(gld_id)
        for welcomerole in wrl:
            cur_wlrole = welcomerole["Welcome_role"]
            new_role = wl_role

        if cur_wlrole is not None:
            collection.update({"_id": guild_id}, {"$set": {"Welcome_role": new_role}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's welcome role have been changed to: **{role}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        elif cur_wlrole == wl_role:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's welcome role already is: **{role}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)

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
        emb = discord.Embed(title='**Command channel**', colour = 0x55ffee)
        await ctx.channel.purge(limit=1)
        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["command-channels"]
        guild_id = ctx.guild.id
        cmd_ch = int(channel.replace("<#", "").replace(">", ""))
        author = ctx.author

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

        if cur_channel is not None:
            collection.update({"_id": guild_id}, {"$set": {"Command_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's command channel have been changed to: **{channel}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        elif cur_channel == cmd_ch:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's command channel already is: **{channel}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @commands.command(aliases = ['setlvlch'])
    @commands.has_permissions(administrator = True)
    async def setlevelchannel(self, ctx, channel, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(title='**Level channel**', colour = 0x55ffee)
        await ctx.channel.purge(limit=1)
        mongo_url = ""
        cluster = MongoClient(mongo_url)
        db = cluster["servers"]
        collection = db["role-channels"]
        guild_id = ctx.guild.id
        role_ch = int(channel.replace("<#", "").replace(">", ""))
        author = ctx.author

        gld_id = {"_id": guild_id}
        cmdch = {"Role_channel": role_ch}

        if collection.count_documents({}) == 0:
            role_info = {"_id": guild_id, "Role_channel": role_ch}
            collection.insert_one(role_info)

        if collection.count_documents(gld_id) == 0:
            role_info = {"_id": guild_id, "Role_channel": role_ch}
            collection.insert_one(role_info)

        rolech = collection.find(gld_id)
        for rolechannel in rolech:
            cur_channel = rolechannel["Role_channel"]
            new_channel = role_ch

        if cur_channel is not None:
            collection.update({"_id": guild_id}, {"$set": {"Role_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's level channel have been changed to: **{channel}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        elif cur_channel == cmd_ch:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's level channel already is: **{channel}")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)
        else:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Something went wrong, please try again.**")
            emb.set_footer(text=f"Was requested to change by {author.name}", icon_url=author.avatar_url)

        collection = db["command-channels"]

        cmdch = collection.find(gld_id)
        for cmdchannel in cmdch:
            cur_channel = cmdchannel["Command_channel"]

        if collection.count_documents(gld_id) == 0:
            await ctx.send(embed = emb)
        else:
            channel = self.bot.get_channel( cur_channel )
            await channel.send( embed = emb)

    @setprefix.error
    async def setprefix_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setprefix [prefix]**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setprefix [prefix]**' )

    @setmute.error
    async def setmute_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setmute @role**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setmute @role**' )

    @setwelcomechannel.error
    async def setwelcomechannel_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setwl #channel**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setwl #channel**' )

    @setwelcomerole.error
    async def setwelcomerole_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setwlrole @role**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setwlrole @role**' )

    @setcommandchannel.error
    async def setcommandchannel_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setcmd #channel**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setcmd #channel**' )

    @setlevelchannel.error
    async def setlevelchannel_error( self, ctx, error ):
        if isinstance( error, commands.MissingRequiredArgument ):
            await ctx.send( f'{ ctx.author.name } please type correct **ex: .setlevelch #channel**' )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ ctx.author.name } you don't have ``Administrator`` permission to use this command.")
        if isinstance( error, commands.errors.BadArgument ):
            await ctx.send( f'{ ctx.author.name } you wrote something wrong please try again **ex: .setlevelch #channel**' )

def setup(bot):
    bot.add_cog(SettingsCommands(bot))
