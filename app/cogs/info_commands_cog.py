import os
import discord
from discord.ext import commands
from app.utils.logger import logger
from app.services.database_service import DatabaseService
class InfoModule(commands.Cog):
    """Contains all needed commands, get information about servers, users, and Ai-Chan."""
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()

    @commands.hybrid_command(name='latency', description="Shows Ai-Chan's response time.")
    async def latency(self, ctx):
        await ctx.send(f"My response time is {round(self.bot.latency * 1000)} ms. 🏓")

    

    @commands.hybrid_command(name="ping", description="Ping the bot")
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")
        
    @commands.hybrid_command(name='botinfo', help="Shows Ai-Chan's statistics.")
    async def botinfo(self, ctx):
        users = sum(guild.member_count for guild in self.bot.guilds)

        embed = discord.Embed(color=discord.Color.purple())
        embed.set_author(name="Ai-Chan", icon_url=self.bot.user.display_avatar.url)
        embed.add_field(name="🏠 Guilds", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 Users", value=users, inline=True)
        embed.add_field(name="🔹 Prefix", value="+", inline=True)
        embed.add_field(name="🕒 Created", value=self.bot.user.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=True)
        embed.add_field(name="🆔 ID", value=self.bot.user.id, inline=True)
        embed.set_footer(text="Powered by Ai-Chan", icon_url=self.bot.user.display_avatar.url)

        await ctx.send(embed=embed)

        # Function to count lines in Python files
    def count_python_lines(directory):
        total_lines = 0
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        total_lines += sum(1 for _ in f)
        return total_lines

    # Custom command to show total lines of Python code
    @commands.hybrid_command(name='total_lines', help='Shows the total number of lines of Python code in the app folder.')
    async def total_lines(self, ctx):
        # Adjust this line to point to the 'app' directory specifically
        app_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
        total_lines = 0
        for root, _, files in os.walk(app_directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        total_lines += sum(1 for _ in f)

        await ctx.send(f"The total number of lines of Python code is {total_lines}.")


    @commands.hybrid_command(name='userinfo', help="Shows user's information\n+userinfo [user]")
    async def userinfo(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author

        roles = " | ".join([role.mention for role in user.roles if role.name != "@everyone"])

        status_colors = {
            discord.Status.online: discord.Color.green(),
            discord.Status.offline: discord.Color.red(),
            discord.Status.idle: discord.Color.orange(),
            discord.Status.dnd: discord.Color.red()
        }

        status_emojis = {
            discord.Status.online: "🟢",
            discord.Status.offline: "🔴",
            discord.Status.idle: "🌙",
            discord.Status.dnd: "⛔"
        }

        info = self.database.get_level_info(user.id)
        total_exp = info[2]

        embed = discord.Embed(color=status_colors.get(user.status, discord.Color.default()))
        embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.display_avatar.url)
        embed.add_field(name="📅 Joined", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=True)
        embed.add_field(name="🕒 Registered", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=True)
        embed.add_field(name=f"{status_emojis.get(user.status)} Status", value=user.status, inline=False)
        # total exp of user
        embed.add_field(name="🔹 Total Exp, requested by Baka", value=total_exp, inline=True)
        embed.add_field(name="🔷 Roles", value=roles if roles else "No roles", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}", icon_url=user.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='serverinfo', help="Shows information about the current guild.")
    async def serverinfo(self, ctx):
        guild = ctx.guild

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=True)
        embed.add_field(name="📁 Channel categories", value=len(guild.categories), inline=True)
        embed.add_field(name="💬 Text channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="🔊 Voice channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="😃 Emotes", value=len(guild.emojis), inline=True)
        embed.add_field(name="🆔 ID", value=guild.id, inline=True)
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(name="👑 Owner", value=f"{guild.owner.name}#{guild.owner.discriminator}", inline=True)
        embed.add_field(name="📛 Owner's ID", value=guild.owner.id, inline=True)
        embed.add_field(name="🔷 Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="💎 Boost tier", value=guild.premium_tier, inline=True)
        embed.add_field(name="🚀 Boosts", value=guild.premium_subscription_count, inline=True)
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"Guild ID: {guild.id}", icon_url=guild.icon.url)

        await ctx.send(embed=embed)


    @commands.hybrid_command(name='avatar', help="Sends link to user's avatar.")
    async def avatar(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.display_avatar.url)
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}", icon_url=user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(InfoModule(bot))