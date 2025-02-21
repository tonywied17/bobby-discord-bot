from dotenv import load_dotenv
load_dotenv()
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CONVERSATION_CHANCE = 0.05
LAUGH_REACT_CHANCE = 0.22
MAX_RESPONSE_RANGE = (3, 8)