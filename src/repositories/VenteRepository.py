from models.Ventes import Vente
from models.VenteProduit import VenteProduit
from sqlalchemy.orm import Session

class VenteRepository:
    def __init__(self, db: Session):
        self.db = db

    def creer_vente(self, produits, total):
        vente = Vente(total=total)
        self.db.add(vente)
        self.db.flush()  # pour obtenir l'ID

        for produit in produits:
            vp = VenteProduit(vente_id=vente.id, produit_id=produit.id)
            self.db.add(vp)

        return vente

    def supprimer_vente(self, vente_id):
        self.db.query(VenteProduit).filter(VenteProduit.vente_id == vente_id).delete()
        self.db.query(Vente).filter(Vente.id == vente_id).delete()
