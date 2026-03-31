from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from fastapi import status, Depends, HTTPException, Path, APIRouter

try:
    from ..models import Todos
    from ..database import SessionLocal
except ImportError:  # pragma: no cover
    from models import Todos
    from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0,lt=6)
    completed: bool

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependencies):
    return db.query(Todos).all()

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependencies, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Not found")

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependencies, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependencies, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependencies, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    db.refresh(todo_model)
    return {}
