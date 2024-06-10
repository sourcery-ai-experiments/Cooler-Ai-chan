import discord
from discord.ext import commands
from app.services.database_service import DatabaseService

class KleaveModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()
        self.kleave_id = 145319972992712704

    @commands.command(name='bonuspoint')
    async def bonus_point(self, ctx, user: discord.Member):
        if ctx.author.id != self.kleave_id:
            await ctx.send(f"Oi <@{self.kleave_id}>! Someone is trying to cheat!")
            return

        self.database.add_point(user.id)
        await ctx.send(f"Yay! <@{user.id}> just got a bonus point from Kleaves! n.n")

    @commands.command(name='subtractpoint')
    async def subtract_point(self, ctx, user: discord.Member):
        if ctx.author.id != self.kleave_id:
            await ctx.send(f"Oi <@{self.kleave_id}>! Someone is trying to cheat!")
            return

        self.database.subtract_point(user.id)
        await ctx.send(f"Uwaaah! Rip your point <@{user.id}>! You better rethink your life now.")

    @commands.command(name='points')
    async def points(self, ctx):
        points = self.database.get_points(ctx.author.id)
        await ctx.send(f"Bonuspoints balance: {points}")

async def setup(bot):
    await bot.add_cog(KleaveModule(bot))
