import sqlalchemy as _sql
from sqlalchemy.ext.mutable import MutableList
import sqlalchemy.orm as _orm
import passlib.hash as _hash

from Database.database import Base


class User(Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    cart = _sql.Column(MutableList.as_mutable(_sql.PickleType), default=[])

    books = _orm.relationship("Book", back_populates="owner")
    feedbacks = _orm.relationship("Feedback", back_populates="user")
    cart = _orm.relationship("Cart", back_populates="user")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
