import fastapi as _fastapi
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import fastapi.security as _security
import jwt as _jwt
import passlib.hash as _hash
import sqlalchemy.orm as _orm
from dependencies import get_db
import json
from Database import database as _database
from . import models as _models
from . import schemas as _schemas
from Carts import models as _CartModel
from Carts import schemas as _CartSchema

from utils import oauth2schema, JWT_SECRET
from Auth import AuthBearer

# USERS

# GET USER BY ID


async def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


# GET USER BY EMAIL
async def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


# GET ALL USERS
async def get_users(db: _orm.Session):
    users = db.query(_models.User).all()
    return list(map(_schemas.User.from_orm, users))



# CREATE USER
async def create_user(db: _orm.Session, user: _schemas.UserCreate):
    
    user_obj = _models.User(username=user.username,
                            email=user.email,
                            hashed_password=_hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    cart = _CartModel.Cart(books=[], user_id=user_obj.id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    
    return user_obj


# AUTHENTICATE USER
async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


# CREATE TOKEN
async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: _orm.Session = _fastapi.Depends(get_db), token: str = _fastapi.Depends(oauth2schema)):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
        
        cart = db.query(_CartModel.Cart).filter(_CartModel.Cart.user_id == user.id).first()
            
    except:
        raise _fastapi.HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user), _CartSchema.ReadCart.from_orm(cart)


'''async def update_user(user_id: int, user: _schemas.UserCreate, db: _orm.Session):
    user_obj = db.query(_models.User).filter(
        _models.User.id == user_id).first()

    if user_obj is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="User Not Found."
        )
        
    if user.email == user_obj.email:
        user_obj.username = user.username
    else:
        user_obj.username = user.username
        user_obj.email = user.email
        
    if user.hashed_password == "":
            user_obj.hashed_password = user_obj.hashed_password
    else:
        user_obj.hashed_password = _hash.bcrypt.hash(user.hashed_password)
    
    db.commit()
    db.refresh(user_obj)

    return {"username": user_obj.username, "email": user_obj.email, "hashed_password": user_obj.hashed_password}'''

async def update_user(user_id: int, user: _schemas.UserCreate, db: _orm.Session):
    async with db:
        user_obj = db.query(_models.User).filter(
            _models.User.id == user_id).first()

        if user_obj is None:
            raise _fastapi.HTTPException(
                status_code=404, detail="User Not Found."
            )

        user_obj.username = user.username
        if user.email != user_obj.email:
            user_obj.email = user.email

        if user.hashed_password:
            user_obj.hashed_password = hash.bcrypt.hash(user.hashed_password)

        db.commit()
        db.refresh(user_obj)

        return {"username": user_obj.username, "email": user_obj.email, "hashed_password": user_obj.hashed_password}

