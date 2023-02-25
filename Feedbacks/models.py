import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

from Database.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    feedback = _sql.Column(_sql.String)

    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))

    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    user = _orm.relationship("User", back_populates="feedbacks")
