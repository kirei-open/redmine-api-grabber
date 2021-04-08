from typing import List, Optional

from pydantic import BaseModel

class Comment(BaseModel):
    id: int
    comment: str
    post_id:int
    user_id:int

    class Config:
        orm_mode: True

class Post(BaseModel):
    id: int
    description: str
    date: str
    user_id: int
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
