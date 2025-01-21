from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext

# Initialisation du contexte pour les mots de passe hashés
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modèle de données pour les utilisateurs
class User(BaseModel):
    username: str
    is_admin: bool = False

# Simuler une base de données d'utilisateurs
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrator",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("admin"),  # Hash du mot de passe "admin"
        "disabled": False,
    }
}

# Vérifier le mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Récupérer un utilisateur
def get_user(db, username: str) -> Optional[User]:
    user_dict = db.get(username)
    if user_dict:
        return User(**user_dict)
    return None

# Dépendance pour vérifier l'authentification
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = get_user(fake_users_db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
