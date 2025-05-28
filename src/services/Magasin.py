from sqlalchemy.orm import Session
from repositories.ProduitRepository import ProduitRepository
from repositories.VenteRepository import VenteRepository

class Magasin:
    def __init__(self, db: Session):
        self.db = db
        self.produits = ProduitRepository(db)
        self.ventes = VenteRepository(db)

    def effectuer_vente(self, produit_ids):
        total = 0
        produits_vendus = []

        try:
            self.db.begin()

            for pid in produit_ids:
                produit = self.produits.get_by_id(pid)
                if not produit or produit.quantite_stock < 1:
                    raise Exception(f"Produit {pid} indisponible")

                produit.quantite_stock -= 1
                total += produit.prix
                produits_vendus.append(produit)

            vente = self.ventes.creer_vente(produits_vendus, total)
            self.db.commit()
            return vente

        except Exception as e:
            self.db.rollback()
            raise e

    def annuler_vente(self, vente_id):
        try:
            self.db.begin()

            # récupérer les produits liés à la vente
            vps = self.db.query(models.vente_produit.VenteProduit).filter_by(vente_id=vente_id).all()
            for vp in vps:
                produit = self.produits.get_by_id(vp.produit_id)
                produit.quantite_stock += 1

            self.ventes.supprimer_vente(vente_id)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
