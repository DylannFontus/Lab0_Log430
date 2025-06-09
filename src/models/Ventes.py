from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Vente(Base):
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True)
    total = Column(Float)
    date = Column(DateTime, server_default=func.now())

    produits = relationship("VenteProduit", back_populates="vente", cascade="all, delete-orphan")
