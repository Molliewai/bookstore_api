import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

from Database.database import Base


class Book(Base):
    __tablename__ = "books"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    desc = _sql.Column(_sql.String, unique=True, index=True)
    total_pages = _sql.Column(_sql.Integer, index=True)
    price = _sql.Column(_sql.Integer, index=True)
    author = _sql.Column(_sql.String, index=True)
    image_path = _sql.Column(_sql.String, index=True)

    category_id = _sql.Column(_sql.Integer, _sql.ForeignKey("categories.id"))
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    cart_id = _sql.Column(_sql.Integer, _sql.ForeignKey("carts.id"))

    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="books")
    category = _orm.relationship("Category", back_populates="books")
    cart = _orm.relationship("Cart", back_populates="books")