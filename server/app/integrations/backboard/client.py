from backboard import BackboardClient
from app.core.config import BACKBOARD_API_KEY


def get_backboard_client() -> BackboardClient:
    if not BACKBOARD_API_KEY:
        raise ValueError("BACKBOARD_API_KEY is missing from .env")

    return BackboardClient(api_key=BACKBOARD_API_KEY)