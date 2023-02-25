from typing import Optional, List
import pydantic as _pydantic
from pydantic import BaseConfig
from Books import schemas as _BookSchema

BaseConfig.arbitrary_types_allowed = True


class _UserBase(_pydantic.BaseModel):
    username: str
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserAuth(_UserBase):
    hashed_password: str
    id: int

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int
    books: List[_BookSchema.Book] = []

    class Config:
        orm_mode = True
