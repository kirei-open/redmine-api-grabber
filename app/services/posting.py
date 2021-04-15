from datetime import datetime
from dateutil.relativedelta import relativedelta
from app import schemas
from ..main import sql_connection
from fastapi import File, UploadFile, HTTPException
from typing import Optional
from app.middleware import Jwtdecode
import json
import string
import random
import time


def get_post():
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    # query = "SELECT l.post_id AS id, l.post_desc AS description, l.post_user_id AS user_id, date_format(l.post_date,'%Y-%m-%d %T') AS date, ( SELECT JSON_EXTRACT( IFNULL( CONCAT( '[', GROUP_CONCAT( JSON_OBJECT( 'id', a.id, 'comment', a.comment,'user_id', a.user_id , 'post_id', a.post_id) ), ']' ) ,'[]'),'$') FROM tbl_comment AS a WHERE a.post_id = l.post_id ) AS comment FROM post as l"
    # query = "SELECT a.post_id AS id, a.post_desc AS description, a.post_user_id AS user_id, date_format(a.post_date,'%Y-%m-%d %T') AS date, IFNULL(CONCAT( '[', GROUP_CONCAT( JSON_OBJECT( 'id', b.id, 'comment', b.comment,'user_id', b.user_id , 'post_id', b.post_id) ), ']' ),'[]') AS comment FROM post AS a LEFT JOIN tbl_comment AS b ON a.post_id = b.post_id GROUP BY a.post_id, a.post_desc"
    query = "SELECT l.post_id AS id, l.post_desc AS description, l.post_user_id AS user_id, date_format(l.post_date,'%Y-%m-%d %T') AS date, ( SELECT IFNULL( CONCAT( '[', GROUP_CONCAT( JSON_OBJECT( 'id', a.id, 'comment', a.comment,'user_id', a.user_id , 'post_id', a.post_id) ), ']' ) ,'[]') FROM tbl_comment AS a WHERE a.post_id = l.post_id ) AS comment FROM post as l"
    cursor.execute(query)
    data = cursor.fetchall()
    for i in data:
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
    
    
    
