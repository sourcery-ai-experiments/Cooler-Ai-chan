import random
from discord.ext import commands
from app.services.gambling_service import GamblingService, level_up_message, level_down_message
from app.services.database_service import DatabaseService
from app.utils.embeds import create_slot_machine_embed

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
            print(f"Level up after first check: {level_up}")
            print(f"Level down after first check: {level_down}")
            emotes = [str(e) for e in ctx.guild.emojis if not e.animated]
            emotes = emotes[:max(len(emotes) - 40, 1)]

            use_fallback = False
            if len(emotes) < 9:
                use_fallback = True
                await ctx.send("Not enough emotes available to play the slot machine. Using numbers instead.")
                emotes = [str(i) for i in range(1, 10)]

            # Create reels with possible duplicates
            random.shuffle(emotes)
            reels = random.choices(emotes, k=9)

            display = f"    {reels[0]} | {reels[1]} | {reels[2]}\n {reels[3]} | {reels[4]} | {reels[5]}  \n    {reels[6]} | {reels[7]} | {reels[8]}"
            selected_reels = reels[3:6]

            result_message = "(⌯˃̶᷄ ﹏ ˂̶᷄⌯) No match! Maybe better spins next time?"
            all_in_message = None
            amount_won = 0
            # Determine the reward
            if len(set(selected_reels)) == 1:
                amount_won = amount * 3
                result_message = f"(✯◡✯) **!JACKPOT!** (✯◡✯)\nYou won {amount_won} Exp!"
                if number.lower() in {"allin", "max"}:
                    amount_won = amount * 10
                    all_in_message = f"(✯◡✯) **ALL IN JACKPOT!** (✯◡✯)\nYou risked it all and won {amount_won} Exp!"
            elif len(set(selected_reels)) == 2:
                amount_won = amount * 2
                result_message = f"(￢‿￢ ) **!Two of a Kind!** (￢‿￢ ) \nYou won {amount_won} Exp!"
                if number.lower() in {"allin", "max"}:
                    amount_won = amount * 5
                    all_in_message = f"(￢‿￢ ) **ALL IN Two of a Kind!** (￢‿￢ ) \nYou risked it all and won {amount_won} Exp!"
            else:
                if number.lower() in {"allin", "max"}:
                    all_in_message = f"(⌯˃̶᷄ ﹏ ˂̶᷄⌯) **ALL IN No Match!** (⌯˃̶᷄﹏ ˂̶᷄⌯)\nYou risked it all and lost everything!"

            import discord
            # set color of embed
            color = discord.Color.green() if amount_won > 0 else discord.Color.red()
            # Create and send the embed
            embed = await create_slot_machine_embed(ctx, display, result_message, color, all_in_message)
            await ctx.send(embed=embed)

            # Add the points back if the user wins
            if len(set(selected_reels)) <= 2:
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
                
        except Exception as e:
            # In case of error, return the deducted points
            self.database.add_exp(ctx.message.author.id, amount)
            await ctx.send(f"An error occurred: {str(e)}. Your points have been returned.")




async def setup(bot):
    await bot.add_cog(SlotsGame(bot))
