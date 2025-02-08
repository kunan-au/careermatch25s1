import os
import uuid
from http.client import HTTPException

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile
from sqlalchemy import insert, select

from src.database import execute, fetch_one, user_profile
from src.users.schemas import UserUpdate

SUPPORTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]


async def create_user(email: str):
    insert_query = insert(user_profile).values(
        email=email,
        name="",
        avatar="",
        resume="",
    )
    await execute(insert_query)

async def get_user_profile(email):
    query = select(user_profile).where(user_profile.c.email == email)
    # 如果没有找到用户，直接插入一个新用户，name, avatar, resume都为空字符串
    user = await fetch_one(query)
    if not user:
        await create_user(email)
        user = await fetch_one(query)
    return user

async def update_user_profile(email, user):
    values = {key: value for key, value in vars(user).items() if value is not None}
    query = user_profile.update().where(user_profile.c.email == email).values(**values)
    await execute(query)
    return await get_user_profile(email)

async def upload_user_avatar(email: str, avatar: UploadFile):
    user_dict = await get_user_profile(email)
    if not user_dict:
        raise HTTPException(status_code=404, detail="User not found")

    if avatar.content_type not in SUPPORTED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    filename = await save_avatar_file(avatar)

    user_dict['avatar'] = filename

    user = UserUpdate(**user_dict)
    await update_user_profile(email, user)

    return filename

async def save_avatar_file(avatar: UploadFile):
    s3_client = boto3.client('s3')

    short_uuid = str(uuid.uuid4())[:8]
    _, ext = os.path.splitext(avatar.filename)
    new_filename = f"{short_uuid}{ext}"

    try:
        s3_client.upload_fileobj(avatar.file, # 'careermatch-avatar'
                                 'careermatch-avatar-2024', new_filename)
    except (BotoCoreError, ClientError) as error:
        print(error)
        return None

    return new_filename

async def upload_user_resume(email: str, resume: UploadFile):
    user_dict = await get_user_profile(email)
    if not user_dict:
        raise HTTPException(status_code=404, detail="User not found")

    if resume.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type")

    filename = await save_resume_file(resume)

    if not filename:
        raise HTTPException(status_code=500, detail="Failed to save resume file")

    user_dict['resume'] = filename

    user = UserUpdate(**user_dict)
    await update_user_profile(email, user)

    return filename

async def save_resume_file(resume: UploadFile):
    s3_client = boto3.client('s3')

    short_uuid = str(uuid.uuid4())[:8]
    _, ext = os.path.splitext(resume.filename)
    new_filename = f"{short_uuid}{ext}"

    try:
        s3_client.upload_fileobj(
            resume.file,
            # 'careermatch-resume'
            'careermatch-resume-2024',
            new_filename,
            ExtraArgs={
                'ContentType': 'application/pdf',
                'ContentDisposition': 'inline',
            }
        )
    except (BotoCoreError, ClientError) as error:
        print(error)
        return None

    return new_filename

