"""
Default API for User CRUD operations, auth and verification of passwords
"""

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.src.common.security import get_password_hash, verify_password
from app.src.api.crud.base import CRUDBase
from app.src.models.user import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            name=obj_in.name,
            surname=obj_in.surname,
            password=get_password_hash(obj_in.password),
            token=get_password_hash(obj_in.token),
            isAdmin=obj_in.isAdmin,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def verify_token(self, db: Session, *, email: str, token: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(token, user.hashed_password):
            return None
        return user

    def is_admin(self, user: User) -> bool:
        return user.isAdmin


user = CRUDUser(User)
