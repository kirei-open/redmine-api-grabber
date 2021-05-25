from datetime import datetime
from dateutil.relativedelta import relativedelta
from app import schemas
from ..main import sql_connection
from fastapi import HTTPException
from app.middleware import Jwtdecode
from dotenv import load_dotenv
import requests
import json
import string
import random
import time
import os

load_dotenv()

token = os.getenv('TOKEN')
akun_url = os.getenv('AKUN_URL')


def get_post():
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    headers = {'x-token':token}
    url = '{}/users/?skip=0&limit=100'.format(akun_url)
    user = requests.get(url, headers=headers)
    userData = user.json()
    query = "SELECT l.post_id AS id, l.post_desc AS description, l.post_user_id as user_id , u.fullname AS name, date_format(l.post_date,'%Y-%m-%d %T') AS date, ( SELECT IFNULL( CONCAT( '[', GROUP_CONCAT( JSON_OBJECT( 'id', a.id, 'comment', a.comment,'user_id', a.user_id , 'post_id', a.post_id , 'name', b.fullname, 'date' ,date_format(a.date,'%Y-%m-%d %T')) ), ']' ) ,'[]') FROM tbl_comment AS a JOIN tbl_user as b ON b.id_user = a.user_id WHERE a.post_id = l.post_id ) AS comment FROM post as l JOIN tbl_user as u ON u.id_user = l.post_user_id order by l.post_date desc"
    cursor.execute(query)
    data = cursor.fetchall()
    for i in data:
        for index, item in enumerate(userData):
            if item['id'] == i['user_id']:
                if len(item['profile']) > 0:
                    if item['profile'][0]['photo'] is not None:
                        i['photo'] = item['profile'][0]['photo']
                    else:
                        i['photo'] = 'profile.png'
                else:
                    i['photo'] = 'profile.png'
                break
        if i['comment'] != None:
            i['comment'] = json.loads(i['comment'])
    cursor.close()
    db_portal.close()
    return data


def create_post(post:schemas.CreatePost,token:str):
    dataUser = Jwtdecode.decoded(token=token)
    user_id = dataUser['id']
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "INSERT INTO post (post_desc,post_user_id,post_date) VALUES ('{}',{},NOW())".format(post.description,user_id)
    cursor.execute(query)
    db_portal.commit()
    data = {'message':"{}, data berhasil ditambahkan".format(cursor.rowcount)}
    cursor.close()
    db_portal.close()
    return data

def get_laporan(token):
    user = Jwtdecode.decoded(token)
    user_id = user['id']
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "SELECT * FROM tbl_report WHERE report_user_id = {}".format(user_id)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data

def get_laporan_date(date):
    sdate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
    edate = (datetime.strptime(date, "%Y-%m-%d") + relativedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    print(sdate,edate)
    query = "SELECT l.id_report, l.report_date, l.report_project, l.report_desc, l.report_user_id, u.fullname AS name FROM tbl_report as l JOIN tbl_user as u ON u.id_user = l.report_user_id WHERE l.report_date<='{}' AND l.report_date>='{}'".format(edate,sdate) 
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data

def create_laporan(laporan:schemas.CreateLaporan,token: str):
    dataUser = Jwtdecode.decoded(token=token)
    user_id = dataUser['id']
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    id_laporan = ''.join(random.choice(string.ascii_lowercase + string.digits)for i in range(10))
    query = "INSERT INTO tbl_report (id_report,report_date,report_project,report_desc,report_user_id) Values ('{}',Now(),%s,%s,%s)".format(id_laporan)
    createData = (laporan.project,laporan.description,user_id)
    cursor.execute(query,createData)
    db_portal.commit()
    data = {'message':"{}, laporan berhasil ditambahkan".format(cursor.rowcount)}
    cursor.close()
    db_portal.close()
    return data

def crete_comment(comment: schemas.CreateComment, token:str):
    dataUser = Jwtdecode.decoded(token=token)
    user_id = dataUser['id']
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "INSERT INTO tbl_comment (comment, date, post_id, user_id) VALUES (%s,NOW(),%s,%s)"
    createData = (comment.comment,comment.post_id,user_id)
    cursor.execute(query,createData)
    db_portal.commit()
    data = {'message':"{}, comment berhasil diposting".format(cursor.rowcount)}
    cursor.close()
    db_portal.close()
    return data

def create_absent(deskripsi, x_token, photo):
    user = Jwtdecode.decoded(token=x_token)
    user_id = user['id']
    photo_name = ""
    if photo != None:
        file_name = str(int(time.time() * 1000)) + "_"+  photo.filename
        photo_name = file_name.replace(" ", "")
        photo.filename = photo_name
        image_byte = photo.file.read()
        image_len = len(image_byte)
        if image_len > (3000000):
            raise HTTPException(status_code=400, detail="Ukuran file terlalu besar")
        target_path = 'static'
        url = target_path + "/" + photo_name 
        with open(url, "wb") as f:
            f.write(image_byte)
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "INSERT INTO absent (absent_date,absent_desc,absent_user_id,absent_photo) VALUES (NOW(),%s,%s,%s)"
    dataAbsent = (deskripsi,user_id,photo_name)
    cursor.execute(query,dataAbsent)
    db_portal.commit()
    data = {'message':"{}, Absent berhasil diposting".format(cursor.rowcount)}
    cursor.close()
    db_portal.close() 
    return data

def get_user(user_id):
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "SELECT id_user,fullname FROM tbl_user WHERE id_user = {}".format(user_id)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data

def save_token_device(data,token:str):
    dataUser = Jwtdecode.decoded(token=token)
    user_id = dataUser['id']
    getUser = get_user(user_id)
    fullname = getUser[0]['fullname']
    if len(getUser) > 0:
        db_portal = sql_connection("portal")
        cursor = db_portal.cursor(dictionary=True)
        query = "INSERT INTO tbl_token_device (token_name, token_device) VALUES (%s,%s) ON DUPLICATE KEY UPDATE token_device='{}'".format(data.token_device)
        createData = (fullname,data.token_device)
        cursor.execute(query,createData)
        db_portal.commit()
        response = {'message':"token device berhasil disimpan"}
        db_portal.close()
        return response
    else:
        return HTTPException(status_code=404, detail='User not found')
    
    
