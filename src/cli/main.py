from db.init_db import init_db
from services.Magasin import Magasin

def afficher_menu():
    print("\n--- Menu POS ---")
    print("1. Rechercher un produit")
    print("2. Enregistrer une vente")
    print("3. Annuler une vente")
    print("4. Consulter le stock")
    print("0. Quitter")

def main():
    print("Bienvenue dans le système de point de vente (POS) !")
    print("Initialisation de la base de données...")
    init_db()

    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == "1":
            Magasin.RechercheProduit()

        elif choix == "2":
            Magasin.FaireVente()

        elif choix == "3":
            Magasin.AnnulerVente()

        elif choix == "4":
            Magasin.AfficherProduit()

        elif choix == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()