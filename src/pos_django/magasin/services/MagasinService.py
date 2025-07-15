from django.shortcuts import get_object_or_404
from ..models import Magasin
import requests

def get_all_magasins():
    return Magasin.objects.all()

def get_only_magasins():
    try:
        response = requests.get(f"{'10.194.32.186:5000/api'}/magasins/")
        response.raise_for_status()
        all_magasins = response.json()
        return [m for m in all_magasins if m.get('type') == 'magasin']
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des magasins : {e}")
        return []

def get_magasin_by_id(magasin_id):
    return get_object_or_404(Magasin, id=magasin_id)

def get_centre_logistique():
    return Magasin.objects.get(type='logistique')