from fastapi import Depends ,APIRouter, File, Form, UploadFile, Header
from app.services import posting
from typing import List
from app import schemas
from typing import Optional
from ..main import redis_cache
from fastapi_cache.backends.redis import RedisCacheBackend
from app.controller import postingController

router = APIRouter()

@router.get('/posting')
async def get_all_post(cache : RedisCacheBackend = Depends(redis_cache),x_token: str = Header(...)):
    data = await postingController.get_all_post(cache, x_token)
    return data

@router.post('/posting')
async def create_new_post(post: schemas.CreatePost, cache : RedisCacheBackend = Depends(redis_cache), x_token: str = Header(...)):
    return await postingController.create_new_post(post, cache, x_token)

@router.post('/comment')
async def create_new_comment(comment: schemas.CreateComment, cache : RedisCacheBackend = Depends(redis_cache), x_token: str = Header(...)):
    return await postingController.create_new_comment(comment, cache, x_token)

@router.get('/laporan')
async def get_user_laporan(cache : RedisCacheBackend = Depends(redis_cache),x_token: str = Header(...)):
    data = await postingController.get_laporan( x_token)
    return data

@router.get('/laporan/date')
def get_laporan_date(date: str):
    return postingController.get_laporan_date(date)

@router.post('/laporan')
def create_new_laporan(laporan: schemas.CreateLaporan, x_token: str = Header(...)):
    return posting.create_laporan(laporan=laporan, token=x_token);


@router.post('/absent')
def create_new_absent(deskripsi: str = Form (...), photo: Optional[UploadFile] = File(None), x_token: str = Header(...)):
    data = postingController.create_new_absent(deskripsi, photo, x_token)
    return data

@router.post('/save_token')
def save_token(data:schemas.SaveTokenDevice,x_token: str = Header(...)):
    return postingController.save_token_device(data,x_token)

    



