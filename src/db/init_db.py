from models.base import Base
from models.Produit import Produit
from .session import SessionLocal, engine

def init_db():
    print("Création des tables…")
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        count = session.query(Produit).count()
        if count == 0:
            produits = [
                Produit(nom="Chocolat", categorie="Snack", prix=1.00, quantite_stock=25),
                Produit(nom="Chips", categorie="Snack", prix=2.50, quantite_stock=10),
                Produit(nom="Riz", categorie="Céréale", prix=8.99, quantite_stock=5),
                Produit(nom="Steak", categorie="Viande", prix=10.00, quantite_stock=7),
                Produit(nom="Jus", categorie="Boisson", prix=4.50, quantite_stock=15),
                Produit(nom="Lait", categorie="Laitier", prix=3.50, quantite_stock=20),
                Produit(nom="Pomme", categorie="Fruits", prix=0.80, quantite_stock=50),
                Produit(nom="Tomate", categorie="Légumes", prix=1.30, quantite_stock=40),
            ]
            session.add_all(produits)
            session.commit()
    except Exception as e:
        session.rollback()
        print("Erreur lors de l’ajout des produits :", e)
    finally:
        session.close()


"""
Catégories de produit possibles (nourriture) :
- "Viande" : pour les produits carnés (ex: Steak)
- "Boisson" : pour les boissons (ex: Jus, Eau)
- "Snack" : pour les encas (ex: Chips, Chocolat)
- "Céréale" : pour les produits céréaliers (ex: Riz, Pâtes)
- "Laitier" : pour les produits laitiers (ex: Fromage, Lait)
- "Fruits" : pour les fruits (ex: Pomme, Banane)
- "Légumes" : pour les légumes (ex: Carotte, Tomate)
"""