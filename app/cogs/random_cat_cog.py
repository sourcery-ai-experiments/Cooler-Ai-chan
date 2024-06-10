import discord
from discord.ext import commands
from app.services.database_service import DatabaseService
class RandomCatModule(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = DatabaseService()

    @commands.command(name='addkitty', help='Add a link to randomkitty database!\nExample: addkitty https://i.imgur.com/lQcGEtY.png')
    async def add_kitty(self, ctx: commands.Context, *, link: str):
        await ctx.message.delete()
        self.database.add_picture("kitty", link)
        await ctx.send(f"{ctx.message.author.mention} has added a new kitty!\n{link}")

    @commands.command(name='randomkitty', help='Random kitty is back!')
    async def random_kitty(self, ctx: commands.Context):
        link = self.database.get_random_picture("kitty")
        if link:
            await ctx.send(link)
        else:
            await ctx.send("No kitties found in the database!")

    @commands.command(name='addneko', help='Add a link to anime neko database!\nExample: addneko https://i.imgur.com/KxBmblj.jpg')
    async def add_neko(self, ctx: commands.Context, *, link: str):
        await ctx.message.delete()
        self.database.add_picture("neko", link)
        await ctx.send(f"{ctx.message.author.mention} has added a new neko!\n{link}")

    @commands.command(name='randomneko', help='Random anime neko is also back!')
    async def random_neko(self, ctx: commands.Context):
        link = self.database.get_random_picture("neko")
        if link:
            await ctx.send(link)
        else:
            await ctx.send("No nekos found in the database!")

    @commands.command(name='shownekos', help='Shows all nekos')
    async def show_nekos(self, ctx: commands.Context):
        links = self.database.get_pictures("neko")
        if links:
            for i, link in enumerate(links):
                await ctx.send(f"{i}. {link}")
        else:
            await ctx.send("No nekos found in the database!")

    @commands.command(name='showkitties', help='Shows all kitties')
    async def show_kitties(self, ctx: commands.Context):
        links = self.database.get_pictures("kitty")
        if links:
            for i, link in enumerate(links):
                await ctx.send(f"{i}. {link}")
        else:
            await ctx.send("No kitties found in the database!")

async def setup(bot: commands.Bot):
    await bot.add_cog(RandomCatModule(bot))
