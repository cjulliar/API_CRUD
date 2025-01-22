from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# Base modèle des produits
class ProductBase(SQLModel):
    Name: str = Field(..., max_length=255)
    ProductNumber: str = Field(..., unique=True, max_length=50)
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: float
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductCategory.ProductCategoryID")
    ProductModelID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductModel.ProductModelID")
    SellStartDate: datetime = Field(default_factory=datetime.utcnow)
    SellEndDate: Optional[datetime] = None
    DiscontinuedDate: Optional[datetime] = None
    ThumbnailPhotoFileName: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)

# Modèle pour la création d'un produit
class ProductCreate(ProductBase):
    pass

# Modèle des catégories de produits
class ProductCategory(SQLModel, table=True):
    __tablename__ = "ProductCategory"
    __table_args__ = {"schema": "SalesLT"}

    ProductCategoryID: int = Field(primary_key=True)
    Name: str = Field(..., max_length=255)
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)

# Modèle pour les produits
class Product(ProductBase, table=True):
    __tablename__ = "Product"
    __table_args__ = {"schema": "SalesLT"}

    ProductID: int = Field(primary_key=True)

# Modèle des modèles de produits
class ProductModel(SQLModel, table=True):
    __tablename__ = "ProductModel"
    __table_args__ = {"schema": "SalesLT"}

    ProductModelID: int = Field(primary_key=True)
    Name: str = Field(..., max_length=255)
    Description: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)
