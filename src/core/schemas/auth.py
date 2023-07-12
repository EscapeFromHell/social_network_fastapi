from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt, constr


class SuccessAuth(BaseModel):
    access_token: str
    token_type: str


class SuccessSignUp(BaseModel):
    id: PositiveInt
    username: constr(min_length=4, max_length=20)
    email: EmailStr
    registration_date: date


class TokenData(BaseModel):
    user_id: Optional[PositiveInt] = None
