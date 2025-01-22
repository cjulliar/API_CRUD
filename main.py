from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import fake_users_db, verify_password, get_user
from app.routes.products import router as products_router

#uvicorn main:app --reload     pour lancer le programme

app = FastAPI()

# Inclure les routes pour les produits
app.include_router(products_router, prefix="/products", tags=["Products"])

@app.post("/token", summary="Obtenir un token d'accès")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie l'utilisateur et génère un token d'accès.
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": form_data.username, "token_type": "bearer"}
