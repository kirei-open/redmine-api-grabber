from fastapi import APIRouter
from app.services import redmine

router = APIRouter()


@router.get("/recents")
def get_recent_issues():
    return redmine.get_most_recent_issues()[0]


@router.get("/graph")
def graph_issues(sdate: str, edate: str):
    return redmine.get_issues_graph(sdate, edate)


@router.get("/assigned_for/{name}")
def get_assigned_issues(name):
    return redmine.get_issues_assigned_for(name)