import os
from dotenv import load_dotenv

load_dotenv()

# Get the api key from .env
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Set up the default model
DEFAULT_MODEL = "claude-sonnet-5-5"