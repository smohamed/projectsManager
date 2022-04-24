from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserRequest(UserBase):
    company_id: int


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
