import pydantic as _pydantic
from pydantic import BaseConfig

BaseConfig.arbitrary_types_allowed = True


class _CategoryBase(_pydantic.BaseModel):
    category: str


class CategoryCreate(_CategoryBase):
    pass


class CategoryUpdate(_CategoryBase):
    pass


class Category(_CategoryBase):
    id: int

    class Config:
        orm_mode = True
