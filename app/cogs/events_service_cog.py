import discord
from discord.ext import commands
import os
from app.services.database_service import DatabaseService
from app.utils.logger import logger

class EventsService(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()

        bot.add_listener(self.on_ready, 'on_ready')
        bot.add_listener(self.on_member_update, 'on_member_update')
        bot.add_listener(self.on_member_join, 'on_member_join')

    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                self.database.add_user(member)
        logger.debug("Database populated with current guild members.")

    async def on_member_join(self, member):
        await member.guild.system_channel.send(f"Welcome to the BakaCats {member.name}! (｡◕‿‿◕｡)")
        self.database.add_user(member)

    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            self.database.add_nickname(after.id, after.nick)

async def setup(bot):
    await bot.add_cog(EventsService(bot))
