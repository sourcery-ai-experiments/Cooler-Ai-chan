import discord
from discord.ext import commands
#from app.config import Config
from app.utils.logger import logger

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sync_commands')
    async def sync_commands(self, ctx):
        if str(ctx.author.id) == "240561468330737665":
            try:
                # Attempt to sync the commands and log each one
                synced_commands = await self.bot.tree.sync()
                logger.info("Commands synced successfully!")
                logger.info(f"Synced commands: {', '.join([command.name for command in synced_commands])}")
            except discord.errors.Forbidden as e:
                logger.error(f"Failed to sync commands due to permission error: {e}")
                # Log detailed info about permissions
                for guild in self.bot.guilds:
                    logger.info(f"Checking permissions for guild: {guild.name} ({guild.id})")
                    bot_member = guild.get_member(self.bot.user.id)
                    if bot_member is not None:
                        permissions = bot_member.guild_permissions
                        logger.info(f"Bot permissions in {guild.name}: {permissions}")
                        if not permissions.administrator:
                            logger.warning(f"Bot does not have administrator permissions in {guild.name}")
                    else:
                        logger.warning(f"Bot is not a member of the guild {guild.name}")
            except discord.errors.HTTPException as e:
                logger.error(f"Failed to sync commands due to HTTP error: {e}")
            except Exception as e:
                logger.error(f"Failed to sync commands: {e}")
        else:
            await ctx.send("You do not have permission to use this command.")

    @commands.command(name='shutdown')
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        logger.info("Bot is shutting down.")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(General(bot))
