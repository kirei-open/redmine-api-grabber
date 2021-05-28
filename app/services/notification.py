from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials
from app.services import portal as portalServices
from datetime import datetime,date
from ..main import sql_connection
from dotenv import load_dotenv
from pytanggalmerah import TanggalMerah
import requests
import os

load_dotenv('.env')


cred = credentials.Certificate("firebase/kireiportal-firebase-adminsdk-n5ag8-8f4d88463f.json")
firebase_admin.initialize_app(cred)

firebase_key = os.getenv("FIREBASE_KEY")

def send_birthday_firebase():
    # Firebase Cloud Messaging
    birthday = portalServices.get_birthday_today()
    print(len(birthday))
    if len(birthday) > 0:
        for x in birthday:
            condition = "'ultah' in topics"
            name = x['fullname']
            birthday = x['birthday']
            print(name, birthday)
            message = messaging.Message(
                notification=messaging.Notification(
                    title='\U0001F389'+' Selamat Ulang tahun '+'\U0001F382'+'\U0001F973',
                    body='\U0001F338 '+str(name)+' \U0001F338',
                ),
                condition=condition,
            )
            response = messaging.send(message)
            print('Successfully sent message:', response)

def get_holiday_date():
    t = TanggalMerah()
    tanggalMerah = t.check()
    if tanggalMerah == False:
        datenow = datetime.today().strftime("%A")
        if datenow == "Saturday":
            return True
        else:
            return False
    return tanggalMerah


def send_notif_absen_masuk():
    getHoliday = get_holiday_date()
    if getHoliday == False:
        condition = "'absen_masuk' in topics"
        message = messaging.Message(
            notification=messaging.Notification(
                title='Kirei Absen Masuk',
                body='Jangan lupa absen masuk\nSelamat Bekerja \U0001F60A',
            ),
            condition=condition,
        )
        response = messaging.send(message)
        print('Successfully sent message:', response)

def send_notif_absen_keluar():
    getHoliday = get_holiday_date()
    if getHoliday == False:
        condition = "'absen_keluar' in topics"
        message = messaging.Message(
            notification=messaging.Notification(
                title='Kirei Absen Keluar \U0001F6F5',
                body='Jangan lupa absen keluar\nHati-hati diperjalanan pulang \U0001F917',
            ),
            condition=condition,
        )
        response = messaging.send(message)
        print('Successfully sent message:', response)

def get_token_by_fullname(fullname):
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "SELECT * FROM tbl_token_device WHERE token_name = '{}'".format(fullname)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data

def notif_send(notif):
    token_device = get_token_by_fullname(notif['name'])
    if len(token_device) > 0:
        notif['body']['registration_ids'].append(token_device[0]['token_device'])
        headers = {'Content-Type':'application/json',
            'Authorization':f'key={firebase_key}'}
        url = 'https://fcm.googleapis.com/fcm/send'
        send_notif = requests.post(url, headers=headers,json=notif['body'])
        response = send_notif.json()
        success = response['success']
        message_id = response['results'][0]['message_id']
        data = f'succes send notification {success} id = {message_id}'
        return data

def send_notif_per_device(data):
    notif_data = []
    for row in data:
        issues = row['issues']
        for issuesrow in issues:
            created_on = issuesrow['created_on']
            due_date = issuesrow['due_date']
            project_name = issuesrow['project']['name']
            issuesname = issuesrow['subject']
            if 'assigned_to' in issuesrow.keys():
                assigned_to = issuesrow['assigned_to']['name']
                today = date.today()
                current_date = today.strftime('%Y-%m-%d')
                created_on_obj = datetime.strptime(created_on,'%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
                notif = {"name":"name","body":{"registration_ids": [],
                        "notification": {
                            "body": "body",
                            "title": "title"
                            }
                        }}
                if issuesrow['status']['name'] == "New" and current_date == created_on_obj:
                    notif['name'] = assigned_to
                    notif['body']['notification']['body'] = 'New Issues'
                    notif['body']['notification']['title'] = f"{project_name}\n{issuesname}"
                    response_notif = notif_send(notif)
                    if response_notif != None:
                        notif_data.append(response_notif)

                elif due_date != None:
                    due_date_obj = datetime.strptime(due_date,'%Y-%m-%d') 
                    if due_date_obj < datetime.today() and issuesrow['status']['name'] == "New":
                        notif['name'] = assigned_to
                        notif['body']['notification']['body'] = 'Issues over due'
                        notif['body']['notification']['title'] = f"{project_name}\n{issuesname}"
                        response_notif = notif_send(notif)
                        if response_notif != None:
                            notif_data.append(response_notif)
                    
                    elif due_date_obj < datetime.today() and issuesrow['status']['name'] == "In Progress":
                        notif['name'] = assigned_to
                        notif['body']['notification']['body'] = 'Issues over due'
                        notif['body']['notification']['title'] = f"{project_name}\n{issuesname}"
                        response_notif = notif_send(notif)
                        if response_notif != None:
                            notif_data.append(response_notif)
    # print(notif_data)
    print(notif_data)