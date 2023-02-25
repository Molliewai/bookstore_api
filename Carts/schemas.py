import pydantic as _pydantic
import datetime as _dt

from pydantic import BaseConfig
from Users import schemas as _UserSchema
from Books import schemas as _BookSchema

BaseConfig.arbitrary_types_allowed = True


class _CartBase(_pydantic.BaseModel):
    books: list[_BookSchema.Book] = []
    
    
class CartCreate(_CartBase):
    pass


class Cart(_CartBase):
    id: int
    user_id: int
    user: _UserSchema.User
    date_created: _dt.datetime
    date_last_updated: _dt.datetime
    
    class Config:
        orm_mode = True
        

class ReadCart(_CartBase):
    id: int
    
    class Config:
        orm_mode = True