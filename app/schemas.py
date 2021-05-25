from typing import List, Optional

from pydantic import BaseModel

class Comment(BaseModel):
    id: int
    comment: str
    post_id:int
    user_id:int
    name: str

    class Config:
        orm_mode: True

class Post(BaseModel):
    id: int
    description: str
    date: str
    user_id: str
    name: str
    photo: str
    comment: List[Comment] = []

    class Config:
        orm_mode = True

class CreatePost(BaseModel):
    description: str


class CreateLaporan(BaseModel):
    project : str
    description : str

class CreateComment(BaseModel):
    comment: str
    post_id: int

class SaveTokenDevice(BaseModel):
    token_device: str
