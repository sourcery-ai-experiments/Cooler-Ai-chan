import discord
from discord.ext import commands
from app.utils.embeds import create_embed_with_image
from app.utils.helpers import extract_user, user_not_found

class AnimeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='neko')
    async def random_neko(self, ctx):
        embed = await create_embed_with_image("(≈>ܫ<≈)", "https://nekos.life/api/v2/img/neko")
        await ctx.send(embed=embed)

    @commands.command(name='smug')
    async def random_smug(self, ctx):
        embed = await create_embed_with_image("(ಸ‿‿ಸ)", "https://nekos.life/api/v2/img/smug")
        await ctx.send(embed=embed)

    @commands.command(name='slap')
    async def random_slap(self, ctx, *, specified_user: str):
        user = await extract_user(ctx, specified_user)
        if await user_not_found(ctx, user):
            return

        embed = await create_embed_with_image(f"{ctx.author.name} slaps {user.name} (ಸ‿‿ಸ)", "https://nekos.life/api/v2/img/slap")
        await ctx.send(embed=embed)

    @commands.command(name='kiss')
    async def random_kiss(self, ctx, *, specified_user: str):
        user = await extract_user(ctx, specified_user)
        if await user_not_found(ctx, user):
            return

        embed = await create_embed_with_image(f"{ctx.author.name} kisses {user.name} (ꈍᴗꈍ)ε｀*)", "https://nekos.life/api/v2/img/kiss")
        await ctx.send(embed=embed)

    @commands.command(name='poke')
    async def random_poke(self, ctx, *, specified_user: str):
        user = await extract_user(ctx, specified_user)
        if await user_not_found(ctx, user):
            return

        embed = await create_embed_with_image(f"{ctx.author.name} pokes {user.name} ( ๑‾̀◡‾́)σ»", "https://nekos.life/api/v2/img/poke")
        await ctx.send(embed=embed)

    @commands.command(name='hug')
    async def random_hug(self, ctx, *, specified_user: str):
        user = await extract_user(ctx, specified_user)
        if await user_not_found(ctx, user):
            return

        embed = await create_embed_with_image(f"{ctx.author.name} hugs {user.name} (✿˶◕‿◕˶人◕ᴗ◕✿)", "https://nekos.life/api/v2/img/hug")
        await ctx.send(embed=embed)

    @commands.command(name='baka')
    async def random_baka(self, ctx, *, specified_user: str):
        user = await extract_user(ctx, specified_user)
        if await user_not_found(ctx, user):
            return

        embed = await create_embed_with_image(f"{ctx.author.name} thinks {user.name} is baka! (◣_◢)", "https://nekos.life/api/v2/img/baka")
        await ctx.send(embed=embed)

    @commands.command(name='pat')
    async def random_pat(self, ctx, *, specified_user: str):
        user = await extract_user(ctx, specified_user)
        if await user_not_found(ctx, user):
            return

        embed = await create_embed_with_image(f"{ctx.author.name} pats {user.name} (；^＿^)ッ☆(　゜w゜)", "https://nekos.life/api/v2/img/pat")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AnimeCommands(bot))
