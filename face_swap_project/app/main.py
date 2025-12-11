import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.api.apis import router as api_router

load_dotenv()

app = FastAPI(
    title="Face Swap API",
    version="1.0.0",
    description="AI-powered face swap service",
)

# Static files
os.makedirs("app/static/results", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# API routes
app.include_router(api_router)
