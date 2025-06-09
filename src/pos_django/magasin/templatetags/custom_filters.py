"""
Filtres personnalisés pour les templates Django de l'application caisse.
"""

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
