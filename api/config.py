import os 
# from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

# load_dotenv("../.env")
GROQ_KEY = os.environ.get("GROQ_KEY")
MODEL = "llama-3.1-8b-instant"

# data_path = "../data"

BASE_DIR = Path(__file__).parent.resolve()
data_path = BASE_DIR / "data"