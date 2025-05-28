from db.session import SessionLocal
from services.Magasin import Magasin
from repositories.ProduitRepository import ProduitRepository

def afficher_menu():
    print("\n--- Menu POS ---")
    print("1. Rechercher un produit")
    print("2. Enregistrer une vente")
    print("3. Annuler une vente")
    print("4. Consulter le stock")
    print("0. Quitter")

def main():
    db = SessionLocal()
    vente_service = Magasin(db)
    produit_repo = ProduitRepository(db)

    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom (optionnel) : ")
            categorie = input("Catégorie (optionnel) : ")
            produits = produit_repo.search(nom, categorie)
            for p in produits:
                print(f"{p.id} - {p.nom} ({p.categorie}) - {p.prix}$ - Stock: {p.quantite_stock}")

        elif choix == "2":
            ids = input("IDs des produits séparés par virgule : ")
            try:
                vente = vente_service.effectuer_vente([int(i) for i in ids.split(",")])
                print(f"Vente #{vente.id} enregistrée.")
            except Exception as e:
                print("Erreur :", e)

        elif choix == "3":
            idv = int(input("ID de la vente à annuler : "))
            try:
                vente_service.annuler_vente(idv)
                print("Vente annulée.")
            except Exception as e:
                print("Erreur :", e)

        elif choix == "4":
            for p in produit_repo.get_all():
                print(f"{p.id} - {p.nom} - Stock: {p.quantite_stock}")

        elif choix == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()