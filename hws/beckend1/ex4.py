from fastapi import FastAPI

app = FastAPI()

@app.post("/meaning-of-life")
async def meaning_of_life():
    return {"meaning": "42"}
