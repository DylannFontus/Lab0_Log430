from models.Produit import Produit
from models.Ventes import Vente
from models.VenteProduit import VenteProduit
from db.session import SessionLocal

def creer_vente(panier, session):
    try:
        total = sum(p.prix * q for p, q in panier)

        vente = Vente(total=total)
        session.add(vente)
        session.flush()

        for produit, quantite in panier:
            ligne = VenteProduit(
                vente_id=vente.id,
                produit_id=produit.id,
                quantite=quantite,
                prix_unitaire=produit.prix,
            )
            session.add(ligne)
            produit.quantite_stock -= quantite

        session.commit()
        return total
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def annuler_vente():
    session = SessionLocal()

    try:
        ventes = session.query(Vente).order_by(Vente.date.desc()).all()
        if not ventes:
            print("Aucune vente enregistrée.")
            return

        print("\n--- Dernières ventes ---")
        for vente in ventes:
            print(f"ID: {vente.id} | Total: {vente.total:.2f} $ | Date: {vente.date}")

        vente_id = input("ID de la vente à annuler : ").strip()
        vente = session.query(Vente).filter_by(id=int(vente_id)).first()
        if not vente:
            print("Vente introuvable.")
            return

        confirmation = input(f"Confirmer l’annulation de la vente {vente.id} (o/N) ? ").lower()
        if confirmation != 'o':
            print("Annulation confirmée.")
            return

        for ligne in vente.produits:
            produit = session.query(Produit).filter_by(id=ligne.produit_id).first()
            if produit:
                produit.quantite_stock += ligne.quantite

        session.delete(vente)
        session.commit()
        print("Vente annulée avec succès.")

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l’annulation : {e}")
    finally:
        session.close()

def faire_vente():
    session = SessionLocal()
    panier = []
    quantites_temp = {}

    try:
        while True:
            produits = session.query(Produit).all()
            print("\n--- Produits disponibles en stock ---")
            for p in produits:
                manquant = quantites_temp.get(p.id, 0)
                stock_dispo = p.quantite_stock - manquant
                print(f"{p.id}: {p.nom} - {p.prix:.2f} $ ({stock_dispo} en stock)")

            choix = input("ID du produit à ajouter (ou 'f' pour finaliser) : ").strip()
            if choix.lower() == "f":
                break

            try:
                produit_id = int(choix)
            except ValueError:
                print("Entrée invalide.")
                continue

            produit = session.query(Produit).filter_by(id=produit_id).first()
            if not produit:
                print("Produit invalide.")
                continue

            manquant = quantites_temp.get(produit.id, 0)
            stock_dispo = produit.quantite_stock - manquant

            quantite = int(input(f"Quantité de {produit.nom} : "))
            if quantite > stock_dispo:
                print("Stock insuffisant.")
                continue

            panier.append((produit, quantite))
            quantites_temp[produit.id] = manquant + quantite
            print(f"{quantite} x {produit.nom} ajouté(s) au panier.")

        if not panier:
            print("Aucun produit sélectionné.")
            return

        total = creer_vente(panier, session)
        print(f"Vente enregistrée. Total: {total:.2f} $")

    except Exception as e:
        session.rollback()
        print(f"Erreur: {e}")
    finally:
        session.close()