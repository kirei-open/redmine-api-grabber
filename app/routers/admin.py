from fastapi import APIRouter, Depends
from app.services import portal
from websocket import create_connection

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
  
@router.post("/testing-ws")
def testing_ws():
    ws = create_connection("ws://localhost:8000/ws")
    print("sending packet")
    ws.send("packet")
    print("sent")
    print("receiving")
    result=ws.recv()
    print(result)
    ws.close()

