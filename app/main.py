from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import url
from app.database.session import engine, Base
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple and efficient URL shortener backend.",
    version="1.0.0"
)

# Include routes
app.include_router(url.router, tags=["URL Shortener"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open(os.path.join("static", "index.html"), "r") as f:
        return f.read()

@app.get("/api-status")
def api_status():
    return {"message": "Welcome to the URL Shortener API. Go to /docs for API documentation."}
