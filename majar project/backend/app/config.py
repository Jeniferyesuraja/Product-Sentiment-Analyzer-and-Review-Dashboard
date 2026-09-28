"""Application configuration loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration shared by local and deployed environments."""

    CORS_ORIGINS = list(dict.fromkeys([
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        *[origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()],
    ]))
    MONGODB_URI = os.getenv("MONGO_URI", os.getenv("MONGODB_URI", ""))
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "product_sentiment")
