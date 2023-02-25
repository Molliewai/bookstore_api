import fastapi as _fastapi
import fastapi.security as _security
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from typing import Union
from Auth import AuthBearer as _auth_bearer
from Carts import schemas as _CartSchema

router = _fastapi.APIRouter(prefix="/api", tags=["User"])


@router.get("/users", response_model=list[_schemas.User])
async def get_all_users(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_users(db)



@router.post("/users")
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="The Email is already in use.")

    user = await _services.create_user(db=db, user=user)

    return await _auth_bearer.signJWT(user)


@router.post("/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Credentials")

    return await _auth_bearer.signJWT(user)


@router.post("/users/me")
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    res = {
        "user": user[0],
        "cart": user[1]
    }
    return res


@router.put("/users/{user_id}")
async def update_user(user_id: int, user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    res = await _services.update_user(user_id=user_id, user=user, db=db)

    return res
