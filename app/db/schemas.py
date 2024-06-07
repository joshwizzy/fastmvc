from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PostCreate(BaseModel):
    text: str = Field(max_length=1048576)


class PostOut(BaseModel):
    id: int
    text: str
    owner_id: int

    class Config:
        orm_mode = True
