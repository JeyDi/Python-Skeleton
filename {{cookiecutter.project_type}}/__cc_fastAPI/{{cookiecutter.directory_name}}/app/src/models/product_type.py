"""
Product Type model for api and database.
Define the tipology of a single product.
Can be single product type for different products.
"""

from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.src.db.base import Base


# SQLAlchemy table definition (schema)
# 1 product type has many products (1 to many)
class ProductType(Base):
    __tablename__ = "product_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # create the relationship with product
    product = relationship("Product", back_populates="product_type")


# Pydantic validation table definition (model for api and functions)
class ProductTypeBase(BaseModel):
    name: str
    description: Optional[str]
    # products: Optional["ProductBase"] = None


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeRead(ProductTypeBase):
    id: int
    name: str
    description: Optional[str]


# In the update all the objects need to be optional
class ProductTypeUpdate(ProductTypeBase):
    name: Optional[str] = None
    description: Optional[str] = None


class ProductTypeDelete(ProductTypeBase):
    id: int


class ProductTypeInDBBase(ProductTypeBase):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


# pydantic model used to return info from db (for example post calls)
class ProductTypeDataModel(ProductTypeInDBBase):
    pass
