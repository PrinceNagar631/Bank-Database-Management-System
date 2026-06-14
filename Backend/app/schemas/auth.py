from pydantic import BaseModel


class LoginRequest(BaseModel):

    username: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


class UserResponse(BaseModel):

    user_id: str

    class Config:
        from_attributes = True