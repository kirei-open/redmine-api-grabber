from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "hello world",
    }