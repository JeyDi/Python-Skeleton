# from datetime import datetime, timedelta
# from pathlib import Path
# from typing import Any, Dict, Optional

# import emails
# from emails.template import JinjaTemplate
from jose import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from typing import Any, Optional, Union
from passlib.context import CryptContext

from app.src.db.manager import get_session
from app.src.models.user import User, UserBase, UserRead
from app.src.models.token import TokenPayload

from app.src.config import settings


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(*, password: str = Depends(reusable_oauth2)) -> UserBase:
    try:
        payload = jwt.decode(
            password,
            settings.SECURITY_SECRET_KEY,
            algorithms=[settings.SECURITY_ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_id = token_data.sub
    session = get_session()
    user = next(session).get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found or not authenticated"
        )
    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> bool:
    if not current_user.isAdmin:
        raise HTTPException(status_code=400, detail="User is not admin or don't exist")
    if current_user:
        return True
    else:
        return False


def test_user(current_user: User = Depends(get_current_user)) -> bool:
    """
    Test access token
    """
    if current_user:
        return True
    else:
        return False


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECURITY_SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_user_by_username(*, username: str, password: str) -> Optional[UserRead]:
    session = get_session()
    user = next(session).query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def verify_user_by_email(
    *, email: str, password: str, db: Session = Depends(get_session)
) -> Optional[UserRead]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


# def verify_password_reset_token(token: str) -> Optional[str]:
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return decoded_token["email"]
#     except jwt.JWTError:
#         return None


# possibility to check if an user is active or not
# def get_current_active_user(
#     current_user: ShinyUser = Depends(get_current_user),
# ) -> ShinyUser:
#     if not current_user.isActive:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
