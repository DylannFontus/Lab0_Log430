from Produit import Produit

class Vente:
    def __init__(self):
        self.produits = []
        self.prix = 0.0

    def ajouter_produit(self, produit, prix):
        Produit.produits.append((produit, prix))
        self.prix += prix

    def vider_vente(self):
        self.produits.clear()
        self.prix = 0.0

    def calculer_prix_total(self):
        return sum(prix for _, prix in self.produits)