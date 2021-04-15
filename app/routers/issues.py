from fastapi import APIRouter, Depends, Header
from ..main import redis_cache
from fastapi_cache.backends.redis import RedisCacheBackend
from app.controller import issuesController

router = APIRouter()


@router.get("/recents")
async def get_recent_issues(cache : RedisCacheBackend = Depends(redis_cache),x_token: str = Header(...)):
    data = await issuesController.get_recent_issues(cache, x_token)
    return data

@router.get("/graph")
async def graph_issues(sdate: str, edate: str, cache : RedisCacheBackend = Depends(redis_cache),x_token: str = Header(...)):
    data = await issuesController.graph_issues(sdate, edate, cache, x_token)
    return data


@router.get("/assigned_for/{name}")
async def get_assigned_issues(name, cache : RedisCacheBackend = Depends(redis_cache), x_token: str = Header(...)):
    data = await issuesController.get_assigned_issues(name, cache, x_token)
    return data