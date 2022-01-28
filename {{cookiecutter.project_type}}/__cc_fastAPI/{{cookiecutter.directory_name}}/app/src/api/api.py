from fastapi import APIRouter

from app.src.api.endpoints import celery, product, user, login, product_type

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    product_type.router, prefix="/product-types", tags=["product-types"]
)
api_router.include_router(product.router, prefix="/products", tags=["products"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(celery.router, prefix="/celery", tags=["celery"])
