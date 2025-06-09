from db.session import SessionLocal
from models.Produit import Produit

def afficher_produits():
    session = SessionLocal()
    try:
        produits = session.query(Produit).all()
        if not produits:
            print("Aucun produit trouvé.")
            return

        print("\n--- Liste des produits en stock ---")
        for produit in produits:
            print(
                f"[{produit.id}] {produit.nom} - {produit.prix:.2f}$ "
                f"(Categorie: {produit.categorie}) "
                f"(Stock: {produit.quantite_stock})"
            )
    finally:
        session.close()

def rechercher_produit():
    session = SessionLocal()

    try:
        terme = input("Entrez l'identifiant ou le nom du produit à rechercher : ").strip()

        if terme.isdigit():
            produit = session.query(Produit).filter_by(id=int(terme)).first()
            if produit:
                print(
                    f"[{produit.id}] {produit.nom} - {produit.prix:.2f}$ "
                    f"(Categorie: {produit.categorie}) "
                    f"(Stock: {produit.quantite_stock})"
                )
            else:
                print("Aucun produit trouvé avec cet identifiant.")
        else:
            resultats = session.query(Produit).filter(Produit.nom.ilike(f"%{terme}%")).all()
            if resultats:
                print("\n--- Résultats ---")
                for p in resultats:
                    print(f"[{p.id}] {p.nom} - {p.categorie} - {p.prix:.2f}$ (Stock: {p.quantite_stock})")
            else:
                print("Aucun produit ne correspond à ce nom.")

    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
    finally:
        session.close()