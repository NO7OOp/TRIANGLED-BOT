import discord
from discord.ext import commands
from discord.utils import get
from discord import utils
import pymongo
from pymongo import MongoClient
import config
import os
import io

mongo_url = config.mongo_url
cluster = MongoClient(mongo_url)
db = cluster["servers"]

def get_prefix(bot, message):
    collection = db["prefixes"]
    guild_id = message.guild.id

    gld_id = {"_id": guild_id}

    if collection.count_documents(gld_id) == 0:
        prefix_info = {"_id": guild_id, "Prefix": '.'}
        collection.insert_one(prefix_info)

    pfx = collection.find(gld_id)
    for prefix in pfx:
        cur_prefix = prefix["Prefix"]

    return cur_prefix

bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True)
bot.remove_command('help')

# Bot's status
@bot.event
async def on_ready():
    print(f'{bot.user} is connected')

    await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = 3, name = f' help | invite'))

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config.TOKEN)
