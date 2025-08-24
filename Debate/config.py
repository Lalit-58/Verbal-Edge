# config.py

from dotenv import load_dotenv
import os

load_dotenv()

def get_gemini_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key is None:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    return key
