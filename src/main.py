from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import profile
import os

app = FastAPI(title="User Profile API", description="Manage user profiles and profile pictures.")

# Ensure media directory exists
MEDIA_DIR = os.path.join(os.path.dirname(__file__), "media")
os.makedirs(MEDIA_DIR, exist_ok=True)

app.include_router(profile.router, prefix="/profiles", tags=["Profiles"])

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")
