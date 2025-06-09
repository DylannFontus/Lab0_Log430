from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    categorie = Column(String(255))
    prix = Column(Float)
    quantite_stock = Column(Integer)

