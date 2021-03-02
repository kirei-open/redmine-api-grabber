from fastapi import Depends, APIRouter
from app.services import redmine


router = APIRouter()


@router.get("/")
def get_all_users():
    return redmine.get_all_users()