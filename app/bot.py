import discord
from discord.ext import commands
from app.config import Config
import os
from app.utils.logger import logger

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.guilds = True
intents.presences = True  # Enable the presences intent

bot = commands.Bot(command_prefix=Config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    logger.info("------")
    logger.info("Cooler AI-Chan is Up and ready!")
    

    try:
        await bot.tree.sync(guild=discord.Object(id=Config.GUILD_ID))
        logger.debug("Commands synced successfully!")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")
        
@bot.event
async def on_command(ctx):
    user = ctx.author
    command = ctx.command
    channel = ctx.channel
    params = {param: value for param, value in ctx.kwargs.items()}
    params.update({param: value for param, value in zip(command.clean_params, ctx.args[2:])})
    logger.info(f"Command '{command}' used by '{user}' in channel '{channel}' with params: {params}")


async def load_cogs():
    cogs_loaded = []
    for root, dirs, files in os.walk('./app'):
        for filename in files:
            if filename.endswith('_cog.py') or filename == 'help_cog.py':
                relative_path = os.path.relpath(root, './app').replace(os.path.sep, '.')
                module_name = f'app.{relative_path}.{filename[:-3]}' if relative_path != '.' else f'app.{filename[:-3]}'
                try:
                    await bot.load_extension(module_name)
                    cogs_loaded.append(module_name)
                except Exception as e:
                    logger.error(f"Failed to load cog {module_name}: {e}")
    logger.info("Loaded cogs: " + ", ".join(cogs_loaded))

async def main():
    async with bot:
        await load_cogs()
        await bot.start(Config.DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())