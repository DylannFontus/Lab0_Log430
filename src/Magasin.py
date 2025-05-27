from Produit import Produit
from Ventes import Vente

class Magasin:
    def __init__(self):
        self.stocks = []  # Liste de produits en stock
        self.ventes = []  # Historique des ventes

    def ajouter_produit_stock(self, produit):
        self.stocks.append(produit)

    def rechercher_produit(self, valeur, critere="nom"):
        resultats = []
        for produit in self.stocks:
            if critere == "nom" and produit.get_nom() == valeur:
                resultats.append(produit)
            elif critere == "identifiant" and produit.get_identifiant() == valeur:
                resultats.append(produit)
            elif critere == "categorie" and produit.get_categorie() == valeur:
                resultats.append(produit)
        return resultats

    def enregistrer_vente(self, produits_a_vendre):
        vente = Vente()
        for produit in produits_a_vendre:
            vente.ajouter_produit(produit, produit.get_prix())
            if produit in self.stocks:
                self.stocks.remove(produit)
        self.ventes.append(vente)
        return vente

    def gerer_retour(self, vente):
        for produit, _ in vente.produits:
            self.stocks.append(produit)
        vente.vider_vente()

    def consulter_stocks(self):
        return len(self.stocks)