from datetime import datetime, timedelta
import time
import discord
from discord.ext import commands
from app.utils.command_utils import custom_command
from app.services.emojis_service import EmojiService
from app.services.database_service import DatabaseService
from app.services.gambling_service import level_up_message
from app.utils.logger import logger
from app.config import Config
class GuessEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_service = EmojiService()
        self.database = DatabaseService()
        

    @custom_command(name='emojis', help="Play the emoji guessing game! Use once to start, use again to answer.")
    async def emojis(self, ctx, *, input: str = None):
        user_id = ctx.author.id
        print("in emojis command")
        if input is None:
            print("in if from command")
            # Start a new game
            question_data = self.emoji_service.start_game(user_id)
            print(f"after start game from command, question_data: {question_data} (type: {type(question_data)})")
            if question_data is None:
                next_refresh_time = self.calculate_time_remaining()
                embed = discord.Embed(title="Emoji Guessing Game",
                                    description=f"You've used all your attempts. Please wait {next_refresh_time} before trying again.",
                                    color=discord.Color.red())
                await ctx.send(embed=embed)
            elif isinstance(question_data, dict):
                print("in else from command")
                embed = discord.Embed(title="Emoji Guessing Game",
                                    description=f"Here's your emoji question:\n{question_data['question']}\nHint: {question_data.get('hint', 'No hint available')}\nUse the command again with your answer to submit!",
                                    color=discord.Color.blue())
                await ctx.send(embed=embed)
            else:
                print(f"Unexpected question_data format: {question_data} (type: {type(question_data)})")
                embed = discord.Embed(title="Emoji Guessing Game",
                                    description="An error occurred while starting the game. Please try again.",
                                    color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            # Answer the current game
            print("in else from command")
            result = self.emoji_service.answer_game(user_id, input)
            print(f"Result from answer_game: {result} (type: {type(result)})")
            if result is None:
                embed = discord.Embed(title="Emoji Guessing Game",
                                    description="You don't have an active game. Use the command without an answer to start a new game.",
                                    color=discord.Color.orange())
                await ctx.send(embed=embed)
            elif isinstance(result, dict) and result.get('correct'):
                print("in elif from command")
                embed = discord.Embed(title="Emoji Guessing Game",
                                    description=f"Congratulations! You **won 5 exp**.\n{result['comment']}",
                                    color=discord.Color.green())
                await ctx.send(embed=embed)
                # add exp for winner 5 exp
                level_up_after_win, _ = self.database.add_exp(ctx.message.author.id, 5)
                if level_up_after_win:
                    await ctx.send(await level_up_message(ctx))
                    logger.info(f"User {ctx.message.author.id} leveled up after winning the emoji game.")
            else:
                print("in else from command")
                game_data = self.emoji_service.active_games.get(user_id, {})
                correct_answer = game_data.get('answer', 'Unknown')
                embed = discord.Embed(title="Emoji Guessing Game",
                                    description=f"Sorry, that's not correct.\n{result['comment']}",
                                    color=discord.Color.red())
                await ctx.send(embed=embed)



    @custom_command(name='emojisusage', help="Check your emoji game status.")
    async def emojishelp(self, ctx):
        user_id = ctx.author.id
        remaining_usages, not_in_db = self.emoji_service.get_remaining_usages(user_id)

        if remaining_usages >= self.emoji_service.max_stacked_usages:
            description = f"You have {remaining_usages} usages left, which is the maximum limit."
        else:
            if not_in_db:
                description = "You have not played the emoji game yet. Use the `emojis` command to start a new game. **You have 2 uses at start.**"
            else:
                time_remaining_str = self.calculate_time_remaining()
                description = f"You have {remaining_usages} usages left. Next usage available in {time_remaining_str}."

        embed = discord.Embed(
            title="Emoji Guessing Game Status",
            description=description,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    # Calculate time remaining in hours, minutes, and seconds
   

    def calculate_time_remaining(self):
        now = datetime.now()
        print(f"Current time: {now}")

        # Start from today at the reference hour
        reference_time = now.replace(hour=Config.REFERENCE_HOUR, minute=0, second=0, microsecond=0)
        print(f"Base reference time: {reference_time}")

        # Calculate all trigger times for the next 24 hours
        trigger_times = []
        hours_in_day = 24
        for i in range(hours_in_day // self.emoji_service.cooldown_hours):
            trigger_time = reference_time + timedelta(hours=i * self.emoji_service.cooldown_hours)
            if trigger_time <= now:
                trigger_time += timedelta(days=1)
            trigger_times.append(trigger_time)

        print("Next few trigger times:")
        for t in trigger_times[:5]:  # Print only the next 5 for brevity
            print(f"  {t}")

        # Find the next trigger time
        next_trigger_time = min(t for t in trigger_times if t > now)
        print(f"Next trigger time: {next_trigger_time}")

        # Calculate the delay
        time_remaining = next_trigger_time - now

        # Calculate hours, minutes, and seconds from time_remaining
        total_seconds = int(time_remaining.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the time remaining as "HH:MM:SS"
        time_remaining_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        return time_remaining_str
        
    @custom_command(name='emojishelp', help="Show the emoji guessing game help message.")
    async def show_emoji_help(self, ctx):
        embed = discord.Embed(title="😀 Emoji Guessing Game Help 😀", color=0x00FF00)
          # Only if you have an image ready
        embed.add_field(name="How to Play", value=(
            "1. Start a new game by typing **`+emojis`** without any arguments.\n"
            "2. You'll get a random emoji question. Respond with **`+emojis 'your guess with normal human language' `** it's AI ^^ to submit your answer.\n"
            "3. You **get 1 usage every 4 hours**. You can stack up to **4 usages**.\n"
            "4. Use the **`+emojisusage`** to check your game status and remaining guesses.\n"
            "5. Correct answers will earn you **5 exp**.\n"
            "5. Can you guess all the emojis correctly? Also works with **slashes commands**."
        ), inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        


async def setup(bot):
    await bot.add_cog(GuessEmoji(bot))
