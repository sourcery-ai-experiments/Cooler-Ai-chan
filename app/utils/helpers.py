from better_profanity import profanity
import random

def check_profanity(text):
    return profanity.contains_profanity(text)

def censor_text(text):
    return profanity.censor(text)

def calculate_exp_bonus():
    return 1000 if random.random() < 0.001 else 0
