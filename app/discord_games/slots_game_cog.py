import random
from discord.ext import commands
from app.services.gambling_service import GamblingService, level_up_message, level_down_message
from app.services.database_service import DatabaseService
from app.utils.embeds import create_slot_machine_embed
from app.utils.logger import logger
import discord

class SlotsGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()
        self.gambling_service = GamblingService()

    @commands.command(name='slots')
    async def slot_machine(self, ctx, number: str):
        try:
            if number.lower() in {"allin", "max"}:
                amount = self.database.get_total_exp(ctx.message.author.id)
                if amount == 0:
                    await ctx.send("You don't have any exp to bet! Better go start grinding ;]")
                    #await ctx.send("Playing for 0, probably testing the game? (¬_¬)")
                    return
            else:
                amount = int(number)
        except ValueError:
            await ctx.send("You need to specify an amount of exp you want to gamble!\nex. +slots 30 or +slots allin / +slots max")
            return

        if amount <= 0:
            await ctx.send("Wrong number or you want to spin for free! NOTHINGS FREE HERE! ((╬◣﹏◢))")
            return

        total_exp = self.database.get_total_exp(ctx.message.author.id)

        if total_exp < amount:
            await ctx.send("You don't have enough exp! Better go start grinding ;]")
            return

        try:
            # Deduct the points first
            level_up, level_down = self.database.add_exp(ctx.message.author.id, -amount)
            #print(f"Level up after first check: {level_up}")
            #print(f"Level down after first check: {level_down}")

            # Fetch and filter emotes
            emotes = [str(e) for e in ctx.guild.emojis if not e.animated]
            emotes = emotes[:max(len(emotes) - 10, 1)]
            
            # Example values after filtering and slicing
            # emotes = ['😀', '😂', '🥺', '😍']

            if len(emotes) < 9:
                await ctx.send("Not enough emotes available to play the slot machine. Using numbers instead.")
                emotes = [str(i) for i in range(1, 10)]
            else:
                emote_count = 4 # Number of emotes to use
                emotes = emotes[:emote_count]
            
            # Shuffle and create reels
            random.shuffle(emotes)
            reels = random.choices(emotes, k=9)
            print(f"Reels: {reels}")
            
            # Example reels after shuffling and selection
            # reels = ['😂', '😀', '🥺', '😂', '😀', '😍', '🥺', '😂', '😍']

            # Display the reels
            display = f"{reels[0]} | {reels[1]} | {reels[2]}\n{reels[3]} | {reels[4]} | {reels[5]}\n{reels[6]} | {reels[7]} | {reels[8]}"
            

                                                # BOARD: 0 | 1 | 2
                                                #        3 | 4 | 5
                                                #        6 | 7 | 8

            #              A          \/       3---jack        3/       3\         2---       2/        2\        2/3---   2/3---
            #winners = {[6, 1, 8], [0, 7, 2], [3, 4, 5], [6, 4, 2], [0, 4, 8], [3, 4, 5], [6, 4, 2], [0, 4, 8], [0, 1, 2], [6,7,8]
            #     

            def check_win(reels):
                # Initialize counters and messages
                full_win_count = 0
                partial_win_count = 0
                multiplier = 0
                messages = []

                # Check all possible winning combinations
                if reels[6] == reels[1] == reels[8]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit 🔼 [6, 1, 8] (2x)\n")
                if reels[0] == reels[7] == reels[2]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit 🔽 [0, 7, 2] (2x)\n")
                if reels[3] == reels[4] == reels[5]:
                    full_win_count += 1
                    multiplier += 4
                    # here will be function to take from jar
                    messages.append("🎉 Jackpot 🎉 Hit ⬅️➡️ [3, 4, 5] (4x) YOU WINNING ALL IN JAR 'here something for jar function'\n")
                if reels[6] == reels[4] == reels[2]:
                    full_win_count += 1
                    multiplier += 3
                    messages.append("Hit ↗️ [6, 4, 2] (3x)\n")
                if reels[0] == reels[4] == reels[8]:
                    full_win_count += 1
                    multiplier += 3
                    messages.append("Hit ↘️ [0, 4, 8] (3x)\n")
                if reels[0] == reels[1] == reels[2]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit ➡️ [0, 1, 2] (2x)\n")
                if reels[6] == reels[7] == reels[8]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit ➡️ [6, 7, 8] (2x)\n"
                    )
                # Check all possible partial winning combinations
                # Only check if the combination is not part of a full win
                if reels[3] == reels[4] and not (reels[3] == reels[4] == reels[5]):
                    partial_win_count += 1
                    multiplier += 2
                    messages.append("🎊 Mini jackpot 🎊, almost had it! [3, 4] (2x)\n")
                if reels[4] == reels[5] and not (reels[3] == reels[4] == reels[5]):
                    partial_win_count += 1
                    multiplier += 2
                    messages.append("🎊 Mini jackpot 🎊, almost had it! [3, 4] (2x)\n")
                if reels[6] == reels[4] and not (reels[6] == reels[4] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↗️ [6, 4] (1.5x)\n")
                if reels[4] == reels[2] and not (reels[6] == reels[4] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↙️ [4, 2] (1.5x)\n")
                if reels[0] == reels[4] and not (reels[0] == reels[4] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↘️ [0, 4] (1.5x)\n")
                if reels[4] == reels[8] and not (reels[0] == reels[4] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↖️ [4, 8] (1.5x)\n")
                if reels[0] == reels[1] and not (reels[0] == reels[1] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ➡️ [0, 1] (1.5x)\n")
                if reels[1] == reels[2] and not (reels[0] == reels[1] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ⬅️ [1, 2] (1.5x)\n")
                if reels[6] == reels[7] and not (reels[6] == reels[7] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ➡️ [6, 7] (1.5x)\n")
                if reels[7] == reels[8] and not (reels[6] == reels[7] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ⬅️ [7, 8] (1.5x)\n")

                return full_win_count, partial_win_count, multiplier, messages

            all_in_message = None
            full_win_count, partial_win_count, multiplier, messages = check_win(reels)
            # check if user used all in, if so , multiplyer is 3x and all in message is added
            if number.lower() in {"allin", "max"}:
                multiplier *= 3
                all_in_message = "All in! Multiplier multiplyed by 3x!"

            print(f"Full wins: {full_win_count}")
            print(f"Partial wins: {partial_win_count}")
            print(f"Total multiplier: {multiplier}x")

            final_message = "You won!\n"
   
            # Determine the reward
            amount_won = amount * multiplier
            exp_message = f"{str(amount_won)} exp" if amount_won > 0 else "0 exp"
            
            #additional_message = all_in_message if all_in_message else loser_message

            if all_in_message and multiplier > 0:
                additional_message = all_in_message + "\n" + final_message
            elif multiplier > 0:
                additional_message = final_message
            else:
                additional_message = "You lost! Better luck next time!"

            ## AFTER CHECKING WNINGS SEND IT TO EMBED AND CHANGE EXP ETC

            # left exp of user after adding or subtracting exp
            exp_left = total_exp - amount + amount_won
            
            # Set color of embed
            color = discord.Color.green() if amount_won > 0 else discord.Color.red()
            # Create and send the embed
            embed = await create_slot_machine_embed(ctx, display, messages, exp_message, color, additional_message, multiplier, exp_left)
            await ctx.send(embed=embed)
            
            
            # Add the points back if the user wins
            if amount_won > 0:
                level_up_after_win, _ = self.database.add_exp(ctx.message.author.id, amount_won)
                print(f"Level up after second check: {level_up_after_win}")
                if level_up_after_win:
                    await ctx.send(await level_up_message(ctx))
            else:
                # Check for level down if the user loses
                if level_down:
                    await ctx.send(await level_down_message(ctx))

            # Check for initial level change after adjusting points
            if level_up:
                print("Level up detected initially!")  # Debugging
                await ctx.send(await level_up_message(ctx))

            # final log
            logger.info(f"User {ctx.message.author} played slots for {amount} and won/lost {amount_won} exp. He has {exp_left} exp left.")
                
        except Exception as e:
            # In case of error, return the deducted points
            self.database.add_exp(ctx.message.author.id, amount)
            await ctx.send(f"An error occurred: {str(e)}. Your points have been returned.")




async def setup(bot):
    await bot.add_cog(SlotsGame(bot))
