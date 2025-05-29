import os 
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

load_dotenv(BASE_DIR / '.env')
GROQ_KEY = os.environ.get("GROQ_KEY")   
# MODEL = "llama-3.1-8b-instant"
MODEL = "llama-3.3-70b-versatile"

data_path = BASE_DIR.parent / "data"

TEST_MESSAGE = "I'm a storyboard animator, and I want a decent PC rig that does things fast! It needs at least 1 TB of storage as well as 16 GB of RAM. Try to keep the costs as low as possible, but without sacrificing performance."
