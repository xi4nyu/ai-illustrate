from fastapi import FastAPI
from database import init_db
from api import users, files, chat

app = FastAPI(
    title="AI Illustrate API",
    description="API for managing users, files, and chat interactions.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    # This will create the database tables if they don't exist
    init_db()

# Include the API routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the AI Illustrate API"}

# To run this application:
# 1. Install all dependencies: pip install -r requirements.txt
# 2. Make sure you have Redis running for Celery.
# 3. Start the Celery worker in a separate terminal:
#    celery -A tasks worker --loglevel=info
# 4. Start the FastAPI server:
#    uvicorn main:app --reload
