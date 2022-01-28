import datetime as dt
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException

# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.src.db.manager import get_session
from app.src import models
from app.src.api import crud
from app.src.common import security, utils

router = APIRouter()

# define and inherit the base model for the CRUD operations over products
crud_base = crud.base(models.User)

# create user
# get all users
# get single user
# update user
# delete user
# make user admin


@router.get("/", response_model=List[models.UserDataModel])
async def read_users(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: models.UserBase = Depends(security.get_current_admin_user),
) -> Any:
    """
    Retrieve all users
    """
    start_time = dt.datetime.now()
    try:
        users = crud.user.get_multi(db, skip=skip, limit=limit)
        utils.profiling_api("user:get:all", start_time, "info")
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
    except Exception as e:
        utils.profiling_api("user:get:all", start_time, "error")
        raise HTTPException(
            status_code=404, detail=f"Impossible to get the list of all users: {e}"
        )
    return users


@router.get("/{user_id}", response_model=models.UserDataModel)
async def read_single_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    current_user: models.UserBase = Depends(security.get_current_user),
) -> Any:
    start_date = dt.datetime.now()
    user = crud_base.get(db, id=user_id)
    if not user:
        utils.profiling_api("user:get:single:id", start_date, "error")
        raise HTTPException(status_code=404, detail="User not found")
    utils.profiling_api("user:get:single:id", start_date, "info")
    return user


@router.get("/info/{email}", response_model=models.UserDataModel)
async def read_single_user_by_mail(
    *,
    db: Session = Depends(get_session),
    email: str,
    current_user: models.UserBase = Depends(security.get_current_user),
) -> Any:
    start_date = dt.datetime.now()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        utils.profiling_api("user:get:single:email", start_date, "error")
        raise HTTPException(status_code=404, detail="User not found")
    utils.profiling_api("user:get:single:email", start_date, "info")
    return user


@router.get("/info/{username}", response_model=models.UserDataModel)
async def read_single_user_by_username(
    *,
    db: Session = Depends(get_session),
    username: str,
    current_user: models.UserBase = Depends(security.get_current_user),
) -> Any:
    start_date = dt.datetime.now()
    user = crud.user.get_by_username(db, username=username)
    if not user:
        utils.profiling_api("user:get:single:username", start_date, "error")
        raise HTTPException(status_code=404, detail="User not found")
    utils.profiling_api("user:get:single:username", start_date, "info")
    return user


@router.post("/", response_model=models.UserDataModel)
async def create_user(
    *,
    db: Session = Depends(get_session),
    user_in: models.UserCreate,
    current_user: models.UserBase = Depends(security.get_current_admin_user),
) -> Any:
    start_date = dt.datetime.now()
    try:
        user = crud.user.create(db, obj_in=user_in)
        utils.profiling_api("user:create", start_date, "info")
        return user
    except Exception as message:
        utils.profiling_api("user:create", start_date, "error")
        raise HTTPException(
            status_code=404, detail=f"Impossible to add a new user: {message}"
        )


@router.put("/update/me", response_model=models.UserDataModel)
async def update_user_me(
    *,
    db: Session = Depends(get_session),
    user_in: models.UserUpdate,
    current_user: models.UserBase = Depends(security.get_current_user),
) -> Any:
    start_date = dt.datetime.now()
    # current_user_data = jsonable_encoder(current_user)
    # user_existing = models.UserUpdate(**current_user_data)
    # user_data = user_in.dict(exclude_unset=True)
    # for key, value in user_data.items():
    #     setattr(current_user_data, key, value)
    try:
        user = crud_base.update(db, db_obj=current_user, obj_in=user_in)

        utils.profiling_api("user:update", start_date, "info")
        if not user:
            utils.profiling_api("user:update", start_date, "error")
            raise HTTPException(
                status_code=404,
                detail="Impossible to update the user",
            )
    except Exception as message:
        utils.profiling_api("user:update", start_date, "error")
        raise HTTPException(
            status_code=400,
            detail=f"Impossible to update the user: {message}",
        )
