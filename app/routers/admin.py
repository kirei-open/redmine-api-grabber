from fastapi import APIRouter, Depends
from app.services import portal

router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "hello world",
    }


@router.get("/absence")
async def get_absence(date: str):
    return portal.get_absence(date)


@router.get("/piket")
async def get_piket_schedule():
    return portal.get_piket_schedule()


@router.get("/agenda")
async def get_agenda(date_start: str, date_end: str):
    return portal.get_agenda(date_start, date_end)