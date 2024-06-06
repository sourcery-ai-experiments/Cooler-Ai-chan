import discord
from discord.ext import commands
# from app.utils.database import update_exp
# from app.utils.vector_db import save_to_vector_db
#from app.utils.helpers import calculate_exp_bonus

class ExpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Save message to vector database
        #save_to_vector_db(message.content, message.author.id)

        # Update EXP
        exp = 1 + calculate_exp_bonus()
        update_exp(message.author.id, exp)

async def setup(bot):
    await bot.add_cog(ExpSystem(bot))
