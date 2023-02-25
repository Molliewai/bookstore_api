import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

from Database.database import Base


class Cart(Base):
    __tablename__ = "carts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    
    books = _orm.relationship("Book", back_populates="cart")
    user = _orm.relationship("User", back_populates="cart")