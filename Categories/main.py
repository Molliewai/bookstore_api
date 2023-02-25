import fastapi as _fastapi
import sqlalchemy.orm as _orm
from . import schemas as _schemas
from . import services as _services
from dependencies import get_db

router = _fastapi.APIRouter(prefix="/api/categories", tags=["Categories"])


@router.post("/", response_model=_schemas.Category)
async def create_category(category: _schemas.CategoryCreate, db: _orm.Session = _fastapi.Depends(get_db)):
    category_obj = await _services.create_category(category=category, db=db)

    return category_obj


@router.get("/", response_model=list[_schemas.Category])
async def get_categories(db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_categories(db=db)



@router.get("/{cat_id}", response_model=_schemas.Category)
async def get_category(cat_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_category(cat_id=cat_id, db=db)



@router.delete("/{cat_id}")
async def delete_category(cat_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.delete_category(cat_id=cat_id, db=db)

    return {"message": "Category Successfully Deleted"}