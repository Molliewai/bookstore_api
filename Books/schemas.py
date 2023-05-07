import pydantic as _pydantic
from pydantic import BaseConfig
import datetime as _dt
from Categories import schemas as _CategorySchema

BaseConfig.arbitrary_types_allowed = True


class _BookBase(_pydantic.BaseModel):
    title: str
    desc: str
    total_pages: int
    price: int
    author: str


class BookCreate(_BookBase):
    image_path: str
    pass


class BookUpdate(_BookBase):
    category_id: int
    pass


class Book(_BookBase):
    id: int
    image_path: str
    category: _CategorySchema.Category
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True
