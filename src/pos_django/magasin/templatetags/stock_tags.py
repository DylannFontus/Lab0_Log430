"""
Filtres personnalisés liés à l'affichage du stock local dans les templates Django.
"""

from django import template

register = template.Library()

@register.filter
def stock_local(stock_local_dict, produit_id):
    return stock_local_dict.get(produit_id, 0)
