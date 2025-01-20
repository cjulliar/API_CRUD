from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# Modèle de base pour les produits
class ProductBase(SQLModel):
    """
    Modèle de base pour les produits, utilisé lors de la création ou de la mise à jour d'un produit.
    """
    Name: str = Field(..., max_length=255)  
    ProductNumber: str = Field(..., unique=True, max_length=50)  
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: Optional[float] = None
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = None
    ProductModelID: Optional[int] = None
    SellStartDate: datetime = Field(default_factory=datetime)
    SellEndDate: Optional[datetime] = None
    DiscontinuedDate: Optional[datetime] = None
    ThumbnailPhotoFileName: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime)

# Modèle pour la création et la mise à jour des produits
class ProductCreate(ProductBase):
    pass

# Modèle pour la catégorie des produits
class ProductCategory(SQLModel, table=True):
    """
    Modèle représentant une catégorie de produit dans la base de données.
    """
    __tablename__ = "ProductCategory"
    __table_args__ = {"schema": "SalesLT"}

    ProductCategoryID: int = Field(primary_key=True)
    Name: str = Field(..., max_length=255)
    ParentProductCategoryID: Optional[int] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime)

    Products: List["Product"] = Relationship(back_populates="Category", sa_relationship_kwargs={"lazy": "select"})

# Modèle pour le modèle des produits
class ProductModel(SQLModel, table=True):
    """
    Modèle représentant un modèle de produit dans la base de données.
    """
    __tablename__ = "ProductModel"
    __table_args__ = {"schema": "SalesLT"}

    ProductModelID: int = Field(primary_key=True)
    Name: str = Field(..., max_length=255)
    CatalogDescription: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime)

    Products: List["Product"] = Relationship(back_populates="Model", sa_relationship_kwargs={"lazy": "select"})

# Modèle pour les produits
class Product(ProductBase, table=True):
    """
    Modèle représentant un produit dans la base de données.
    """
    __tablename__ = "Product"
    __table_args__ = {"schema": "SalesLT"}

    ProductID: int = Field(primary_key=True)
    ProductCategoryID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductCategory.ProductCategoryID")
    ProductModelID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductModel.ProductModelID")

    Category: Optional[ProductCategory] = Relationship(back_populates="Products")
    Model: Optional[ProductModel] = Relationship(back_populates="Products")
