import fastapi as _fastapi
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from dependencies import get_db
import os
import uuid
import shutil, json

router = _fastapi.APIRouter(prefix="/api/books", tags=["Books"])

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

@router.post("/", response_model=_schemas.Book)
async def create_book(
    book: str = _fastapi.Form(...),
    category_id: int = _fastapi.Form(...),
    db: _orm.Session = _fastapi.Depends(get_db),
    image: _fastapi.UploadFile = _fastapi.File(...)
):
    book_data = json.loads(book)
    # save image with a unique name
    file_name = str(uuid.uuid4()) + "." + image.filename.split(".")[-1]
    with open(os.path.join(UPLOAD_DIR, file_name), "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    book_data["image_path"] = file_name

    book_obj = await _services.create_book(
        db=db, book_data=book_data, category_id=category_id
    )


    return book_obj



@router.get("/", response_model=list[_schemas.Book])
async def get_books(db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_books(db=db)


@router.get("/{book_id}", response_model=_schemas.Book)
async def get_book(book_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_book(book_id=book_id, db=db)


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.delete_book(book_id=book_id, db=db)

    return {"message": "Book Successfully Deleted."}