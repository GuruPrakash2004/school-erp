from pydantic import BaseModel


class LoginRequest(BaseModel):
    school_id: int
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
