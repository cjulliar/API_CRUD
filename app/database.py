from sqlmodel import create_engine, Session
from app.config import settings
import logging

# Crée l'engine de connexion
engine = create_engine(
    settings.database_url,
    echo=True  # Active les logs SQL
)

# Configure le logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_session():
    """Gère la création et la fermeture de session."""
    with Session(engine) as session:
        yield session

# Vérification de la connexion à la base
def check_database_connection():
    """Teste la connexion à la base."""
    try:
        with Session(engine) as session:
            session.execute("SELECT 1")
            logger.info("Connexion à la base de données réussie.")
    except Exception as e:
        logger.error(f"Erreur de connexion : {str(e)}")
        raise ValueError("Échec de la connexion à la base.")
