import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")  # OpenAI или другая модель
BLOCKCHAIN_NODE = os.getenv("BLOCKCHAIN_NODE")  # Узел Dogecoin
