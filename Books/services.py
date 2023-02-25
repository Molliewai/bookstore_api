import fastapi as _fastapi
import datetime as _dt
from . import schemas as _BookSchema
from . import models as _BookModel
import sqlalchemy.orm as _orm
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

# GET SINGLE BOOK BY ID
async def get_book(db: _orm.Session, book_id: int):
    return db.query(_BookModel.Book).filter(_BookModel.Book.id == book_id).first()


# GET ALL BOOKS
async def get_books(db: _orm.Session):
    books = db.query(_BookModel.Book)

    return list(map(_BookSchema.Book.from_orm, books))


# CREATE BOOK
async def create_book(db: _orm.Session, book_data: dict, category_id: int):
    book = _BookModel.Book(**book_data, category_id=category_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


# DELETE BOOK
async def delete_book(db: _orm.Session, book_id: int):
    book_obj = db.query(_BookModel.Book).filter(_BookModel.Book.id == book_id).first()

    db.delete(book_obj)
    db.commit()
    
    try:
        os.remove(os.path.join(UPLOAD_DIR, book_obj.image_path))
    except:
        pass
    return {"message": "Book deleted successfully"}


