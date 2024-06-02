from fastapi import APIRouter, Depends

from api.users.dependencies import authenticate_user
from api.users.models import User
from .dependencies import get_current_auth_user_for_refresh
from .schemas import TokenResponse
from .utils import create_access_token, create_refresh_token

router = APIRouter(prefix='/api/v1/auth/jwt', tags=['jwt'])


@router.post('/login/', response_model=TokenResponse)
def login_user(user: User = Depends(authenticate_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post('/refresh/', response_model=TokenResponse, response_model_exclude_none=True)
def refresh_token(user: User = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    return TokenResponse(access_token=access_token)
