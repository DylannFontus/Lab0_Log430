from models.Produit import Produit
from sqlalchemy.orm import Session

class ProduitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int):
        return self.db.query(Produit).filter(Produit.id == id).first()

    def search(self, nom=None, categorie=None):
        query = self.db.query(Produit)
        if nom:
            query = query.filter(Produit.nom.like(f"%{nom}%"))
        if categorie:
            query = query.filter(Produit.categorie.like(f"%{categorie}%"))
        return query.all()

    def get_all(self):
        return self.db.query(Produit).all()
    
    def ajouter_produit(self, produit: Produit):
        self.db.add(produit)
        self.db.commit()
        self.db.refresh(produit)
        return produit
    
    def update_stock(self, produit_id: int, quantite: int):
        produit = self.get_by_id(produit_id)
        if produit:
            produit.quantite_stock += quantite
            self.db.commit()
            self.db.refresh(produit)
            return produit
        return None
    
    def delete_produit(self, produit_id: int):
        produit = self.get_by_id(produit_id)
        if produit:
            self.db.delete(produit)
            self.db.commit()
            return True
        return False
