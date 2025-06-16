from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class VerificationCodeSchema(BaseModel):
    email: str
    code: str
