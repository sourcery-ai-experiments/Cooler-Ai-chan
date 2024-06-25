
import requests
import random
from app.config import Config
emoji_key = Config.EMOJI_API_KEY

def fetch_emojis():
    url = f"https://emoji-api.com/emojis?access_key={emoji_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def create_emoji_combinations(emojis, num_combinations=5):
    emoji_combinations = []
    for _ in range(num_combinations):
        # Ensure only valid emoji characters are used
        valid_emojis = [emoji for emoji in emojis if 'character' in emoji and emoji['character'].isprintable()]
        if len(valid_emojis) >= 3:
            emoji_combination = random.sample(valid_emojis, 3)
            question_emojis = ''.join([emoji['character'] for emoji in emoji_combination])
            emoji_combinations.append(question_emojis)
    return emoji_combinations

emojis = fetch_emojis()
emoji_questions = create_emoji_combinations(emojis)

print(emoji_questions)
