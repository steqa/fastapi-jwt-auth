from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from . import services
from .schemas import UserResponse

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.get(
    '/',
    response_model=list[UserResponse],
)
def get_users(db: Session = Depends(get_db)):
    users = services.get_users(db)
    return users
