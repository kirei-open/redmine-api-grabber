from .redmine import count_issues_before_date
from datetime import datetime
from dateutil.relativedelta import relativedelta


def insert_issues_statuses():
    db = sql_connection("redmine")
    cursor = db.cursor()
    now = (datetime.now() + relativedelta(days=1)).strftime("%Y-%m-%d")
    status = count_issues_before_date(now)
    datetime_now = (
        (datetime.now() + relativedelta(hours=7))
        .replace(minute=0, second=0)
        .strftime("%Y-%m-%d %H:%M:%S")
    )
    query = "INSERT INTO issues_graph (new, closed, in_progress, feedback, datetime) VALUES ({},{},{},{},'{}')".format(
        status["New"],
        status["Closed"],
        status["In Progress"],
        status["Feedback"],
        datetime_now,
    )
    # try:
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    # except Exception as e:
    # print(e)
    return


from ..main import sql_connection