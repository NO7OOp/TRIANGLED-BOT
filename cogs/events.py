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

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove( self, guild ):
        
        collection = db["prefixes"]
        guild_id = guild.id

        gld_id = {"_id": guild_id}

        prefix_info = {"_id": guild_id}

        collection.delete_one(prefix_info)

        collection = db["mute-roles"]

        gld_id = {"_id": guild_id}

        if collection.count_documents(gld_id) == 0:
            mtrole_info = {"_id": guild_id}

            collection.delete_one(mtrole_info)
        else:
            return

        collection = db["welcome-channels"]

        gld_id = {"_id": guild_id}

        if collection.count_documents(gld_id) == 0:
            wlch_info = {"_id": guild_id}

            collection.delete_one(wlch_info)
        else:
            return

        collection = db["welcome-roles"]

        gld_id = {"_id": guild_id}

        if collection.count_documents(gld_id) == 0:
            welcomerole_info = {"_id": guild_id}

            collection.delete_one(welcomerole_info)
        else:
            return

        collection = db["command-channels"]

        gld_id = {"_id": guild_id}

        if collection.count_documents(gld_id) == 0:
            cmd_info = {"_id": guild_id}

            collection.delete_one(cmd_info)
        else:
            return

        collection = db["levels"]

        gld_id = {"GuildID": guild_id}
        if collection.count_documents(gld_id) == 0:
            user_info = {"GuildID": guild_id}

            collection.delete_one(user_info)
        else:
            return

        collection = db["level-status"]

        gld_id = {"_id": guild_id}
        if collection.count_documents(gld_id) == 0:
            lvlst_info = {"_id": guild_id}

            collection.delete_one(lvlst_info)
        else:
            return

        collection = db["level-channels"]

        gld_id = {"_id": guild_id}
        if collection.count_documents(gld_id) == 0:
            lvlch_info = {"_id": guild_id}

            collection.delete_one(lvlch_info)
        else:
            return

def setup(bot):
    bot.add_cog(Events(bot))
