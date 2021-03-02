from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_birthday_today():
    datetime_now = (
        (datetime.now() + relativedelta(hours=7))
        .replace(minute=0, second=0)
        .strftime("%m-%d")
    )
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "SELECT fullname, birthday FROM tbl_user WHERE birthday LIKE '%{}%'".format(
        datetime_now
    )
    print(query)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data


def get_absence(date):
    sdate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    edate = (datetime.strptime(date, "%Y-%m-%d") + relativedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "SELECT absent_date, absent_desc, fullname FROM absent INNER JOIN tbl_user WHERE absent_user_id = tbl_user.id_user AND absent_date >= '{}' AND absent_date <= '{}'".format(
        sdate, edate
    )
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data


def get_agenda(date_start, date_end):
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "SELECT pengumuman, tanggal_kegiatan FROM tbl_pengumuman WHERE tanggal_kegiatan >= '{}' AND tanggal_kegiatan <= '{}'".format(
        date_start, date_end
    )
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data


def get_piket_schedule():
    map_day_indonesia = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu",
    }
    datetime_now = (
        (datetime.now() + relativedelta(hours=7))
        .replace(minute=0, second=0)
        .strftime("%A")
    )
    db_portal = sql_connection("portal")
    cursor = db_portal.cursor(dictionary=True)
    query = "SELECT user, hari_piket FROM tbl_piket WHERE hari_piket = '{}'".format(
        map_day_indonesia[datetime_now]
    )
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db_portal.close()
    return data


from ..main import sql_connection