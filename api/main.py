from fastapi import FastAPI 
from recommendation import * 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/recommend")
def read_item(message: str):
    rec = get_recommendation(message=message)
    return rec