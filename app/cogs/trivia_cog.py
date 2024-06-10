import discord
from discord.ext import commands
import random
import aiohttp

class TriviaApis:
    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.content_type == 'application/json':
                    return await response.json()
                return await response.text()

    async def number_api_result(self, number, trivia_type):
        url = f"http://numbersapi.com/{number}/{trivia_type}"
        return await self.fetch(url)

    async def meow_api_result(self):
        url = "https://meowfacts.herokuapp.com/"
        return await self.fetch(url)

    async def dogs_api_result(self):
        url = "https://dog-api.kinduff.com/api/facts"
        return await self.fetch(url)

    async def jservice_api_result(self, category_id):
        url = f"https://jservice.io/api/random?count=1&category={category_id}"
        return await self.fetch(url)

class TriviaModule(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.trivia_apis = TriviaApis()

    @commands.command(name='numbers', help='Posts random facts about numbers.\n+trivia numbers <number> <trivia|math|date|year>')
    async def numbers(self, ctx: commands.Context, *objects):
        number = objects[0] if len(objects) > 0 else ""
        trivia_type = objects[1] if len(objects) > 1 else ""
        result = await self.trivia_apis.number_api_result(number, trivia_type)
        await ctx.send(result)

    @commands.command(name='cats', help='Random facts about cats. Meow!')
    async def cats(self, ctx: commands.Context):
        result = await self.trivia_apis.meow_api_result()
        if isinstance(result, dict) and 'data' in result:
            fact = result['data'][0]
        else:
            fact = "No fact available at the moment."
        await ctx.send(f"🐱 **Cat Fact**: {fact}")


    @commands.command(name='dogs', help='Mad barkers trivias!')
    async def dogs(self, ctx: commands.Context):
        result = await self.trivia_apis.dogs_api_result()
        if isinstance(result, dict) and 'facts' in result:
            fact = result['facts'][0]
        else:
            fact = "No fact available at the moment."
        await ctx.send(f"🐶 **Dog Fact**: {fact}")

    @commands.command(name='sport', help='Sports facts.')
    async def sports(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("42")
        await ctx.send(result)

    @commands.command(name='animals', help='Everything about animals.')
    async def animals(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("21")
        await ctx.send(result)

    @commands.command(name='colors', help='Colors trivias!')
    async def colors(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("36")
        await ctx.send(result)

    @commands.command(name='insects', help='For entomologists.')
    async def insects(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("35")
        await ctx.send(result)

    @commands.command(name='tv', help='Random TV-series facts.')
    async def television(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("67")
        await ctx.send(result)

    @commands.command(name='business', help='Business & Industry trivias.')
    async def business(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("176")
        await ctx.send(result)

    @commands.command(name='words', help='Etymology - The origins of some words.')
    async def words(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("223")
        await ctx.send(result)

    @commands.command(name='anatomy', help='Leave the frogs alone!')
    async def anatomy(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("356")
        await ctx.send(result)

    @commands.command(name='measures', help='Trivias about all kind of units.')
    async def measures(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("420")
        await ctx.send(result)

    @commands.command(name='history', help='History facts.')
    async def history(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("114") if random.randint(0, 1) == 0 else await self.trivia_apis.jservice_api_result("530")
        await ctx.send(result)

    @commands.command(name='food', help='Facts about nom noming.')
    async def food(self, ctx: commands.Context):
        result = await self.trivia_apis.jservice_api_result("777") if random.randint(0, 1) == 0 else await self.trivia_apis.jservice_api_result("49")
        await ctx.send(result)

    @commands.command(name='people', help='Reasons why famous people are famous.')
    async def people(self, ctx: commands.Context):
        choices = ["442", "1478", "4138"]
        result = await self.trivia_apis.jservice_api_result(random.choice(choices))
        await ctx.send(result)

    @commands.command(name='literature', help='Category for book-worms.')
    async def literature(self, ctx: commands.Context):
        choices = ["574", "10", "779", "484"]
        result = await self.trivia_apis.jservice_api_result(random.choice(choices))
        await ctx.send(result)

    @commands.command(name='science', help='Random knowledge and trivias about science.')
    async def science(self, ctx: commands.Context):
        choices = ["25", "23526", "579", "1087", "2046", "950"]
        result = await self.trivia_apis.jservice_api_result(random.choice(choices))
        await ctx.send(result)

    @commands.command(name='fashion', help='Interesting facts about fashion.')
    async def fashion(self, ctx: commands.Context):
        choices = ["26", "383", "1735", "953"]
        result = await self.trivia_apis.jservice_api_result(random.choice(choices))
        await ctx.send(result)

    @commands.command(name='geography', help='Facts about places around the globe.')
    async def geography(self, ctx: commands.Context):
        choices = ["582", "534", "88", "1479"]
        result = await self.trivia_apis.jservice_api_result(random.choice(choices))
        await ctx.send(result)

async def setup(bot: commands.Bot):
    await bot.add_cog(TriviaModule(bot))
