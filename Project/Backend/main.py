# backend/main.py

from fastapi import FastAPI
from webhook import router as webhook_router

app = FastAPI(title="PR Security Analyzer")

app.include_router(webhook_router)

@app.get("/")
def health_check():
    return {"status": "Backend running"}
