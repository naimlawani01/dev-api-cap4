from fastapi import FastAPI

app = FastAPI() # Variable name for the server

@app.get("/")
async def root():
    return {"message": "Bingo"}