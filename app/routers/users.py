from fastapi import APIRouter
from app.services import redmine


router = APIRouter()


@router.get("/")
async def get_all_users():
    return redmine.get_all_users()