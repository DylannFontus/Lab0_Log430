"""Commande Django pour initialiser la base de données avec les magasins, produits et stock de base."""

from django.core.management.base import BaseCommand
from ...models import Magasin, Produit, Stock


class Command(BaseCommand):
    """Commande personnalisée pour initialiser les données de base dans la base de données."""

    help = "Initialise la base de données avec les magasins, produits et le stock de base."

    def handle(self, *args, **options):
        self.stdout.write("Initialisation de la base de données avec Django ORM...")

        # Création des magasins
        if Magasin.objects.count() == 0:
            magasins = [
                Magasin(nom="Magasin un", quartier="un", type="magasin"),
                Magasin(nom="Magasin deux", quartier="deux", type="magasin"),
                Magasin(nom="Magasin trois", quartier="trois", type="magasin"),
                Magasin(nom="Magasin quatre", quartier="quatre", type="magasin"),
                Magasin(nom="Magasin cinq", quartier="cinq", type="magasin"),
                Magasin(nom="Centre logistique", quartier="Centre logistique", type="logistique"),
                Magasin(nom="Maison mère", quartier="Administration", type="admin"),
            ]
            Magasin.objects.bulk_create(magasins)
            self.stdout.write(self.style.SUCCESS("Magasins de base créés."))
        else:
            self.stdout.write("Magasins déjà présents, rien à faire.")

        # Ajout des produits avec description
        if Produit.objects.count() == 0:
            produits = [
                Produit(nom="Chocolat", categorie="Snack", prix=1.00, description="Chocolat noir riche en cacao."),
                Produit(nom="Riz", categorie="Céréale", prix=8.99, description="Riz basmati parfumé et savoureux."),
                Produit(nom="Steak", categorie="Viande", prix=10.00, description="Steak de boeuf tendre et juteux."),
                Produit(nom="Jus", categorie="Boisson", prix=4.50, description="Jus d'orange frais et naturel."),
                Produit(nom="Lait", categorie="Laitier", prix=3.50, description="Lait entier de qualité supérieure."),
                Produit(nom="Pomme", categorie="Fruits", prix=0.80, description="Des pommes fraîches et croquantes."),
                Produit(nom="Tomate", categorie="Légumes", prix=1.30, description="Tomates juteuses et savoureuses."),
            ]
            Produit.objects.bulk_create(produits)
            self.stdout.write(self.style.SUCCESS("Produits de base créés avec descriptions."))
        else:
            self.stdout.write("Produits déjà présents, rien à faire.")

        # Stock initial
        if Stock.objects.count() == 0:
            centre_logistique = Magasin.objects.get(type="logistique")
            for produit in Produit.objects.all():
                Stock.objects.create(produit=produit, magasin=centre_logistique, quantite=10000)
            self.stdout.write(self.style.SUCCESS("Stock de base ajouté au centre logistique."))
        else:
            self.stdout.write("Stock déjà présent, rien à faire.")

        self.stdout.write(self.style.SUCCESS("Base de données initialisée."))