import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv("../.env")
GROQ_KEY = os.getenv("GROQ_KEY")
MODEL = "llama-3.1-8b-instant"

data_path = "../data"