import os

from dotenv import load_dotenv

load_dotenv()

# ENV VARIABLES
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX_KEY = os.getenv('GOOGLE_CX_ID')
DISCORD_DB_USER = os.getenv('DISCORD_DB_USER')
DISCORD_DB_PASSWORD = os.getenv('DISCORD_DB_PASSWORD')
DISCORD_DB_HOST = os.getenv('DISCORD_DB_HOST')
DISCORD_DB_NAME = os.getenv('DISCORD_DB_NAME')
