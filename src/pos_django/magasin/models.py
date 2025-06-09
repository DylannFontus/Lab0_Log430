from django.db import models
from django.utils.timezone import now

# Create your models here.
class Magasin(models.Model):
    nom = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.nom)

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    prix = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.nom)

class Stock(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="stocks")
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="stocks")
    quantite = models.IntegerField()

    def __str__(self) -> str:
        nom_produit = getattr(self.produit, "nom", "Produit inconnu")
        nom_magasin = getattr(self.magasin, "nom", "Magasin inconnu")
        return f"{self.quantite} de {nom_produit} depuis {nom_magasin}"

class Vente(models.Model):
    date_heure = models.DateTimeField(default=now)
    total = models.FloatField()
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="ventes")

    def __str__(self) -> str:
        # Accès sécurisé à l'id, au cas où l'objet n'aurait pas d'id (ex. non sauvegardé)
        vente_id = str(self.id) if self.id is not None else "non sauvegardée"
        return f"Vente {vente_id} - {self.total}$"

class VenteProduit(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name="produits")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.FloatField()

    def __str__(self) -> str:
        # Utiliser str() pour éviter les erreurs si produit ou vente est None (ex: en cours de suppression)
        produit_nom = str(self.produit.nom) if self.produit else "Produit inconnu"
        vente_id = str(self.vente.id) if self.vente else "Vente inconnue"
        return f"{self.quantite} x {produit_nom} dans vente {vente_id}"