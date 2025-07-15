from django.test import TestCase
from unittest.mock import MagicMock, patch
import pytest
import json
from django.http import Http404
from .models import Magasin, Produit, Stock, Vente
from .services.MagasinService import get_all_magasins, get_only_magasins, get_magasin_by_id, get_centre_logistique
from .services.ProduitService import get_produits_par_magasin, rechercher_produits_par_nom_ou_id, get_tous_les_produits, mettre_a_jour_produit
from .services.StockService import get_stock_total_par_magasin, get_stock_par_magasin, get_stock_entry, get_stock_dict_for_magasin, get_stock_indexed_by_produit, get_produits_disponibles
from .services.VenteService import get_ventes_par_magasin, get_produits_les_plus_vendus, get_dashboard_stats
from django.db.models import Q
from django.contrib.auth.models import User
import base64
from django.test import Client
# Create your tests here.

@pytest.fixture
def mock_magasins(mocker):
    # Mock d’un queryset retournant une liste simple de magasins
    magasins = [
        Magasin(nom="Magasin 1", quartier="Q1", type="magasin"),
        Magasin(nom="Magasin 2", quartier="Q2", type="magasin"),
        Magasin(nom="Centre Logistique", quartier="Q3", type="logistique"),
    ]
    mock_qs = mocker.MagicMock()
    mock_qs.all.return_value = magasins
    mock_qs.filter.return_value = [m for m in magasins if m.type == "magasin"]
    mock_qs.get.return_value = magasins[2]
    return magasins, mock_qs

