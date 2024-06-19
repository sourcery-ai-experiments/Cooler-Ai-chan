import discord
from discord.ext import commands
from app.config import Config
import os
from app.utils.logger import logger
from app.services.database_service import DatabaseService
from app.discord_games.tic_tac_toe.tic_tac_toe import start_tic_tac_toc
#from app.discord_games.tic_tac_toe.tic_tac_toe import start_tic_tac_toc
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.guilds = True
intents.presences = True  # Enable the presences intent
database = DatabaseService()

bot = commands.Bot(command_prefix=Config.PREFIX, intents=intents)
bot.bot_id = None  # Initialize bot_id

@bot.event
async def on_ready():
    logger.info("------")
    logger.info("Cooler AI-Chan is Up and ready!")

    bot.bot_id = bot.user.id  # Set bot's user ID
    logger.info(f"Bot ID is {bot.bot_id}")
    logger.debug(f"Bot environment is set to {Config.ENVIROMENT}")

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

#@bot.tree.command(name="tic_tac_toe")
#async def tic_tac_toe(interaction: discord.Interaction, difficulty: str):
#    bot.loop.create_task(start_tic_tac_toc(interaction, difficulty))

@bot.tree.command(name="ping", description="Ping the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="tic_tac_toe")
async def tic_tac_toe(interaction: discord.Interaction, difficulty: str):
    bot.loop.create_task(start_tic_tac_toc(interaction, difficulty))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
