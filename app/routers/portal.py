from fastapi import Depends ,APIRouter, File, Form, UploadFile, Header
from app.services import posting, portal
from typing import List
from app import schemas
from typing import Optional
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials
from ..main import redis_cache
from fastapi_cache.backends.redis import RedisCacheBackend
from app.controller import postingController


cred = credentials.Certificate("firebase/kireiportal-firebase-adminsdk-n5ag8-8f4d88463f.json")
firebase_admin.initialize_app(cred)


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

def get_birthday():
    # Firebase Cloud Messaging
    birthday = portal.get_birthday_today()
    print(len(birthday))
    if len(birthday) > 0:
        for x in birthday:
            condition = "'ultah' in topics"
            name = x['fullname']
            birthday = x['birthday']
            print(name, birthday)
            message = messaging.Message(
                notification=messaging.Notification(
                    title='Selamat Ulang tahun',
                    body=str(name),
                ),
                condition=condition,
            )
            response = messaging.send(message)
            print('Successfully sent message:', response)
    



