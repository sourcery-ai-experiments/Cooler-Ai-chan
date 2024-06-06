# Cooler-Ai-chan
Python version of Ai-chan, pranky ai made by Nequss (https://github.com/Nequss)

## WRITING IT IN HURY TO JUST HAVE SOMETHING, IT WILL BE CHANGED LATER
to install and run:

clone this, add config.py with this in it
```
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = "your bot otken here"
    OWNER_ID = int(os.getenv('OWNER_ID', '123131441423454353')) # this is i dont kw know if needed 
    GUILD_ID = int(os.getenv('GUILD_ID', '124124234234234234')) # this is i dont kw know if needed 
    #ai_groq_key = os.getenv('AI_GROQ_KEY')
    LOG_FILE_PATH = "app/logs/discord_bot.log"
    LOKI_URL="http://localhost:3100" # url this is something for now needed but not working xd need to coment in logger this part


``` 

in the root directory of the project, and run the following commands:
```
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
python -m app.main
```