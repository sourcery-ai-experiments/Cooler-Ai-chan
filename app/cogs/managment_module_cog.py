import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions, Bot, Context

class ManagementModule(commands.Cog):
    """Management module for Ai-Chan. Commands for managing the server."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='exile', help='Kicks someone! +exile @user')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: Context, *, command: str):
        user = await commands.MemberConverter().convert(ctx, command)

        if not user:
            await ctx.send("User not found!")
            return

        await user.kick(reason=None)
        await ctx.send(f"{user.name}#{user.discriminator} has been exiled!")

    @commands.command(name='clear', help='Deletes specified amount of messages. +clear number')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx: Context, amount: str = None):
        if amount is None or not amount.isdigit():
            await ctx.send("Amount must be a number!\n+clear [amount]")
            return

        amount = int(amount)
        # Fetch the messages
        messages = [message async for message in ctx.channel.history(limit=amount + 1)]
        await ctx.channel.delete_messages(messages)
        await ctx.send(f"Deleted {amount} messages", delete_after=5)

    @commands.command(name='say', help='Says something as Ai-Chan. +say text')
    async def say(self, ctx: Context, *, text: str):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(name='showemotes', help='Lists all of a guild emotes.')
    @commands.guild_only()
    async def showemotes(self, ctx: Context):
        guild = ctx.guild
        animated_emotes = [emote for emote in guild.emojis if emote.animated]
        standard_emotes = [emote for emote in guild.emojis if not emote.animated]

        await ctx.send(f"Standard emotes | {len(standard_emotes)}")
        emotes = ''
        for i, emote in enumerate(standard_emotes, 1):
            emotes += f"<:{emote.name}:{emote.id}>"
            if i % 9 == 0:
                await ctx.send(emotes)
                emotes = ''
        if emotes:
            await ctx.send(emotes)

        await ctx.send(f"\nAnimated emotes | {len(animated_emotes)}")
        emotes = ''
        for i, emote in enumerate(animated_emotes, 1):
            emotes += f"<a:{emote.name}:{emote.id}>"
            if i % 9 == 0:
                await ctx.send(emotes)
                emotes = ''
        if emotes:
            await ctx.send(emotes)

    @commands.command(name='setnicks', help='Set new nicknames for users with specific role\nExample: setnicks @role newnickname')
    @commands.guild_only()
    async def setnicks(self, ctx: Context, user_role: discord.Role = None, *, name: str = None):
        await ctx.message.delete()

        if user_role is None:
            await ctx.send("Role not found!")
            return

        for member in user_role.members:
            await member.edit(nick=name if name else member.name)

async def setup(bot: commands.Bot):
    await bot.add_cog(ManagementModule(bot))
