from datetime import timedelta
from typing import Any

# from fastapi.security import APIKeyHeader
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

# from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# from app.src.common.utils import profiling_api
from app.src.config import settings
from app.src.db.manager import get_session
from app.src.common.security import (
    reusable_oauth2,
    verify_user_by_username,
    create_access_token,
    get_current_user,
    verify_password,
    get_password_hash,
)
from app.src.models import token, user


router = APIRouter()


@router.get("/test")
async def read_items(token: str = Depends(reusable_oauth2)):
    """
    Test the oauth 2 authentication verifying the token
    """
    return {"token": token}


@router.post("/access-token", response_model=token.Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = verify_user_by_username(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(
        minutes=settings.SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if user:
        return {
            "access_token": create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    else:
        raise HTTPException(
            status_code=404, detail="Impossible to verify the user login"
        )


@router.post("/retrieve-user-by-token", response_model=user.UserBase)
async def retrieve_user_by_token(token: str) -> Any:
    """
    Get the user information by the bearer auth token
    """
    current_user = get_current_user(token=token)
    if not current_user:
        raise HTTPException(status_code=400, detail="Token not valid or user not found")
    return current_user


@router.post("/test-token-user")
async def test_token_simple(current_user: user.UserBase = Depends(get_current_user)) -> Any:
    """
    Test access token and retrieve information about the user
    """
    if current_user:
        return {"user_id": current_user.user_id}
    else:
        return {"user_id": None}


@router.post("/standard-token")
async def standard_token_validation(
    access_token: str, session: Session = Depends(get_session)
) -> Any:
    """
    Verify if access token is the default application token
    """
    if verify_password(access_token, get_password_hash(settings.ACCESS_TOKEN)):
        return {"valid": True}
    else:
        return {"valid": False}
