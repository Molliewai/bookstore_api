import fastapi as _fastapi
import sqlalchemy.orm as _orm
from . import schemas as _FeedbackSchema
from . import models as _FeedbackModel
from Users import models as _UserModel


async def get_feedback(db: _orm.Session, feedback_id: int):
    return db.query(_FeedbackModel.Feedback).filter(_FeedbackModel.Feedback.id == feedback_id).first()


async def get_feedbacks(db: _orm.Session):
    feedbacks = db.query(_FeedbackModel.Feedback)

    return list(map(_FeedbackSchema.Feedback.from_orm, feedbacks))


async def create_feedback(db: _orm.Session, feedback: _FeedbackSchema.FeedbackCreate, user_id: int):
    user = db.query(_UserModel.User).filter(_UserModel.User.id == user_id)

    if user is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="User not Found."
        )

    feedback_obj = _FeedbackModel.Feedback(**feedback.dict(), user_id=user_id)
    db.add(feedback_obj)
    db.commit()
    db.refresh(feedback_obj)
    return feedback_obj


async def delete_feedback(db: _orm.Session, feedback_id: int):
    feedback_obj = db.query(_FeedbackModel.Feedback).filter(_FeedbackModel.Feedback.id == feedback_id).first()

    db.delete(feedback_obj)
    db.commit()