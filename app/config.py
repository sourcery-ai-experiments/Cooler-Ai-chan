import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID'))
    ai_groq_key = os.getenv('AI_GROQ_KEY')
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'app/persistent_data/logs/discord_bot.log')
    LOKI_URL = os.getenv('LOKI_URL', 'http://localhost:3100')
    PREFIX = os.getenv('PREFIX', '+')
    ENVIROMENT = os.getenv('ENVIROMENT', 'production')