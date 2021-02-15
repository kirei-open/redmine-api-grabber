from fastapi import APIRouter
from app.services import redmine

router = APIRouter()


@router.get("/graph")
async def graph_issues(sdate: str, edate: str):
    return redmine.get_issues_graph(sdate, edate)


@router.get("/assigned_for/{name}")
async def get_assigned_issues(name):
    return redmine.get_issues_assigned_for(name)