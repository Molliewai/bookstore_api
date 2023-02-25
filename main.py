import Users
import Books
import Categories
import Feedbacks
import Carts
from Users import main, models
from Books import main, models
from Categories import main, models
from Feedbacks import main, models
from Carts import main, models

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from Database.database import engine

import fastapi as _fastapi

Users.models.Base.metadata.create_all(bind=engine)
Books.models.Base.metadata.create_all(bind=engine)
Feedbacks.models.Base.metadata.create_all(bind=engine)
Carts.models.Base.metadata.create_all(bind=engine)

app = _fastapi.FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to BookStore"}


# _services.create_database()
app.include_router(Users.main.router)
app.include_router(Books.main.router)
app.include_router(Categories.main.router)
app.include_router(Feedbacks.main.router)
app.include_router(Carts.main.router)