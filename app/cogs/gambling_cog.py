import discord
from discord.ext import commands
import random
import asyncio
from app.services.database_service import DatabaseService
from app.services.gambling_service import GamblingService
from app.utils.embeds import create_slot_machine_embed

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = DatabaseService()
        self.gambling_service = GamblingService()
        self.time = 0

    # @commands.command(name='russian')
    # async def russian(self, ctx, number: str):
    #     try:
    #         if not self.gambling_service.joinable:
    #             await ctx.send("Game has already been started!")
    #             return

    #         try:
    #             amount = int(number)
    #         except ValueError:
    #             await ctx.send("You need to specify an amount of exp you want to bet!\nex. +russian 30")
    #             return

    #         total_exp = 0
    #         message = await ctx.send("React to participate ↑_(ΦwΦ)Ψ")
    #         await message.add_reaction('💀')

    #         users = []

    #         def check(reaction, user):
    #             return str(reaction.emoji) == '💀' and reaction.message.id == message.id

    #         timer = 15
    #         while timer > 0:
    #             try:
    #                 reaction, user = await self.bot.wait_for('reaction_add', timeout=1, check=check)
    #                 if user not in users and not user.bot:
    #                     users.append(user)
    #             except asyncio.TimeoutError:
    #                 pass
    #             timer -= 1

    #         if len(users) < 2:
    #             await ctx.send("EVERYONE scared to join huh? Minimum 2 cattos required for the game to start!")
    #             return

    #         for user in users:
    #             if self.database.get_exp(user.id) < amount:
    #                 await ctx.send(f"{user.mention} is broke as heck and cannot join\nGo get some exp and don't waste OUR time")
    #                 users.remove(user)
    #             else:
    #                 self.database.add_exp(user.id, -amount)
    #                 total_exp += amount

    #         if len(users) >= 2:
    #             await ctx.send("THE GAME IS ABOUT TO BEGIN!")
    #             await self.gambling_service.russian_game(users, ctx, total_exp)
    #         else:
    #             await ctx.send("EVERYONE scared to join huh? Minimum 2 cattos required for the game to start!")

    #     except Exception as e:
    #         print(e)

    @commands.command(name='slots')
    async def slot_machine(self, ctx, number: str):
        try:
            if number.lower() == "allin" or number.lower() == "max":
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

            emotes = [str(e) for e in ctx.guild.emojis if not e.animated]
            emotes = emotes[:max(len(emotes) - 40, 1)]

            use_fallback = False
            if len(emotes) < 9:
                use_fallback = True
                await ctx.send("Not enough emotes available to play the slot machine. Using numbers instead.")
                emotes = [str(i) for i in range(1, 10)]

            random.shuffle(emotes)
            reels = random.sample(emotes, 9)

            display = f"    {reels[0]} | {reels[1]} | {reels[2]}\n {reels[3]} | {reels[4]} | {reels[5]}  \n    {reels[6]} | {reels[7]} | {reels[8]}"
            selected_reels = reels[3:6]

            result_message = "(⌯˃̶᷄ ﹏ ˂̶᷄⌯) No match! Maybe better spins next time?"
            all_in_message = None

            if len(set(selected_reels)) == 1:
                amount_won = amount * 10
                result_message = f"(✯◡✯) **!JACKPOT!** (✯◡✯)\nYou won {amount_won} Exp!"
                if number.lower() in ["allin", "max"]:
                    all_in_message = f"(✯◡✯) **ALL IN JACKPOT!** (✯◡✯)\nYou risked it all and won {amount_won} Exp!"
            elif len(set(selected_reels)) == 2:
                amount_won = amount * 4
                result_message = f"(￢‿￢ ) **!Two of a Kind!** (￢‿￢ ) \nYou won {amount_won} Exp!"
                if number.lower() in ["allin", "max"]:
                    all_in_message = f"(￢‿￢ ) **ALL IN Two of a Kind!** (￢‿￢ ) \nYou risked it all and won {amount_won} Exp!"
            else:
                if number.lower() in ["allin", "max"]:
                    all_in_message = f"(⌯˃̶᷄ ﹏ ˂̶᷄⌯) **ALL IN No Match!** (⌯˃̶᷄ ﹏ ˂̶᷄⌯)\nYou risked it all and lost everything!"

            # Create and send the embed
            embed = await create_slot_machine_embed(ctx, display, result_message, all_in_message)
            await ctx.send(embed=embed)

            # Add the points back if the user wins
            if len(set(selected_reels)) <= 2:
                self.database.add_exp(ctx.message.author.id, amount_won)

            # Check for level change after adjusting points
            new_level_up, new_level_down = self.database.add_exp(ctx.message.author.id, 0)
            if new_level_up:
                await ctx.send(f"Congratulations even more {ctx.message.author.mention}!\nYour gambling addiction caused you to level up! (* ^ ω ^)")
            elif new_level_down:
                await ctx.send(f"Oh no, {ctx.message.author.mention}!\nYour losses caused you to lose a level... (；￣Д￣)")
        except Exception as e:
            # In case of error, return the deducted points
            self.database.add_exp(ctx.message.author.id, amount)
            await ctx.send(f"An error occurred: {str(e)}. Your points have been returned.")








async def setup(bot):
    await bot.add_cog(Gambling(bot))

