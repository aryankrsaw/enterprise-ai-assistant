import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_CLOUD_MODEL_API_KEY")

OLLAMA_HOST = "https://ollama.com"

OLLAMA_MODEL = "gemma4:31b"