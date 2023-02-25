import pydantic as _pydantic
import datetime as _dt
from Users import schemas as _UserSchema

class _FeedbackBase(_pydantic.BaseModel):
    feedback: str


class FeedbackCreate(_FeedbackBase):
    pass


class Feedback(_FeedbackBase):
    id: int
    user: _UserSchema.User
    date_created: _dt.datetime

    class Config:
        orm_mode = True