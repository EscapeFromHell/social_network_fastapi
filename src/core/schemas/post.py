from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel, NonNegativeInt, PositiveInt, constr, validator


class PostBase(BaseModel):
    text: constr(min_length=1, max_length=560)

    @validator("text")
    def strip_whitespace(cls, v):
        if not v.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty or consist only of whitespace")
        return v.strip()


class PostCreate(PostBase):
    author_id: PositiveInt


class PostUpdate(PostBase):
    author_id: PositiveInt


class PostInDB(PostBase):
    id: PositiveInt
    publication_date: date
    likes: NonNegativeInt
    dislikes: NonNegativeInt

    class Config:
        orm_mode = True


class Post(PostInDB):
    author: str


class PostResponseMessage(BaseModel):
    message: str
