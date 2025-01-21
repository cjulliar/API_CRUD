from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# Modèle de base pour les produits
class ProductBase(SQLModel):
    ProductID: Optional[int]  # Ajouté comme optionnel
    Name: str
    ProductNumber: str
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: float
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = None
    ProductModelID: Optional[int] = None
    SellStartDate: datetime
    SellEndDate: Optional[datetime] = None
    DiscontinuedDate: Optional[datetime] = None
    ThumbnailPhotoFileName: Optional[str] = None
    rowguid: uuid.UUID
    ModifiedDate: datetime

# Modèle pour la création d'un produit (exclut ProductID)
class ProductCreate(ProductBase):
    pass

# Modèle pour les catégories des produits
class ProductCategory(SQLModel, table=True):
    __tablename__ = "ProductCategory"
    __table_args__ = {"schema": "SalesLT"}

    ProductCategoryID: int = Field(primary_key=True)
    Name: str = Field(..., max_length=255)
    ParentProductCategoryID: Optional[int] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)

    Products: List["Product"] = Relationship(back_populates="Category", sa_relationship_kwargs={"lazy": "select"})

# Modèle pour les produits
class Product(ProductBase, table=True):
    __tablename__ = "Product"
    __table_args__ = {"schema": "SalesLT"}

    ProductID: int = Field(primary_key=True)
    ProductCategoryID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductCategory.ProductCategoryID")
    ProductModelID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductModel.ProductModelID")

    Category: Optional[ProductCategory] = Relationship(back_populates="Products")
