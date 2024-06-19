import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID'))
    ai_groq_key = os.getenv('AI_GROQ_KEY')

    @staticmethod
    def get_groq_api_keys():
        api_keys = []
        i = 1
        while True:
            key = os.getenv(f'AI_GROQ_KEY{i}')
            if key is None:
                break
            api_keys.append(key)
            i += 1
        return api_keys
    
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'app/persistent_data/logs/discord_bot.log')
    LOKI_URL = os.getenv('LOKI_URL', 'http://localhost:3100')
    PREFIX = os.getenv('PREFIX', '+')
    ENVIROMENT = os.getenv('ENVIROMENT', 'production')