from pydantic import BaseModel, EmailStr

class GroupLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginRequest(BaseModel):
    phone: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
