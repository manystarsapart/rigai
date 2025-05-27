from fastapi import FastAPI 
from .recommendation import * 
from .extraction import get_requirements

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/parrot")
def parrot(message: str):
    return {"message": message}

@app.get("/extract")
def extract(message: str):
    print(message)
    reqs = get_requirements(message)
    return reqs

@app.get("/recommend")
def recommend(message: str):
    rec = get_recommendation(message=message)
    return rec