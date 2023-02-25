import fastapi as _fastapi
import sqlalchemy.orm as _orm
from . import schemas as _schemas
from . import services as _services
from dependencies import get_db


router = _fastapi.APIRouter(prefix="/api/carts", tags=["Carts"])


@router.get("/", response_model=list[_schemas.Cart])
async def get_carts(db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_carts(db=db)


@router.post("/{book_id}")
async def add_book_to_cart(book_id: int, user_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.add_to_cart(book_id=book_id, user_id=user_id, db=db)
    
    return {"message": "Book Added To Cart."}


@router.delete("/{user_id}/{book_id}")
async def delete_book_from_cart(user_id: int, book_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.delete_book_from_cart(user_id=user_id, book_id=book_id, db=db)
    
    return {"message": "Book deleted from cart."}



@router.post("/checkout/{user_id}")
async def checkout(user_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.checkout(user_id=user_id, db=db)
    
    return {"message": "Checkout Success."}