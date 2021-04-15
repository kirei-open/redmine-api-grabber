from fastapi import APIRouter, Depends, Header
from app.services import redmine, redisCache
from ..main import redis_cache
from fastapi_cache.backends.redis import RedisCacheBackend
from app.controller import projectsController


router = APIRouter()


@router.get("/")
async def get_all_projects(cache : RedisCacheBackend = Depends(redis_cache), x_token: str = Header(...)):
    data = await projectsController.get_all_projects(cache, x_token)
    return data


@router.get("/summary")
async def get_all_project_summary(cache : RedisCacheBackend = Depends(redis_cache), x_token: str = Header(...)):
    data = await projectsController.get_all_project_summary(cache, x_token)
    return data


@router.get("/details")
async def get_all_project_detail(cache : RedisCacheBackend = Depends(redis_cache), x_token: str = Header(...)):
    data = await projectsController.get_all_project_detail(cache, x_token)
    return data


@router.get("/{id}")
async def get_project_by_id(id: int, x_token: str = Header(...),cache : RedisCacheBackend = Depends(redis_cache)):
    data = await projectsController.get_project_by_id(id, cache, x_token)
    return data

@router.get("/graph/{id}")
async def get_graph_by_project_id(id: int, sdate: str, edate: str):
    data = redmine.get_open_issues_before_date_by_project_id(sdate, edate, id)
    return data