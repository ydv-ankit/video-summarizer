from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str
    tokens: int = 0

    class Config:
        orm_mode = True

class CreateUser(UserBase):
    class Config:
        orm_mode = True