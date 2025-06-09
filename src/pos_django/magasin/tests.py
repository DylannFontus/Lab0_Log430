from django.test import TestCase
from unittest.mock import MagicMock
import pytest
from django.http import Http404
from .models import Magasin
from .services.MagasinService import get_all_magasins, get_only_magasins, get_magasin_by_id, get_centre_logistique
from .services.ProduitService import get_produits_par_magasin, rechercher_produits_par_nom_ou_id, get_tous_les_produits, mettre_a_jour_produit
from .services.StockService import get_stock_total_par_magasin, get_stock_par_magasin, get_stock_entry, get_stock_dict_for_magasin, get_stock_indexed_by_produit, get_produits_disponibles
from .services.VenteService import get_ventes_par_magasin, get_produits_les_plus_vendus, get_dashboard_stats
from django.db.models import Q
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