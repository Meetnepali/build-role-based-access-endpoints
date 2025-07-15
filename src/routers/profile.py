from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
import aiofiles
import uuid
import imghdr
import os

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "../media")

router = APIRouter()

# In-memory user storage: {username: UserProfileData}
user_profiles: Dict[str, dict] = {}

ALLOWED_MIMETYPES = {"image/png", "image/jpeg"}
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE_BYTES = 1024 * 1024  # 1 MB

class UserProfileCreate(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None

class UserProfile(UserProfileCreate):
    profile_picture_url: Optional[str] = None

@router.post("/", response_model=UserProfile, status_code=status.HTTP_201_CREATED, summary="Create User Profile", description="Create a new user profile.")
async def create_profile(profile: UserProfileCreate):
    if profile.username in user_profiles:
        raise HTTPException(status_code=400, detail={"error": "Username already exists."})
    user_profiles[profile.username] = {
        "username": profile.username,
        "email": profile.email,
        "bio": profile.bio,
        "profile_picture": None
    }
    return UserProfile(**user_profiles[profile.username], profile_picture_url=None)

@router.get("/{username}", response_model=UserProfile, summary="Get User Profile", description="Return all info (including profile picture URL, if set) for a user.")
async def get_profile(username: str):
    user = user_profiles.get(username)
    if not user:
        raise HTTPException(status_code=404, detail={"error": "User not found."})
    picture_url = None
    if user.get("profile_picture"):
        fname = user["profile_picture"]
        picture_url = f"/media/{fname}"
    return UserProfile(**user, profile_picture_url=picture_url)

@router.post("/{username}/profile_picture", summary="Upload or Update Profile Picture",
    description="Upload a PNG or JPEG image (<=1MB) as the user's profile picture.", status_code=200)
async def upload_profile_picture(username: str, file: UploadFile = File(...)):
    user = user_profiles.get(username)
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found."})

    if file.content_type not in ALLOWED_MIMETYPES:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type. Only PNG or JPEG allowed."})

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        return JSONResponse(status_code=400, content={"error": "File too large. Max file size is 1MB."})

    # Validate actual file header (not just mimetype)
    ext = imghdr.what(None, h=contents)
    if ext not in ALLOWED_EXTENSIONS:
        return JSONResponse(status_code=400, content={"error": "File content is not a valid PNG or JPEG image."})
    fname = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(MEDIA_DIR, fname)
    async with aiofiles.open(file_path, "wb") as out_file:
        await out_file.write(contents)
    user["profile_picture"] = fname
    return {"message": "Profile picture uploaded successfully.", "profile_picture_url": f"/media/{fname}"}
