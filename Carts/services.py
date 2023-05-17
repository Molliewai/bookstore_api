import fastapi as _fastapi
import datetime as _dt
import sqlalchemy.orm as _orm
from . import schemas as _schemas
from . import models as _models
from Users import models as _UserModel
from Users import schemas as _UserSchema
from Books import models as _BookModel
from Books import schemas as _BookSchema


async def get_carts(db: _orm.Session):
    carts = db.query(_models.Cart)

    return list(map(_schemas.Cart.from_orm, carts))


async def add_to_cart(db: _orm.Session, book_id: int, user_id: int):
    user = db.query(_UserModel.User).filter(
        _UserModel.User.id == user_id).first()

    if user is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="User not Found."
        )

    cart = db.query(_models.Cart).filter(
        _models.Cart.user_id == user_id).first()

    book = db.query(_BookModel.Book).filter(
        _BookModel.Book.id == book_id).first()

    if book is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="Book not Found."
        )

    books_in_cart = cart.books

    if book not in books_in_cart:
        cart.id = cart.id
        cart.user_id = cart.user_id
        cart.books = cart.books + [book]
        cart.date_created = cart.date_created
        cart.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(cart)

    return _schemas.Cart.from_orm(cart)


async def delete_book_from_cart(user_id: int, book_id: int, db: _orm.Session):
    cart = db.query(_models.Cart).filter(
        _models.Cart.user_id == user_id).first()

    if cart is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="Cart not Found."
        )

    book = db.query(_BookModel.Book).filter(
        _BookModel.Book.id == book_id).first()

    if book is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="Book not Found."
        )

    if book in cart.books:
        cart.books.remove(book)

    db.commit()
    db.refresh(cart)

    return _schemas.Cart.from_orm(cart)


async def checkout(db: _orm.Session, user_id: int):
    user = db.query(_UserModel.User).filter(
        _UserModel.User.id == user_id).first()

    if user is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="User Not Found."
        )

    cart = db.query(_models.Cart).filter(
        _models.Cart.user_id == user_id).first()

    books_in_cart = cart.books

    cart.books = []
    db.commit()
    db.refresh(cart)

    if books_in_cart:
        user.id = user.id
        user.username = user.username
        user.email = user.email
        user.books = user.books + books_in_cart

    db.commit()
    db.refresh(user)

    return _UserSchema.User.from_orm(user)
