from fastapi import APIRouter, File, UploadFile

from src.users import service
from src.users.schemas import UserRead, UserUpdate

router = APIRouter()

@router.put("/{email}", response_model=UserRead)
async def update_user_profile(email, user: UserUpdate):
  user = await service.update_user_profile(email, user)
  return user

@router.get("/{email}", response_model=UserRead)
async def get_user(email : str):
  user = await service.get_user_profile(email)
  return user

@router.post("/{email}/avatar")
async def upload_avatar(email: str, avatar: UploadFile = File(...)):
    await service.upload_user_avatar(email, avatar)
    return {"message": f"Avatar for {email} uploaded successfully"}

@router.post("/{email}/resume")
async def upload_resume(email: str, resume: UploadFile = File(...)):
    await service.upload_user_resume(email, resume)
    return {"message": f"Resume for {email} uploaded successfully"}
