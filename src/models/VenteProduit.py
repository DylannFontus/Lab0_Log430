from sqlalchemy import Column, Integer, ForeignKey
from base import Base

class VenteProduit(Base):
    __tablename__ = "vente_produits"

    id = Column(Integer, primary_key=True)
    vente_id = Column(Integer, ForeignKey("ventes.id"))
    produit_id = Column(Integer, ForeignKey("produits.id"))
