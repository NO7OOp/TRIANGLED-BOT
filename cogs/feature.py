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

class Feature(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['ava'])
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            emb = discord.Embed(title = "Download", url = f"{ctx.author.avatar_url}", colour = ctx.author.color)
            emb.set_image(url = ctx.author.avatar_url)
        else:
            emb = discord.Embed(title = "Download", url = f"{member.avatar_url}", colour = member.color)
            emb.set_image(url = member.avatar_url)
        
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

    @commands.command(aliases = ['link'])
    async def invite(self, ctx, which = None):
        if which is None:
            emb = discord.Embed(colour = 0xff0000)
            emb.add_field(name = f"Error", value = "you need to write which link you want! support server or bot invite link [server/bot]")
        elif which == 'server':
            emb = discord.Embed(colour = 0x55ffee)
            emb = discord.Embed(title = 'Support server link', url = 'https://discord.gg/fUmt4BT')
        elif which == 'bot':
            emb = discord.Embed(colour = 0x55ffee)
            emb = discord.Embed(title = 'Bot invite link', url = 'https://discord.com/api/oauth2/authorize?client_id=745225990850215966&permissions=8&scope=bot')
        
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

def setup(bot):
    bot.add_cog(Feature(bot))