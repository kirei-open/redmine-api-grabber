from fastapi import APIRouter
from app.services import redmine


router = APIRouter()


@router.get("/")
async def get_all_projects():
    return redmine.get_all_projects()


@router.get("/summary")
async def get_all_project_summary():
    return redmine.get_all_project_summary()

@router.get("/details")
async def get_all_project_detail():
    return redmine.get_all_project_detail()

@router.get("/{id}")
async def get_project_by_id(id: int):
    return redmine.get_project_by_id(id)


@router.get("/graph/{id}")
async def get_graph_by_project_id(id: int, sdate: str, edate: str):
    return redmine.get_open_issues_before_date_by_project_id(sdate, edate, id)