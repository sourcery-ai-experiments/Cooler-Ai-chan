import random
import discord 



def calculate_exp_bonus():
    return 1000 if random.random() < 0.001 else 0

async def extract_user(ctx, specified_user):
    if len(ctx.message.mentions) > 0:
        return ctx.message.mentions[0]
    else:
        return discord.utils.find(lambda m: m.name == specified_user, ctx.guild.members)

async def user_not_found(ctx, user):
    if user is None:
        await ctx.send("User not found.")
        return True
    return False