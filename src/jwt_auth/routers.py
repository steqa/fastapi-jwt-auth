from fastapi import APIRouter, Depends

from src.users.dependencies import authenticate_user
from .schemas import TokenResponse
from .utils import create_access_token, create_refresh_token
from src.users.models import User

router = APIRouter(prefix='/api/v1/auth/jwt', tags=['jwt'])


@router.post('/login/', response_model=TokenResponse)
def login_user(user: User = Depends(authenticate_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
