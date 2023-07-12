from datetime import date
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, PositiveInt, constr, validator


class UserBase(BaseModel):
    username: constr(min_length=4, max_length=20)
    email: EmailStr

    @validator("username")
    def strip_whitespace(cls, v):
        if len(v.strip()) < 4:
            raise HTTPException(status_code=400, detail=f"Username cannot be empty or consist only of whitespace")
        return v.strip()


class UserCreate(UserBase):
    password: constr(min_length=6)

    @validator("password")
    def check_whitespace(cls, v):
        if " " in v:
            raise HTTPException(status_code=400, detail="Password cannot contain spaces")
        return v


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: PositiveInt
    name: Optional[str] = None
    surname: Optional[str] = None
    hashed_password: str
    registration_date: date

    class Config:
        orm_mode = True


class User(UserInDB):
    pass


class ExtraUserFields(BaseModel):
    name: str
    surname: str
