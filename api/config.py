import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv("../.env")
GROQ_KEY = os.getenv("GROQ_KEY")
MODEL = "llama-3.1-8b-instant"

data_path = "../data"
TEST_MESSAGE = "I'm a storyboard animator, and I want a decent PC rig that does things fast! It needs at least 1 TB of storage as well as 16 GB of RAM. Try to keep the costs as low as possible, but without sacrificing performance."