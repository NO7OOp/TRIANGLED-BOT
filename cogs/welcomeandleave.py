import discord
from discord.ext import commands
from discord import utils
from discord.utils import get
import sys
import pymongo
from pymongo import MongoClient

sys.path.insert(1, '../TRIANGLED')
import config

mongo_url = config.mongo_url
cluster = MongoClient(mongo_url)
db = cluster["servers"]

class WelcomeAndLeave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Auto role
    @commands.Cog.listener()
    async def on_member_join( self, member ):
        emb = discord.Embed( colour = 0x55ffee )

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

        if collection.count_documents(gld_id) !=  0:
            role = discord.utils.get( member.guild.roles, id = cur_wlrole )
            await member.add_roles( role )
        else:
            return

        emb.set_author( name = guild.name, icon_url = guild.icon_url )
        emb.add_field( name = "**Say Hello to**", value = '**{}**'.format( member.mention ), inline = False )
        emb.set_thumbnail( url = member.avatar_url )

        await channel.send( embed = emb)

    #Cool Removing
    @commands.Cog.listener()
    async def on_member_remove( self, member ):
        emb = discord.Embed( colour = 0xff0000  )

        collection = db["welcome-channels"]
        guild_id = member.guild.id
        guild = member.guild
        author_id = member.id
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

        role_names = []
        for role in member.roles:
            role_names.append(role.name)
        role_names = ', '.join(role_names)

        if collection.count_documents(gld_myid) !=  0:
            user_info = {"_id": myid, "AuthorID": author_id, "GuildID": guild_id, "Level": lvl_start, "xp": cur_xp}
            collection.delete_one(user_info)
            emb.set_author( name = guild.name, icon_url = guild.icon_url )
            emb.add_field( name = "**Say GoodBye to**", value = '**{}**'.format( member.mention ), inline = False )
            emb.add_field(name = "**Level was**", value = f'**{lvl_start}**')
            emb.add_field(name = "** **", value = '** **')
            emb.add_field(name = "**Experience was**", value = f"**{cur_xp}**")
            emb.set_thumbnail( url = member.avatar_url )
            emb.add_field(name="**Roles were**", value=f'**{role_names}**')
        else:
            emb.set_author( name = guild.name, icon_url = guild.icon_url )
            emb.add_field( name = "**Say GoodBye to**", value = '**{}**'.format( member.mention ), inline = False )
            emb.add_field(name = "**Level was**", value = f'**1**', inline = False)
            emb.add_field(name = "** **", value = '** **')
            emb.add_field(name = "**Experience was**", value = f"**0**", inline = False)
            emb.set_thumbnail( url = member.avatar_url )
            emb.add_field(name="**Roles were**", value=f'**{role_names}**')

        await channel.send( embed = emb)

    @commands.command(aliases = ['setwlch'])
    @commands.has_permissions(administrator = True)
    async def setwelcomechannel(self, ctx, channel, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        
        collection = db["welcome-channels"]
        guild_id = ctx.guild.id
        wl_ch = int(channel.replace("<#", "").replace(">", ""))

        gld_id = {"_id": guild_id}

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

        if collection.count_documents == 0:
            collection.update({"_id": guild_id}, {"$set": {"Welcome_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's welcome channel have been setted to: **{channel}")
        if cur_channel == wl_ch:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's welcome channel already is: **{channel}")
        elif cur_channel is not None:
            collection.update({"_id": guild_id}, {"$set": {"Welcome_channel": new_channel}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's welcome channel have been changed to: **{channel}")
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


    @commands.command(aliases = ['setwlrl'])
    @commands.has_permissions(administrator = True)
    async def setwelcomerole(self, ctx, role, guild: discord.Guild = None):
        guild = ctx.guild if not guild else guild
        emb = discord.Embed(colour = 0x55ffee)
        
        collection = db["welcome-roles"]
        wl_role = int(role.replace("<@&", "").replace(">", ""))
        guild_id = ctx.guild.id

        gld_id = {"_id": guild_id}

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

        if cur_wlrole == wl_role:
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Error**", value = f"**Your server's welcome role already is: **{role}")
        elif cur_wlrole is not None:
            collection.update({"_id": guild_id}, {"$set": {"Welcome_role": new_role}})
            emb.set_author(name = guild.name, icon_url = guild.icon_url)
            emb.add_field(name = "**Successful**", value = f"**Your server's welcome role have been changed to: **{role}")
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

def setup(bot):
    bot.add_cog(WelcomeAndLeave(bot))
