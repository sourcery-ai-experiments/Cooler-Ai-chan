import os
import discord
from discord.ext import commands
from discord.ui import View, Button
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
            "SlotsGame": "slots",
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
                commands = cog.get_commands()
                await self.send_paginated_help(ctx, alias.capitalize(), commands)
            else:
                await ctx.send(f"No module named '{alias}' found.")
        else:
            # Show summary of all cogs
            cog_summaries = [
                (alias.capitalize(), cog.__doc__ or "No description available.")
                for cog_name, cog in self.bot.cogs.items()
                for alias in [self.cog_aliases.get(cog_name, cog_name.lower())]
            ]
            await self.send_paginated_summary(ctx, cog_summaries)

    async def send_paginated_help(self, ctx, title, commands, per_page=10):
        pages = [
            commands[i:i + per_page]
            for i in range(0, len(commands), per_page)
        ]

        if len(pages) == 1:
            embed = self.get_page_embed(pages[0], title, 1, 1)
            await ctx.send(embed=embed)
            return

        current_page = 0
        message = await ctx.send(embed=self.get_page_embed(pages[current_page], title, current_page + 1, len(pages)))

        async def update_page(interaction, increment):
            nonlocal current_page
            current_page += increment
            await interaction.response.edit_message(embed=self.get_page_embed(pages[current_page], title, current_page + 1, len(pages)), view=self.get_page_view(current_page, len(pages), update_page))

        await message.edit(view=self.get_page_view(current_page, len(pages), update_page))

    async def send_paginated_summary(self, ctx, summaries, per_page=10):
        pages = [
            summaries[i:i + per_page]
            for i in range(0, len(summaries), per_page)
        ]

        if len(pages) == 1:
            embed = self.get_summary_page_embed(pages[0], 1, 1)
            await ctx.send(embed=embed)
            return

        current_page = 0
        message = await ctx.send(embed=self.get_summary_page_embed(pages[current_page], current_page + 1, len(pages)))

        async def update_page(interaction, increment):
            nonlocal current_page
            current_page += increment
            await interaction.response.edit_message(embed=self.get_summary_page_embed(pages[current_page], current_page + 1, len(pages)), view=self.get_page_view(current_page, len(pages), update_page))

        await message.edit(view=self.get_page_view(current_page, len(pages), update_page))

    def get_page_embed(self, page, title, current_page, total_pages):
        embed = discord.Embed(
            title=f"Help - {title}",
            color=discord.Color.blue()
        )
        for command in page:
            embed.add_field(
                name=f"🔹 {self.bot.command_prefix}{command.name}",
                value=command.help or "No description available.",
                inline=False
            )
        embed.set_footer(text=f"Page {current_page}/{total_pages}")
        return embed

    def get_summary_page_embed(self, page, current_page, total_pages):
        embed = discord.Embed(
            title="Help",
            color=discord.Color.green()
        )
        for alias, description in page:
            embed.add_field(
                name=f"{alias} | `+help {alias.lower()}`",
                value=f"🔸 {description}",
                inline=False
            )
        embed.set_footer(text=f"Page {current_page}/{total_pages}")
        return embed

    def get_page_view(self, current_page, total_pages, update_page):
        view = View()
        if current_page > 0:
            view.add_item(Button(label="⬅️", style=discord.ButtonStyle.blurple, custom_id="prev"))
        else:
            view.add_item(Button(label="⬅️", style=discord.ButtonStyle.gray, disabled=True))

        if current_page < total_pages - 1:
            view.add_item(Button(label="➡️", style=discord.ButtonStyle.blurple, custom_id="next"))
        else:
            view.add_item(Button(label="➡️", style=discord.ButtonStyle.gray, disabled=True))

        async def button_callback(interaction):
            if interaction.data["custom_id"] == "next":
                await update_page(interaction, 1)
            elif interaction.data["custom_id"] == "prev":
                await update_page(interaction, -1)

        for child in view.children:
            child.callback = button_callback

        return view

async def setup(bot):
    await bot.add_cog(HelpModule(bot))
