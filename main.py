from fastapi import FastAPI
from app.routes.products import router as products_router

# Création de l'application FastAPI
app = FastAPI(
    title="AdventureWorks API",
    description="API RESTful pour la gestion des produits AdventureWorks",
    version="1.0.0",
)

# Enregistrement des routes
app.include_router(products_router, prefix="/api", tags=["Produits"])

# Route d'accueil
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API AdventureWorks!"}
