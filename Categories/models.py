import sqlalchemy as _sql
import sqlalchemy.orm as _orm

from Database.database import Base


class Category(Base):
    __tablename__ = "categories"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    category = _sql.Column(_sql.String, index=True, unique=True)

    books = _orm.relationship("Book", back_populates="category")
