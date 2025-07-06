from contextlib import asynccontextmanager
from fastapi import FastAPI
from middleware import middleware

from api import chat, files, user
from init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Illustrate API",
    description="API for managing users, files, and chat interactions.",
    version="1.0.0",
    lifespan=lifespan,
)

PREFIX = "/api/v1"

# Include the API routers
app.include_router(user.router, prefix=f"{PREFIX}/users", tags=["Users"])
app.include_router(files.router, prefix=f"{PREFIX}/files", tags=["Files"])
app.include_router(chat.router, prefix=f"{PREFIX}/chat", tags=["Chat"])


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the AI Illustrate API"}


for m in middleware:
    app.add_middleware(m)

# To run this application:
# 1. Install all dependencies: pip install -r requirements.txt
# 2. Make sure you have Redis running for Celery.
# 3. Start the Celery worker in a separate terminal:
#    celery -A tasks worker --loglevel=info
# 4. Start the FastAPI server:
#    uvicorn main:app --reload
