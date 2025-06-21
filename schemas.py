from datetime import datetime

from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class VerificationCodeSchema(BaseModel):
    email: str
    code: str


class ToDoDateSchema(BaseModel):
    start_date: datetime
    end_date: datetime
