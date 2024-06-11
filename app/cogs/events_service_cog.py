import discord
from discord.ext import commands
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
                try:
                    self.database.add_user(member)
                except Exception as e:
                    logger.error(f"Error adding user {member.id}: {e}")
        logger.debug("Database populated with current guild members.")

    async def on_member_join(self, member):
        try:
            await member.guild.system_channel.send(f"Welcome to the BakaCats {member.name}! (｡◕‿‿◕｡)")
            self.database.add_user(member)
        except Exception as e:
            logger.error(f"Error adding new member {member.id}: {e}")

    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            try:
                self.database.add_nickname(after.id, after.nick)
            except Exception as e:
                logger.error(f"Error updating nickname for {after.id}: {e}")

async def setup(bot):
    await bot.add_cog(EventsService(bot))
