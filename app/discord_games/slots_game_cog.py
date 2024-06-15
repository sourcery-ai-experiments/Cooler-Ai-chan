import random
from discord.ext import commands
from app.services.gambling_service import GamblingService, level_up_message, level_down_message
from app.services.database_service import DatabaseService
from app.utils.embeds import create_slot_machine_embed
from app.utils.logger import logger
from app.utils.gamba_jar import CasinoJar
from app.config import Config
import discord

class SlotsGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()
        self.gambling_service = GamblingService()
        self.casino_jar = CasinoJar()
        self.config = Config()
        self.ENVIROMENT = self.config.ENVIROMENT

    @commands.command(name='slots')
    async def slot_machine(self, ctx, number: str):
        try:
            if number.lower() in {"allin", "max"}:
                amount = self.database.get_total_exp(ctx.message.author.id)
                if amount == 0:
                    await ctx.send("You don't have any exp to bet! Better go start grinding ;]")
                    # for testing purposes it will be fake 1 exp
                    #amount = 1
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
        
        #for testing purposes
        if self.ENVIROMENT == "development" and amount == 0:
            amount = 1
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

            elif self.ENVIROMENT == "development": # For testing purposes
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
                jackpot_win = False
                # Check all possible winning combinations
                if reels[6] == reels[1] == reels[8]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit 🔼 [6, 1, 8] (4x)\n")
                if reels[0] == reels[7] == reels[2]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit 🔽 [0, 7, 2] (4x)\n")
                if reels[3] == reels[4] == reels[5]:
                    full_win_count += 1
                    multiplier += 4
                    jackpot_win = True
                    print("Jackpot win detected! seting variable ")  # Debugging
                    messages.append("🎉 Jackpot 🎉 Hit ⬅️➡️ [3, 4, 5] (8x)\n")
                if reels[6] == reels[4] == reels[2]:
                    full_win_count += 1
                    multiplier += 3
                    messages.append("Hit ↗️ [6, 4, 2] (6x)\n")
                if reels[0] == reels[4] == reels[8]:
                    full_win_count += 1
                    multiplier += 3
                    messages.append("Hit ↘️ [0, 4, 8] (6x)\n")
                if reels[0] == reels[1] == reels[2]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit ➡️ [0, 1, 2] (4x)\n")
                if reels[6] == reels[7] == reels[8]:
                    full_win_count += 1
                    multiplier += 2
                    messages.append("Hit ➡️ [6, 7, 8] (4x)\n"
                    )
                # Check all possible partial winning combinations
                # Only check if the combination is not part of a full win
                if reels[3] == reels[4] and not (reels[3] == reels[4] == reels[5]):
                    partial_win_count += 1
                    multiplier += 2
                    messages.append("🎊 Mini jackpot 🎊, almost had it! [3, 4] (4x)\n")
                if reels[4] == reels[5] and not (reels[3] == reels[4] == reels[5]):
                    partial_win_count += 1
                    multiplier += 2
                    messages.append("🎊 Mini jackpot 🎊, almost had it! [3, 4] (4x)\n")
                if reels[6] == reels[4] and not (reels[6] == reels[4] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↗️ [6, 4] (3x)\n")
                if reels[4] == reels[2] and not (reels[6] == reels[4] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↙️ [4, 2] (3x)\n")
                if reels[0] == reels[4] and not (reels[0] == reels[4] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↘️ [0, 4] (3x)\n")
                if reels[4] == reels[8] and not (reels[0] == reels[4] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ↖️ [4, 8] (3x)\n")
                if reels[0] == reels[1] and not (reels[0] == reels[1] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ➡️ [0, 1] (3x)\n")
                if reels[1] == reels[2] and not (reels[0] == reels[1] == reels[2]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ⬅️ [1, 2] (3x)\n")
                if reels[6] == reels[7] and not (reels[6] == reels[7] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ➡️ [6, 7] (3x)\n")
                if reels[7] == reels[8] and not (reels[6] == reels[7] == reels[8]):
                    partial_win_count += 1
                    multiplier += 1.5
                    messages.append("Hit 2 in ⬅️ [7, 8] (3x)\n")

                return full_win_count, partial_win_count, multiplier, messages, jackpot_win

            all_in_message = None
            full_win_count, partial_win_count, multiplier, messages, jackpot_win = check_win(reels)
            # check if user used all in, if so , multiplyer is 3x and all in message is added
            if number.lower() in {"allin", "max"}:
                multiplier *= 3
                all_in_message = "All in! Multiplier multiplyed by 3x!"

            # RIUSING MULTIPLAYER GLOBALY BY 2 COUSE ITS TO HARD
            multiplier += multiplier

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
            
            #sending to jar if user lost
            if amount_won == 0:
                self.casino_jar.add_to_jar(ctx.message.author.id, amount)
                jar_messgage = f"User {ctx.message.author} lost {amount} exp. It was added to the jar.\n Jar now has {self.casino_jar.get_jar_total()} exp."
            else:
                self.casino_jar.add_winning_combination(ctx.message.author.id, full_win_count, partial_win_count, amount_won)
                logger.info(f"Adding winning combination for user {ctx.message.author} with full wins: {full_win_count} and partial wins: {partial_win_count}")
            
            # Get the points from the jar if the user wins and the win was jackpot
            if jackpot_win:
                print("Jackpot win detected!")  # Debugging
                # Get the points from the jar and add them to the overal win
                jar_winning = self.casino_jar.get_from_jar(ctx.message.author.id)
                amount_won += jar_winning
                jar_messgage = f"🎉 JACKPOOOOOT 🎉.\n 🎉 {jar_winning} exp taken from jar!. 🎉\n🎉 Now jar has {self.casino_jar.get_jar_total()} exp. 🎉"
            elif amount_won > 0:
                jar_messgage = f"No jackpot = no jar winnings. Jar stays the same:  {self.casino_jar.get_jar_total()} exp."
            # Set color of embed
            color = discord.Color.green() if amount_won > 0 else discord.Color.red()
            # Create and send the embed
            embed = await create_slot_machine_embed(ctx, display, messages, exp_message, color, additional_message, multiplier, exp_left, jar_messgage)
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
            await ctx.send(f"An error occurred: {str(e)}.\n Your points have been returned. Ask Shiro AI whats wrong! (¬_¬)")

    # Command to show the jar amount
    @commands.command(name='slotsjar')
    async def show_jar(self, ctx):
        jar_amount = self.casino_jar.get_jar_total()
        await ctx.send(f"Jar has {jar_amount} exp.")

    @commands.command(name='slotsrank')
    async def show_ranking_embed(self, ctx):
        top_winners = self.casino_jar.get_top_winners_with_counts()
        top_losers = self.casino_jar.get_top_losers()
        winning_combinations = self.casino_jar.get_winning_combination_counts()
        embed = discord.Embed(title="🎰 Slots Ranking 🎰", color=0xFFD700)

        # Add a section for the winning combinations count
        embed.add_field(name="🎉 Winning Combinations 🎉", value="", inline=False)
        if winning_combinations:
            for user in winning_combinations:
                embed.add_field(name="User", value=f"{ctx.guild.get_member(user[0])}", inline=True)
                embed.add_field(name="Full Wins", value=f"{user[1]}", inline=True)
                embed.add_field(name="Partial Wins", value=f"{user[2]}", inline=True)
        else:
            embed.add_field(name="\u200b", value="No winning combinations yet", inline=False)

        # Add a section for the top jar winners
        embed.add_field(name="🏆 Top Jar Winners 🏆", value="", inline=False)
        if top_winners:
            for winner in top_winners:
                embed.add_field(name="User", value=f"{ctx.guild.get_member(winner[0])}", inline=True)
                embed.add_field(name="Jar Wins", value=f"{winner[2]}", inline=True)
                embed.add_field(name="Exp", value=f"{winner[1]}", inline=True)
        else:
            embed.add_field(name="\u200b", value="No winners yet", inline=False)

        # Add a section for the top losers
        embed.add_field(name="😭 Top Losers 😭", value="", inline=False)
        if top_losers:
            for loser in top_losers:
                embed.add_field(name="User", value=f"{ctx.guild.get_member(loser[0])}", inline=True)
                embed.add_field(name="Losses", value=f"{loser[2]}", inline=True)
                embed.add_field(name="Exp", value=f"{loser[1]}", inline=True)
        else:
            embed.add_field(name="\u200b", value="No losers yet", inline=False)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

    @commands.command(name='slotsrankingembed')
    async def show_ranking_embed(self, ctx):
        top_winners = self.casino_jar.get_top_winners_with_counts()
        top_losers = self.casino_jar.get_top_losers()
        winning_combinations = self.casino_jar.get_winning_combination_counts()
        embed = discord.Embed(title="🎰 Slots Ranking 🎰", color=0xFFD700)

        # Add a section for the winning combinations count
        winning_combination_str = ""
        if winning_combinations:
            for user in winning_combinations:
                user_name = ctx.guild.get_member(user[0])
                full_wins = user[1]
                partial_wins = user[2]
                total_exp_won = user[3]
                winning_combination_str += f"**{user_name}** | Full wins: **{full_wins}** | Partial wins: **{partial_wins}** | Total exp: **{total_exp_won} Exp**\n"
        else:
            winning_combination_str = "No winning combinations yet"
        
        embed.add_field(name="🎉 Winning Combinations 🎉", value=winning_combination_str, inline=False)

        # Add a section for the top jar winners
        embed.add_field(name="🏆 Top Jar Winners 🏆", value="", inline=False)
        if top_winners:
            for winner in top_winners:
                embed.add_field(name="User", value=f"{ctx.guild.get_member(winner[0])}", inline=True)
                embed.add_field(name="Jar Wins", value=f"{winner[2]}", inline=True)
                embed.add_field(name="Exp", value=f"{winner[1]}", inline=True)
        else:
            embed.add_field(name="SAD", value="No winners yet", inline=False)

        # Add a section for the top losers
        top_losers_str = ""
        if top_losers:
            for loser in top_losers:
                user_name = ctx.guild.get_member(loser[0])
                losses = loser[2]
                exp = loser[1]
                top_losers_str += f"**{user_name}** | Losses: **{losses}** | Exp: **{exp} Exp**\n"
        else:
            top_losers_str = "No losers yet"
        
        embed.add_field(name="😭 Top Losers 😭", value=top_losers_str, inline=False)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SlotsGame(bot))
