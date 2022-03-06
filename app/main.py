import uvicorn
from fastapi import FastAPI

from app.routers import items, users

app = FastAPI()


app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
