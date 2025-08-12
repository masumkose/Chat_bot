from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()