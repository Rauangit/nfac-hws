from fastapi import FastAPI
from math import factorial

app = FastAPI()

@app.get("/{num}")
async def compute_factorial(num: int):
    return {"nfactorial": factorial(num)}
