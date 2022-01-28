"""
Product model for api and database
"""

from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type
from sqlalchemy.sql.sqltypes import JSON


from app.src.db.base import Base


# from app.src.models.link import ProductTagLink
# from app.src.models.product_type import ProductTypeRead
# from app.src.models.product_type import ProductType

# from app.src.models.tag import Tag, TagRead

# from app.src.models.tag import Tag


# Database table
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    available = Column(Boolean, nullable=False)
    data_field = Column(mutable_json_type(dbtype=JSON, nested=True), nullable=True)
    # 1 product type to many products
    # define the foreign key
    product_type_id = Column(
        Integer,
        ForeignKey("product_type.id", ondelete="CASCADE"),
        nullable=True,
    )
    # create the relationship with product type
    product_type = relationship("ProductType", back_populates="product")

    # many to many relationship (many products with many tags)
    # tags: List[Tag] = relationship("tag", back_populates="products")

    # 1 to 1 relationship


# Pydantic api models
class ProductBase(BaseModel):
    name: str = None
    description: Optional[str] = None
    price: float = 0.0
    available: bool = False
    data_field: Optional[dict] = None
    product_type_id: Optional[int] = None


class ProductRead(ProductBase):
    id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
    data_field: Optional[dict] = None


class ProductDelete(ProductBase):
    id: int


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: int
    name: str
    description: Optional[str]
    price: float
    available: bool
    data_field: Optional[dict]

    class Config:
        orm_mode = True


# Properties properties stored in DB
# # pydantic model used to return info from db (for example post calls)
class ProductDataModel(ProductInDBBase):
    pass


# class ProductReadwithTypeAndTags(ProductBase):
#     product_type: Optional[ProductTypeRead] = None
#     tags: List[TagRead] = []
