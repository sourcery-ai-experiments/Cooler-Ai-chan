import os
from dotenv import load_dotenv
from app.bot import main
import asyncio

# Load environment variables from a .env file
load_dotenv()



if __name__ == "__main__":
    asyncio.run(main())
