from repositories.ProduitRepository import afficher_produits, rechercher_produit
from repositories.VenteRepository import faire_vente, annuler_vente

class Magasin:
    def AfficherProduit():
        afficher_produits()
        input("\nAppuyez sur Entrée pour revenir au menu...")

    def RechercheProduit():
        rechercher_produit()
        input("\nAppuyez sur Entrée pour revenir au menu...")

    def FaireVente():
        faire_vente()
        input("\nAppuyez sur Entrée pour revenir au menu...")

    def AnnulerVente():
        annuler_vente()
        input("\nAppuyez sur Entrée pour revenir au menu...")
