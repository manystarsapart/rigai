from fastapi import FastAPI 
from .recommendation import * 
from .extraction import get_requirements
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/parrot")
def parrot(message: str):
    return {"message": message}

@app.get("/extract")
def extract(message: str):
    reqs = get_requirements(message)
    return reqs

@app.get("/recommend")
def recommend(message: str):
    rec = get_recommendation(message=message)
    return rec