"""Configuration management for the project."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_openai_key():
    """Get the OpenAI API key from environment variables."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY not found. Please set it in your .env file."
        )
    return OPENAI_API_KEY