def test_get_all_magasins(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('magasin.models.Magasin.objects.all', return_value=magasins)

    result = get_all_magasins()
    assert result == magasins

def test_get_only_magasins(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('magasin.models.Magasin.objects.filter', return_value=mock_qs.filter(type="magasin"))

    result = get_only_magasins()
    assert all(m.type == "magasin" for m in result)

def test_get_magasin_by_id_success(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    # Mock get_object_or_404
    mocker.patch('magasin.services.MagasinService.get_object_or_404', return_value=magasins[0])

    result = get_magasin_by_id(1)
    assert result == magasins[0]

def test_get_magasin_by_id_raises_404(mocker):
    # Mock get_object_or_404 pour lever Http404
    def raise_404(*args, **kwargs):
        raise Http404()

    mocker.patch('magasin.services.MagasinService.get_object_or_404', side_effect=raise_404)

    with pytest.raises(Http404):
        get_magasin_by_id(999)

def test_get_centre_logistique(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('magasin.models.Magasin.objects.get', return_value=magasins[2])

    result = get_centre_logistique()
    assert result.type == "logistique"

def test_get_all_magasins(mocker, mock_magasins):
    magasins, mock_qs = mock_magasins
    mocker.patch('magasin.models.Magasin.objects.all', return_value=magasins)

    result = get_all_magasins()
    assert result == magasins

@pytest.fixture
def produit_mock(mocker):
    return mocker.patch('magasin.models.Produit')

@pytest.fixture
def stock_mock(mocker):
    return mocker.patch('magasin.models.Stock')

def test_get_produits_par_magasin(mocker):
    mock_stocks = [
        MagicMock(produit=MagicMock(id=1, nom="Prod1")),
        MagicMock(produit=MagicMock(id=2, nom="Prod2")),
    ]
    # Patch Stock.objects.filter().select_related() pour retourner mock_stocks
    mock_filter = mocker.patch('magasin.services.ProduitService.Stock.objects.filter')
    mock_filter.return_value.select_related.return_value = mock_stocks

    result = get_produits_par_magasin(1)

    mock_filter.assert_called_once_with(magasin_id=1)
    mock_filter.return_value.select_related.assert_called_once_with('produit')
    assert result == [stock.produit for stock in mock_stocks]

def test_rechercher_produits_par_nom_ou_id_with_id(mocker):
    mock_qs = MagicMock()
    patch_filter = mocker.patch('magasin.services.ProduitService.Produit.objects.filter', return_value=mock_qs)

    result = rechercher_produits_par_nom_ou_id("1")

    # Vérifie que filter a été appelé avec le bon Q
    patch_filter.assert_called_once_with(Q(id=1) | Q(nom__icontains="1"))
    assert result == mock_qs

def test_rechercher_produits_par_nom_ou_id_with_name(mocker):
    mock_qs = MagicMock()
    patch_filter = mocker.patch('magasin.services.ProduitService.Produit.objects.filter', return_value=mock_qs)

    result = rechercher_produits_par_nom_ou_id("sdada")

    patch_filter.assert_called_once_with(nom__icontains="sdada")
    assert result == mock_qs

def test_get_tous_les_produits(mocker):
    mock_qs = MagicMock()
    patch_all = mocker.patch('magasin.services.ProduitService.Produit.objects.all', return_value=mock_qs)

    result = get_tous_les_produits()

    patch_all.assert_called_once()
    assert result == mock_qs

def test_mettre_a_jour_produit(mocker):
    mock_produit = MagicMock()
    patch_get = mocker.patch('magasin.services.ProduitService.Produit.objects.get', return_value=mock_produit)

    mettre_a_jour_produit(produit_id=1, nom="ProduitTest", prix=1, description="Test")

    patch_get.assert_called_once_with(id=1)
    assert mock_produit.nom == "ProduitTest"
    assert mock_produit.prix == 1
    assert mock_produit.description == "Test"
    mock_produit.save.assert_called_once()

def test_get_stock_total_par_magasin(mocker):
    mock_manager = MagicMock()
    mock_values = MagicMock()
    mock_result = MagicMock()

    # On configure la chaîne d'appels : Stock.objects.values().annotate()
    mocker.patch('magasin.models.Stock.objects', mock_manager)
    mock_manager.values.return_value = mock_values
    mock_values.annotate.return_value = mock_result

    result = get_stock_total_par_magasin()

    mock_manager.values.assert_called_once_with('magasin__id', 'magasin__nom')
    mock_values.annotate.assert_called_once()
    assert result == mock_result

def test_get_stock_dict_for_magasin(mocker):
    mock_queryset = MagicMock()
    mock_stock1 = MagicMock()
    mock_stock1.produit.id = 1
    mock_stock2 = MagicMock()
    mock_stock2.produit.id = 2
    mock_stock_list = [mock_stock1, mock_stock2]

    mock_queryset.select_related.return_value = mock_stock_list

    mocker.patch('magasin.models.Stock.objects.filter', return_value=mock_queryset)

    result = get_stock_dict_for_magasin(1)

    assert result == {
        1: mock_stock1,
        2: mock_stock2,
    }
    mock_queryset.select_related.assert_called_once_with('produit')

def test_get_produits_disponibles(mocker):
    mock_queryset = MagicMock()
    
    stock1 = MagicMock()
    stock1.produit = "Produit A"
    stock2 = MagicMock()
    stock2.produit = "Produit B"
    stock_list = [stock1, stock2]

    mock_queryset.select_related.return_value = stock_list
    mocker.patch('magasin.models.Stock.objects.filter', return_value=mock_queryset)

    result = get_produits_disponibles(magasin_id=1)

    assert result == ["Produit A", "Produit B"]
    mock_queryset.select_related.assert_called_once_with('produit')

def test_get_ventes_par_magasin(mocker):
    mock_qs = MagicMock()
    mock_qs.values.return_value.annotate.return_value.order_by.return_value = "resultat"
    mocker.patch('magasin.models.Vente.objects', new=MagicMock(values=MagicMock(return_value=mock_qs.values())))
    
    result = get_ventes_par_magasin()
    assert result == "resultat"

# API Tests
class MagasinAPITests(TestCase):
    def setUp(self):
        self.username = "userasmin"
        self.password = "asmoday1"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.defaults['HTTP_AUTHORIZATION'] = self._get_basic_auth_header()

        self.magasin = Magasin.objects.create(nom="Magasin Test", type="magasin")
        self.produit = Produit.objects.create(nom="Produit Test", prix=10.0)
        self.stock = Stock.objects.create(produit=self.produit, magasin=self.magasin, quantite=100)

    def _get_basic_auth_header(self):
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"

    def test_get_magasins(self):
        response = self.client.get("/api/magasins/")
        self.assertEqual(response.status_code, 200)

    def test_magasins_unauthorized(self):
        self.client.defaults.pop("HTTP_AUTHORIZATION", None)
        response = self.client.get("/api/magasins/")
        self.assertEqual(response.status_code, 401)

    def test_liste_magasins(self):
        response = self.client.get("/api/magasins/")
        self.assertEqual(response.status_code, 200)

    def test_liste_produits(self):
        response = self.client.get("/api/produits/")
        self.assertEqual(response.status_code, 200)

    def test_liste_stocks(self):
        response = self.client.get("/api/stocks/")
        self.assertEqual(response.status_code, 200)

    def test_afficher_panier(self):
        url = f"/api/panier/{self.magasin.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_ajouter_au_panier(self):
        url = f"/panier/{self.magasin.id}/ajouter/"
        data = {"produit_id": self.produit.id, "quantite": 2}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertIn(response.status_code, [200, 201])  # dépend de ton implémentation

    def test_retirer_du_panier(self):
        # Ajouter avant de retirer (sinon panier vide)
        self.client.post(f"/panier/{self.magasin.id}/ajouter/", data=json.dumps({
            "produit_id": self.produit.id, "quantite": 1
        }), content_type="application/json")

        url = f"/api/panier/{self.magasin.id}/retirer/"
        data = {"produit_id": self.produit.id}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_finaliser_vente(self):
        # Ajouter au panier avant de finaliser
        self.client.post(f"/panier/{self.magasin.id}/ajouter/", data=json.dumps({
            "produit_id": self.produit.id, "quantite": 2
        }), content_type="application/json")

        url = f"/api/panier/{self.magasin.id}/finaliser/"
        response = self.client.post(url)
        self.assertIn(response.status_code, [200, 201])

    def test_ventes_par_magasin(self):
        url = f"/api/magasins/{self.magasin.id}/ventes/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_annuler_vente(self):
        # Créer une vente pour tester l’annulation
        self.client.post(f"/panier/{self.magasin.id}/ajouter/", data=json.dumps({
            "produit_id": self.produit.id, "quantite": 1
        }), content_type="application/json")
        self.client.post(f"/api/panier/{self.magasin.id}/finaliser/")
        vente = Vente.objects.filter(magasin=self.magasin).last()
        url = f"/api/magasins/{self.magasin.id}/ventes/{vente.id}/annuler/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)


    def test_reappro(self):
        centre_logistique = Magasin.objects.create(nom="Centre Logistique Test", type="logistique")
        magasin = Magasin.objects.create(nom="Magasin Test", type="magasin")

        produit = Produit.objects.create(nom="Produit Test", prix=10.0)

        Stock.objects.create(magasin=centre_logistique, produit=produit, quantite=100)

        data = {
            'produit_id': produit.id,
            'quantite': 10,
            'destination_magasin_id': magasin.id,
        }

        url = f"/api/magasins/{magasin.id}/reapprovisionner/"

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [200, 201])
        self.assertIn("success", response.json())

    def test_rapport_ventes(self):
        # Création d’un magasin de type admin (maison mère)
        magasin_admin = Magasin.objects.create(nom="Maison Mère Admin", type="admin")

        url = f"/api/maison_mere/{magasin_admin.id}/rapport_ventes/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("ventes_par_magasin", data)
        self.assertIn("produits_plus_vendus", data)
        self.assertIn("stocks_restant", data)

    def test_tableau(self):
        self.magasin.type = "maison_mere"
        self.magasin.save()
        url = f"/api/maison_mere/{self.magasin.id}/tableau_de_bord/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_donnees_appro(self):
        # Création de la maison mère
        maison_mere = Magasin.objects.create(nom="Maison Mère Test", type="maison_mere")

        # Création du centre logistique
        centre_logistique = Magasin.objects.create(nom="Centre Logistique Test", type="centre_logistique")

        # Mock des fonctions de stock_service pour éviter dépendances sur la DB et logique métier
        with patch('magasin.services.StockService.get_produits_disponibles') as mock_get_produits, \
            patch('magasin.services.StockService.get_stock_dict_for_magasin') as mock_get_stock_dict:

            mock_get_produits.return_value = []  # ou liste d’objets Produit simulés
            mock_get_stock_dict.return_value = {}

            url = f"/api/maison_mere/{maison_mere.id}/donnees_approvisionnement/"

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['centre_id'], centre_logistique.id)
            self.assertIn('magasins', data)
            self.assertIn('produits', data)
            self.assertIn('stocks', data)

    def test_approvisionner(self):
        centre = Magasin.objects.create(nom="Centre", type="centre_logistique")
        destination = Magasin.objects.create(nom="Magasin C", type="magasin")
        produit = Produit.objects.create(nom="Produit D", prix=12.5)
        Stock.objects.create(magasin=centre, produit=produit, quantite=20)

        url = f"/api/maison_mere/{centre.id}/approvisionner/"
        data = {
            "destination_magasin_id": destination.id,
            f"quantite_{produit.id}": 5
        }

        response = self.client.post(url, data)
        self.assertIn(response.status_code, [200, 201])
        self.assertIn("message", response.json())