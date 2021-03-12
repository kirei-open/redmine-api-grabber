from itertools import groupby
from pprint import pprint
import urllib.parse
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def count_status(issues):
    closed_status = ["Resolved", "Closed"]
    result = {
        "New": 0,
        "Closed": 0,
        "In Progress": 0,
        "Feedback": 0,
    }
    for issue in issues:
        if issue["status"]["name"] == "New":
            result["New"] += 1
        elif issue["status"]["name"] == "In Progress":
            result["In Progress"] += 1
        elif issue["status"]["name"] == "Feedback":
            result["Feedback"] += 1
        elif issue["status"]["name"] in closed_status:
            result["Closed"] += 1
    return result


def get_all_projects():
    return sorted(
        list(redmine.project.all().filter(is_public=True).values()),
        key=lambda x: x["id"],
    )


def get_project_by_id(project_id):
    project = redmine.project.get(project_id)
    issues = [
        i
        for i in list(
            redmine.issue.filter(status_id="*", project_id=project_id).values()
        )
        if i["is_private"] == False
    ]
    result = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "members": project.memberships.values(),
        "status_count": count_status(issues),
        "issues": issues,
    }
    return result

def get_all_project_detail():
    results = []
    projects = get_all_projects()
    for project in projects:
        result = get_project_by_id(project["id"])
        result["issues"] = sorted(result["issues"], key=lambda x:x["created_on"], reverse=True)[:10]
        results.append(result)
    return results

def get_project_membership(project_id):
    project = redmine.project.get(project_id)
    return list(project.memberships.values())


# Issue For Assigned Name


def get_most_recent_issues():
    all_issues = (
        list(
            redmine.issue.all(
                sort="created_on:desc",
                include=[
                    "project",
                    "status",
                    "subject",
                    "assigned_to",
                    "tracker",
                    "priority",
                ],
                limit=10,
            )
            .filter(is_private=False)
            .values()
        ),
    )
    return all_issues


def get_issues_assigned_for(name):
    name = urllib.parse.unquote(name)
    all_issues = sorted(
        list(
            redmine.issue.all(
                include=[
                    "project",
                    "status",
                    "subject",
                    "assigned_to",
                    "tracker",
                    "priority",
                ]
            )
            .filter(assigned_to__name=name, is_private=False)
            .values()
        ),
        key=lambda x: x["project"]["name"],
    )
    # pprint(all_issues)
    grouped_issues = [
        (project_name, list(issues))
        for project_name, issues in groupby(
            all_issues, key=lambda x: x["project"]["name"]
        )
    ]
    result = {
        "summary": count_status(all_issues),
        "issues": sorted(all_issues, key=lambda x: x["priority"]["id"], reverse=True),
        "projects": [
            {
                "id": issues[0]["project"]["id"],
                "name": project_name,
                "status_count": count_status(issues),
                "members": [
                    {"name": name["user"]["name"], "roles": name["roles"]}
                    for name in get_project_membership(issues[0]["project"]["id"])
                ],
                # "issues": issues,
            }
            for project_name, issues in grouped_issues
        ],
    }
    return result


# All Project Summary
def get_all_project_summary():
    all_issues = sorted(
        [i for i in list(redmine.issue.all().values()) if i["is_private"] == False],
        key=lambda x: x["project"]["name"],
    )
    grouped_issues = [
        (project_name, list(issues))
        for project_name, issues in groupby(
            all_issues, key=lambda x: x["project"]["name"]
        )
    ]
    projects = [
        {
            "id": issues[0]["project"]["id"],
            "name": project_name,
            "status_count": count_status(issues),
            "members": [
                {"name": name["user"]["name"]}
                for name in get_project_membership(issues[0]["project"]["id"])
            ],
        }
        for project_name, issues in grouped_issues
    ]
    return projects


def get_open_issues_before_date_by_project_id(sdate, edate, project_id):
    try:
        issues = sorted(
            list(
                redmine.issue.filter(
                    project_id=project_id,
                    status_id="open",
                    updated_on="><{}|{}".format(sdate, edate),
                ).values()
            ),
            key=lambda x: x["updated_on"],
        )
        # pprint(issues)
        grouped_by_date = [
            {
                "date": k + ":00:00Z",
                "count": len([i for i in list(v) if i["is_private"] == False]),
            }
            for k, v in groupby(issues, key=lambda x: x["updated_on"][:13])
        ]
        df = pd.DataFrame.from_dict(grouped_by_date)
        df["count"] = df["count"].cumsum()
        hourly_date_rng = pd.date_range(
            start=df["date"].iloc[0], end=df["date"].iloc[-1], freq="H"
        )
        hourly_date_rng.name = "date"
        df["date"] = pd.to_datetime(df["date"])
        return (
            df.set_index("date")
            .reindex(hourly_date_rng)
            .fillna(method="ffill")
            .reset_index()
            .to_dict(orient="records")
        )
    except:
        return


def get_open_issues_before_date(sdate, edate):
    try:
        issues = sorted(
            list(
                redmine.issue.filter(
                    status_id="*",
                    updated_on="><{}|{}".format(sdate, edate),
                ).values()
            ),
            key=lambda x: x["updated_on"],
        )
        grouped_by_date = [
            {
                "date": k,
                "count": len(
                    [
                        i
                        for i in list(v)
                        if (i["status"]["id"] and i["is_private"] == False)
                    ]
                ),
            }
            for k, v in groupby(issues, key=lambda x: x["updated_on"][:13])
        ]

        # return grouped_by_date
        df = pd.DataFrame.from_dict(grouped_by_date)
        # print(df)
        df["count"] = df["count"].cumsum()
        hourly_date_rng = pd.date_range(
            start=df["date"].iloc[0], end=df["date"].iloc[-1], freq="H"
        )
        hourly_date_rng.name = "date"
        df["date"] = pd.to_datetime(df["date"])
        return (
            df.set_index("date")
            .reindex(hourly_date_rng)
            .fillna(method="bfill")
            .reset_index()
            .to_dict(orient="records")
        )
    except Exception as e:
        print(e)
        return


def count_issues_before_date(edate):
    issues = sorted(
        [
            i
            for i in list(
                redmine.issue.filter(
                    status_id="*",
                    updated_on="<={}".format(edate),
                ).values()
            )
            if i["is_private"] == False
        ],
        key=lambda x: x["updated_on"],
    )
    return count_status(issues)


def get_issues_graph(sdate, edate):
    sdate = datetime.strptime(sdate, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
    edate = (datetime.strptime(edate, "%Y-%m-%d") + relativedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    db = sql_connection("redmine")
    cursor = db.cursor(dictionary=True)
    query = "SELECT id, datetime AS date, (new + in_progress + feedback) AS count FROM issues_graph WHERE datetime<='{}' AND datetime>='{}' ORDER BY id ASC".format(
        edate, sdate
    )
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def get_all_users():
    users = list(redmine.user.all().values())
    for user in users:
        user["fullname"] = " ".join([user["firstname"], user["lastname"]])
    return list(users)


from ..main import redmine, sql_connection