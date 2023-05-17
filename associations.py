# associations.py
import sqlalchemy as _sql
from Database.database import Base

cart_books = _sql.Table(
    "cart_books",
    Base.metadata,
    _sql.Column("cart_id", _sql.Integer, _sql.ForeignKey("carts.id")),
    _sql.Column("book_id", _sql.Integer, _sql.ForeignKey("books.id"))
)
