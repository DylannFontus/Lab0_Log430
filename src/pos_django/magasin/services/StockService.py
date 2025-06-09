from django.db import transaction
from django.db.models import Sum
from ..models import Stock

def get_stock_total_par_magasin():
    stocks = (
        Stock.objects
        .values('magasin__id', 'magasin__nom')
        .annotate(stock_total=Sum('quantite'))
    )
    return stocks

def get_stock_par_magasin(magasin_id):
    return Stock.objects.filter(magasin_id=magasin_id).select_related('produit')

def get_stock_entry(magasin_id, produit_id):
    return Stock.objects.filter(magasin_id=magasin_id, produit_id=produit_id).first()

def get_stock_dict_for_magasin(magasin_id):
    stock_list = Stock.objects.filter(magasin_id=magasin_id).select_related('produit')
    return {stock.produit.id: stock for stock in stock_list}

def get_stock_indexed_by_produit(centre_id, magasin_id):
    stock_centre = get_stock_dict_for_magasin(centre_id)
    stock_local = get_stock_dict_for_magasin(magasin_id)
    return stock_centre, stock_local

def get_produits_disponibles(magasin_id):
    stock_entries = Stock.objects.filter(magasin_id=magasin_id, quantite__gt=0).select_related('produit')
    return [entry.produit for entry in stock_entries]

@transaction.atomic
def transferer_stock(produit_id, quantite, source_magasin_id, destination_magasin_id):
    source_stock = Stock.objects.select_for_update().filter(
        magasin_id=source_magasin_id, produit_id=produit_id
    ).first()

    if not source_stock or source_stock.quantite < quantite:
        raise ValueError("Stock insuffisant au centre logistique.")

    dest_stock, _ = Stock.objects.select_for_update().get_or_create(
        magasin_id=destination_magasin_id, produit_id=produit_id,
        defaults={'quantite': 0}
    )

    source_stock.quantite -= quantite
    dest_stock.quantite += quantite

    source_stock.save()
    dest_stock.save()

    return True, "Transfert effectué avec succès."