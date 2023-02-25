import fastapi as _fastapi
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from dependencies import get_db

router = _fastapi.APIRouter(prefix="/api/feedbacks", tags=["Feedbacks"])


@router.post("/", response_model=_schemas.Feedback)
async def create_feedback(feedback: _schemas.FeedbackCreate, user_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    feedback_obj = await _services.create_feedback(feedback=feedback, user_id=user_id, db=db)
    
    return feedback_obj


@router.get("/", response_model=list[_schemas.Feedback])
async def get_feedbacks(db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_feedbacks(db=db)


@router.get("/{feedback_id}", response_model=_schemas.Feedback)
async def get_feedback(feedback_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_feedback(feedback_id=feedback_id, db=db)


@router.delete("/{feedback_id}", status_code=200)
async def delete_feedback(feedback_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.delete_feedback(feedback_id=feedback_id, db=db)
    
    return {"message": "Feedback Successfully Deleted."}