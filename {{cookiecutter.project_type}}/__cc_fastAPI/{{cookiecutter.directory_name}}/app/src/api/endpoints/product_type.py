import datetime as dt
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.src.db.manager import get_session
from app.src import models
from app.src.api import crud
from app.src.common import utils

#
router = APIRouter()
# define and inherit the base model for the CRUD operations over products
ptype = crud.base(models.ProductType)


@router.get("/", response_model=List[models.ProductTypeDataModel])
async def read_product_types(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.UserBase = Depends(security.get_current_user),
    current_user=True,
) -> Any:
    """
    Retrieve all existing product types
    """
    start_time = dt.datetime.now()

    if current_user:
        product_types = ptype.get_multi(db=db, skip=skip, limit=limit)
        utils.profiling_api("product:get:all", start_time, "info")
    else:
        utils.profiling_api("product:get:all", start_time, "error")
        raise HTTPException(status_code=400, detail="User not authenticated")

    return product_types


@router.get("/{product_type_id}", response_model=models.ProductTypeDataModel)
async def read_single_product_type(
    *,
    db: Session = Depends(get_session),
    product_type_id: int,
    # current_user: models.UserBase = Depends(security.get_current_user)
) -> Any:
    """
    Return a single product type based on a specific id
    """
    start_date = dt.datetime.now()
    existing_product_type = ptype.get(db, id=product_type_id)
    if not existing_product_type:
        utils.profiling_api("product:get:single", start_date, "error")
        raise HTTPException(status_code=404, detail="Product not found")
    utils.profiling_api("product:get:single", start_date, "info")
    return existing_product_type


@router.post("/", response_model=models.ProductTypeDataModel)
async def create_product_type(
    *,
    db: Session = Depends(get_session),
    input_product: models.ProductTypeCreate = Body(
        ...,
        example={
            "name": "Panini",
            "description": "Deliziosi panini da mangiare",
        },
    ),
    # current_user: models.UserBase = Depends(security.get_current_user)
) -> Any:
    """
    Create and insert a new product type
    """
    start_date = dt.datetime.now()
    try:
        new_product_type = ptype.create(db, obj_in=input_product)
        utils.profiling_api("product:create", start_date, "info")
        return new_product_type
    except Exception as e:
        utils.profiling_api("product:create", start_date, "error")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_type_id}")
async def delete_product_type(
    *,
    db: Session = Depends(get_session),
    product_type_id: int,
    # current_user: models.UserBase = Depends(security.get_current_user)
) -> Any:
    start_date = dt.datetime.now()
    try:
        ptype.remove(db, id=product_type_id)
        utils.profiling_api("product:delete", start_date, "info")
        return {"product_type_id": product_type_id, "message": "deleted succesfully"}
    except Exception as e:
        utils.profiling_api("product:delete", start_date, "error")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_type_id}", response_model=models.ProductTypeDataModel)
async def update_product_type(
    *,
    db: Session = Depends(get_session),
    product_type_id: int,
    # current_user: models.UserBase = Depends(security.get_current_user),
    new_product_type: models.ProductTypeUpdate,
) -> Any:
    start_date = dt.datetime.now()
    try:
        updated_product_type = ptype.update(
            db, obj_in=new_product_type, id=product_type_id
        )
        utils.profiling_api("product:update", start_date, "info")
        return updated_product_type
    except Exception as e:
        utils.profiling_api("product:update", start_date, "error")
        raise HTTPException(status_code=400, detail=str(e))
