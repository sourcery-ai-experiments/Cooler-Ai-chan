import discord
from discord.ext import commands
from app.services.database_service import DatabaseService

class DatabaseModule(commands.Cog):
    """Pls do not mess with it
    """
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()

    @commands.command(name='levelinfo')
    async def get_user(self, ctx):
        user_id = ctx.author.id
        info = self.database.get_level_info(user_id)
        await ctx.send(f"Gozaimas! o/ How's grinding?\nLevel: {info[0]}\nExperience: {info[1]}\nTotal Experience: {info[2]}")

    @commands.command(name='aichaninfo')
    async def aichan_info(self, ctx):
        aichan_id = 452541322667229194
        info = self.database.get_level_info(aichan_id)
        await ctx.send(f"Here my stats! OwO\nLevel: {info[0]}\nExperience: {info[1]}")

    @commands.command(name='leaderboard')
    async def get_leaderboard(self, ctx):
        leaderboard = self.database.get_leaderboard()
        await ctx.send(leaderboard)

    @commands.command(name='addexp')
    async def add_exp(self, ctx, number: str):
        try:
            amount = int(number)
            level_up = self.database.add_exp(ctx.author.id, amount)
            await ctx.send(f"Added {amount} exp.")
            if level_up:
                await ctx.send("Congratulations! You've leveled up to the next level.")
        except ValueError:
            await ctx.send("Invalid number.")

    @commands.command(name='listusers')
    async def list_users(self, ctx):
        self.database.list_users()
        await ctx.send("Listed all users in the console.")

async def setup(bot):
    await bot.add_cog(DatabaseModule(bot))
