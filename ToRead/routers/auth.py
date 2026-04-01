from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

try:
    from ..database import SessionLocal
    from ..models import User
except ImportError:  # pragma: no cover
    from database import SessionLocal
    from models import User

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(get_db)]

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependencies,create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active = True
    )
    db.add(create_user_model)
    db.commit()
