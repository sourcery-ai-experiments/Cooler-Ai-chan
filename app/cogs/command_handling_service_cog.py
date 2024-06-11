import random
import os
import discord
from discord.ext import commands
from discord.utils import get
from app.services.database_service import DatabaseService
from app.config import Config
from app.utils.logger import logger

class CommandHandlingService(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()
        self.previous_author = None
        logger.info("CommandHandlingService initialized")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Check if the message is a command
        if message.content.startswith(Config.PREFIX):
            return

        # Respond to greetings
        greetings = ["hello", "hi", "yo", "hey", "ohayo", "henlo", "oi", "ahoy"]
        if any(word in message.content.lower().split() for word in greetings):
            logger.debug(f"Greeting detected in message: {message.content}")
            emote = get(self.bot.emojis, name="hi")
            if emote:
                logger.debug(f"Emote 'hi' found: {emote}")
                await message.add_reaction(emote)
            else:
                logger.error("Emote 'hi' not found in the server.")

        # Lottery reaction
        if random.randint(1, 100000) == 1:
            emote = random.choice(message.guild.emojis)
            await message.add_reaction(emote)
            exp_gain = random.randint(10, 100)
            await message.channel.send(f"{message.author.mention}!! You just won a lottery with 0.001% chance! +{exp_gain} exp for you for free!")
            self.database.add_exp(message.author.id, exp_gain)


        # Level up for chatting
        if os.path.exists(self.database.path):
            if self.previous_author != message.author.id:
                level_up, _ = self.database.add_exp(message.author.id, 1)
                if level_up:
                    await message.channel.send(f"🎉 Level Up! 🎉 Congratulations! {message.author.mention}! You leveled up from babbling so much!")
            self.previous_author = message.author.id

        
        # Bad word filter
        if 'badword' in message.content:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, watch your language!')

        # Process commands
        logger.debug(f"Processing commands for message: {message.content}")
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, commands.CommandInvokeError):
            await context.send(f"Error: {str(error)}")

async def setup(bot):  
    await bot.add_cog(CommandHandlingService(bot))
    
