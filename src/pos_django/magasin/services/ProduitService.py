from django.db.models import Q
from ..models import Stock, Produit

def get_produits_par_magasin(magasin_id):
    stocks = Stock.objects.filter(magasin_id=magasin_id).select_related('produit')
    return [stock.produit for stock in stocks]

def rechercher_produits_par_nom_ou_id(query):
    if query.isdigit():
        return Produit.objects.filter(Q(id=int(query)) | Q(nom__icontains=query))
    return Produit.objects.filter(nom__icontains=query)

def get_tous_les_produits():
    return Produit.objects.all()

def mettre_a_jour_produit(produit_id: int, nom: str, prix: float, description: str):
    produit = Produit.objects.get(id=produit_id)
    produit.nom = nom
    produit.prix = prix
    produit.description = description
    produit.save()
    return produit