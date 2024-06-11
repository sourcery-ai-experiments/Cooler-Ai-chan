import os
import discord
from discord.ext import commands
from app.utils.logger import logger

class HelpModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = None  # Disable the default help command
        self.cog_aliases = {
            "DatabaseModule": "database",
            "AICommands": "aicommands",
            "AnimeCommands": "anime",
            "CommandHandlingService": "command",
            # Add more aliases as needed
        }

    @commands.command(name='help')
    async def custom_help(self, ctx, *, alias: str = None):
        """Displays help information for all commands or a specific cog."""
        if alias:
            # Convert alias back to the cog name
            cog_name = None
            for name, alias_name in self.cog_aliases.items():
                if alias_name == alias:
                    cog_name = name
                    break

            # If no alias match found, try to match with class name (lowercased)
            if not cog_name:
                for name in self.bot.cogs.keys():
                    if name.lower() == alias:
                        cog_name = name
                        break

            if not cog_name:
                await ctx.send(f"No module named '{alias}' found.")
                return

            # Show help for a specific cog
            cog = self.bot.get_cog(cog_name)
            if cog:
                embed = discord.Embed(
                    title=f"Help - {alias.capitalize()}",
                    description=cog.__doc__ or "No description available.",
                    color=discord.Color.blue()
                )
                for command in cog.get_commands():
                    embed.add_field(
                        name=f"🔹 {self.bot.command_prefix}{command.name}",
                        value=command.help or "No description available.",
                        inline=False
                    )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"No module named '{alias}' found.")
        else:
            # Show summary of all cogs
            embed = discord.Embed(
                title="Help",
                description="List of all modules. Use `+help <module>` to see details.",
                color=discord.Color.green()
            )
            for cog_name, cog in self.bot.cogs.items():
                description = cog.__doc__ or "No description available."
                alias = self.cog_aliases.get(cog_name, cog_name.lower())
                embed.add_field(
                    name=f"{alias.capitalize()} | `+help {alias}`",
                    value=f"🔸 {description}",
                    inline=False
                )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpModule(bot))