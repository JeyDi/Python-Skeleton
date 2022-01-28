import datetime as dt
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body, status, Cookie
from sqlalchemy.orm import Session

from app.src.db.manager import get_session
from app.src import models
from app.src.api import crud
from app.src.common import utils

#
router = APIRouter()
# define and inherit the base model for the CRUD operations over products
product = crud.base(models.Product)


@router.get(
    "/",
    response_model=List[models.ProductDataModel],
    status_code=status.HTTP_200_OK,
)
async def read_products(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.UserBase = Depends(security.get_current_user),
    current_user=True,
) -> Any:
    """
    Retrieve all products
    """
    start_time = dt.datetime.now()

    if current_user:
        all_products = product.get_multi(db=db, skip=skip, limit=limit)
        utils.profiling_api("product:get:all", start_time, "info")
    else:
        utils.profiling_api("product:get:all", start_time, "error")
        raise HTTPException(status_code=400, detail="User not authenticated")

    return all_products


@router.get("/{product_id}", response_model=models.ProductDataModel)
async def read_single_product(
    *,
    db: Session = Depends(get_session),
    product_id: int = Cookie(default=1),
    # current_user: models.UserBase = Depends(security.get_current_user)
) -> Any:
    start_date = dt.datetime.now()
    existing_product = product.get(db, id=product_id)
    if not existing_product:
        utils.profiling_api("product:get:single", start_date, "error")
        raise HTTPException(status_code=404, detail="Product not found")
    utils.profiling_api("product:get:single", start_date, "info")
    return existing_product


@router.post("/", response_model=models.ProductDataModel)
async def create_product(
    *,
    db: Session = Depends(get_session),
    input_product: models.ProductCreate = Body(
        ...,
        examples={
            "simple": {
                "summary": "A simple example",
                "description": "A **normal** item works correctly without product type id.",
                "value": {
                    "name": "panino",
                    "description": "panino di pane",
                    "price": 5,
                    "available": True,
                    "data_field": {"ingredients": ["pane", "salame"]},
                },
            },
            "with product type": {
                "summary": "Example with product type",
                "description": "Kebab example with product type, remember to have a product type id in the system",
                "value": {
                    "name": "kebab",
                    "description": "ottimo kebab",
                    "price": 2.5,
                    "available": True,
                    "data_field": {
                        "ingredients": ["cipolla", "carne", "pane", "salse", "verdure"]
                    },
                    "product_type_id": 0,
                },
            },
        },
    )
    # current_user: models.UserBase = Depends(security.get_current_user)
) -> Any:
    start_date = dt.datetime.now()
    try:
        new_product = product.create(db, obj_in=input_product)
        utils.profiling_api("product:create", start_date, "info")
        return new_product
    except Exception as e:
        utils.profiling_api("product:create", start_date, "error")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}")
async def delete_product(
    *,
    db: Session = Depends(get_session),
    product_id: int,
    # current_user: models.UserBase = Depends(security.get_current_user)
) -> Any:
    start_date = dt.datetime.now()
    try:
        product.remove(db, id=product_id)
        utils.profiling_api("product:delete", start_date, "info")
        return {"product_id": product_id, "message": "deleted succesfully"}
    except Exception as e:
        utils.profiling_api("product:delete", start_date, "error")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}", response_model=models.ProductDataModel)
async def update_product(
    *,
    db: Session = Depends(get_session),
    product_id: int,
    # current_user: models.UserBase = Depends(security.get_current_user),
    new_product: models.ProductUpdate,
) -> Any:
    start_date = dt.datetime.now()
    try:
        updated_product = product.update(db, obj_in=new_product, id=product_id)
        utils.profiling_api("product:update", start_date, "info")
        return updated_product
    except Exception as e:
        utils.profiling_api("product:update", start_date, "error")
        raise HTTPException(status_code=400, detail=str(e))
