from app.services import notification as notificationServices, redmine as redmineServices

def get_birthday():
    return notificationServices.send_birthday_firebase()

def absen_masuk_notification():
    return notificationServices.send_notif_absen_masuk()

def absen_keluar_notification():
    return notificationServices.send_notif_absen_keluar()

def new_and_over_due_issues():
    print('send notification')
    data = redmineServices.get_all_project_detail()
    return notificationServices.send_notif_per_device(data)
    