import os
from dotenv import load_dotenv

load_dotenv()

BACKBOARD_API_KEY = os.getenv("BACKBOARD_API_KEY")
DEFAULT_BACKBOARD_ASSISTANT_ID = os.getenv("DEFAULT_BACKBOARD_ASSISTANT_ID")