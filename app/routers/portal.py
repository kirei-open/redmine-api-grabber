from fastapi import APIRouter, File, Form, UploadFile, Header
from app.services import posting
from app.services import portal
from typing import List
from app import schemas
from typing import Optional
from app.middleware import Jwtdecode
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase/kireiportal-firebase-adminsdk-n5ag8-8f4d88463f.json")
firebase_admin.initialize_app(cred)


router = APIRouter()

@router.get('/posting', response_model=List[schemas.Post])
def get_all_post():
    return posting.get_post();

@router.post('/posting')
def create_new_post(post: schemas.CreatePost, x_token: str = Header(...)):
    return posting.create_post(post=post, token=x_token);

@router.post('/comment')
def create_new_comment(comment: schemas.CreateComment, x_token: str = Header(...)):
    return posting.crete_comment(comment, token=x_token);

@router.get('/laporan')
def get_user_laporan(x_token: str = Header(...)):
    dataUser = Jwtdecode.decoded(token=x_token)
    return posting.get_laporan(user_id=dataUser['id']);

@router.post('/laporan')
def create_new_laporan(laporan: schemas.CreateLaporan, x_token: str = Header(...)):
    return posting.create_laporan(laporan=laporan, token=x_token);

@router.post('/absent')
def create_new_absent(deskripsi: str = Form (...), photo: Optional[UploadFile] = File(None), x_token: str = Header(...)):
    dataUser = Jwtdecode.decoded(token=x_token)
    return posting.create_absent(deskripsi=deskripsi, photo=photo, user_id = dataUser['id'])

def get_birthday():
    
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
    



