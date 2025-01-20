from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from ..models import Product, ProductCreate
from ..database import get_session


router = APIRouter()

# Endpoint: Lister tous les produits
@router.get("/products", response_model=List[Product], summary="Lister tous les produits")
def get_products(session: Session = Depends(get_session)):
    try:
        # Récupérer tous les produits depuis la base de données
        statement = select(Product)
        products = session.exec(statement).all()

        # Vérification si des produits sont trouvés
        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucun produit trouvé"
            )
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des produits : {str(e)}"
        )

# Endpoint: Détails d'un produit
@router.get("/products/{product_id}", response_model=Product, summary="Détails d'un produit")
def get_product(product_id: int, session: Session = Depends(get_session)):
    try:
        # Récupérer un produit par ID
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du produit : {str(e)}"
        )

# Endpoint: Créer un produit
@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED, summary="Créer un produit")
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    try:
        new_product = Product.from_orm(product)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)  # Recharger pour récupérer les données générées
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du produit : {str(e)}"
        )

# Endpoint: Mettre à jour un produit
@router.put("/products/{product_id}", response_model=Product, summary="Mettre à jour un produit")
def update_product(product_id: int, product: ProductCreate, session: Session = Depends(get_session)):
    try:
        existing_product = session.get(Product, product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        # Mettre à jour les champs
        for key, value in product.dict(exclude_unset=True).items():
            setattr(existing_product, key, value)
        session.add(existing_product)
        session.commit()
        session.refresh(existing_product)
        return existing_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du produit : {str(e)}"
        )

# Endpoint: Supprimer un produit
@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un produit")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    try:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        session.delete(product)
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression du produit : {str(e)}"
        )

# Endpoint: Tester la connexion à la base de données
@router.get("/test-db", summary="Tester la connexion à la base de données")
def test_db_connection(session: Session = Depends(get_session)):
    try:
        session.execute("SELECT 1")
        return {"message": "Connexion à la base de données réussie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de connexion à la base de données : {str(e)}"
        )
