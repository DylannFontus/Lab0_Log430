import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Récupère les variables d'environnement
DB_USER = os.getenv("DB_USER", "magasin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "verysecretpassword")
DB_NAME = os.getenv("DB_NAME", "magasin")
DB_PORT = os.getenv("DB_PORT", "3306")

# Utilise "localhost" dans GitHub Actions, sinon "db" par défaut
if os.getenv("GITHUB_ACTIONS") == "true":
    DB_HOST = "127.0.0.1"
else:
    DB_HOST = os.getenv("DB_HOST", "db")

# URL complète
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
