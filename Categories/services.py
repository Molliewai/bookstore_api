import fastapi as _fastapi
from . import schemas as _schemas
from . import models as _models
import sqlalchemy.orm as _orm


async def get_category(db: _orm.Session, cat_id: int):
    return db.query(_models.Category).filter(_models.Category.id == cat_id).first()


async def get_categories(db: _orm.Session):
    categories = db.query(_models.Category)

    return list(map(_schemas.Category.from_orm, categories))


async def create_category(db: _orm.Session, category: _schemas.CategoryCreate):
    category_obj = _models.Category(**category.dict())

    db.add(category_obj)
    db.commit()
    db.refresh(category_obj)

    return category_obj


async def update_category(db: _orm.Session, cat_id: int, category: _schemas.CategoryUpdate):
    category_obj = db.query(_models.Category).filter(
        _models.Category.id == cat_id).first()

    if not category_obj:
        return None

    for field, value in category.dict(exclude_unset=True).items():
        setattr(category_obj, field, value)

    db.add(category_obj)
    db.commit()
    db.refresh(category_obj)

    return category_obj


async def delete_category(db: _orm.Session, cat_id: int):
    category = db.query(_models.Category).filter(
        _models.Category.id == cat_id).first()

    db.delete(category)
    db.commit()
