from fastapi import FastAPI
from routers import ads, users
import uvicorn

app = FastAPI()

app.include_router(ads.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("app:app", port=8080, reload=True)
