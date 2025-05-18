import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv("../.env")
GROQ_KEY = os.getenv("GROQ_KEY")
MODEL = "llama3-70b-8192"

data_path = "../data"