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
                await self.bot.tree.sync()
                await ctx.send("Commands synced successfully!")
            except Exception as e:
                await ctx.send(f"Failed to sync commands: {e}")
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
