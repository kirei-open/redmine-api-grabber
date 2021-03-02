from fastapi import APIRouter, Depends
from app.services import portal

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "hello world",
    }


@router.get("/birthday")
def get_birthday():
    return portal.get_birthday_today()


@router.get("/absence")
def get_absence(date: str):
    return portal.get_absence(date)


@router.get("/piket")
def get_piket_schedule():
    return portal.get_piket_schedule()


@router.get("/agenda")
def get_agenda(date_start: str, date_end: str):
    return portal.get_agenda(date_start, date_end)