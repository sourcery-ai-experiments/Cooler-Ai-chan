import discord
from discord.ext import commands
from app.utils.chatgpt_api import send_to_openai

class AICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ask')
    async def ask(self, ctx, *, question):
        response = send_to_openai([{"role": "user", "content": question}])
        await ctx.send(response[0])

async def setup(bot):
    await bot.add_cog(AICommands(bot))
