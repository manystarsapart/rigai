import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv("../.env")
APIKEY = os.getenv("GROQ_KEY")

client = Groq(api_key=APIKEY)
MODEL = "llama3-70b-8192"

prompt = input("Insert your prompt: ")

chat_completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(chat_completion.choices[0].message.content)