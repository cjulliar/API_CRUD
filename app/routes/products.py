from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from ..models import Product, ProductCreate
from ..database import get_session
from ..auth import get_current_user, User
from datetime import datetime

router = APIRouter()

# Fonction de validation des dates
def validate_date_fields(product: ProductCreate):
    """Valide les champs datetime dans le produit."""
    for date_field in ["SellStartDate", "SellEndDate", "DiscontinuedDate", "ModifiedDate"]:
        date_value = getattr(product, date_field, None)
        if date_value is not None:
            try:
                datetime.fromisoformat(str(date_value))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Champ de date invalide : {date_field} doit être au format ISO 8601. Valeur fournie : {date_value}"
                )

# Endpoint: Lister tous les produits
@router.get("/", response_model=List[Product], summary="Lister tous les produits")
async def get_products(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Récupère tous les produits."""
    try:
        statement = select(Product)
        products = session.exec(statement).all()
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

# Endpoint: Détails d’un produit
@router.get("/{product_id}", response_model=Product, summary="Détails d’un produit")
async def get_product(
    product_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Retourne les détails d’un produit spécifique."""
    try:
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
async def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    try:
        # Vérification si ProductID est fourni
        if product.ProductID is not None:
            existing_product = session.get(Product, product.ProductID)
            if existing_product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ProductID déjà existant."
                )

        # Création du produit
        new_product = Product.from_orm(product)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du produit : {str(e)}"
        )


# Endpoint: Modifier un produit
@router.put("/{product_id}", response_model=Product, summary="Mettre à jour un produit")
async def update_product(
    product_id: int,
    product: ProductCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Met à jour les informations d’un produit existant."""
    try:
        existing_product = session.get(Product, product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
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
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un produit")
async def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Supprime un produit spécifique."""
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
