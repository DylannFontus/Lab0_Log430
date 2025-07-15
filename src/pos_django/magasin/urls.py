from django.urls import path, include, re_path
from .views import page_caisse, page_magasins, home_view, reapprovisionnement_view, liste_ventes, rechercher_produit, afficher_panier, ajouter_au_panier, retirer_du_panier, finaliser_vente, annuler_vente, admin_page, admin_entite, rapport_ventes, tableau_de_bord, modifier_produits_depuis_maison_mere, modifier_produit, approvisionner_magasin
from rest_framework.routers import DefaultRouter
from .api_views import MagasinViewSet, ProduitViewSet, StockViewSet, VenteViewSet, reapprovisionner_api, afficher_panier_api,ajouter_au_panier_api, retirer_du_panier_api, finaliser_vente_api, ventes_par_magasin_api, annuler_vente_api, rapport_ventes_api, tableau_de_bord_api, donnees_approvisionnement, approvisionner 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'magasins', MagasinViewSet, basename='magasin')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'produits', ProduitViewSet, basename='produit')

schema_view = get_schema_view(
   openapi.Info(
      title="API du magasin",
      default_version='v1',
      description="Documentation des endpoints de l'API du magasin",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API Doc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # API REST
    path('api/', include(router.urls)),
    path('api/magasins/<int:magasin_id>/reapprovisionner/', reapprovisionner_api, name='reapprovisionner_api'),
    path('api/centreLogistique/<int:magasin_id>/reapprovisionner/', reapprovisionner_api, name='reapprovisionner_api_centre'),
    path('api/panier/<int:magasin_id>/', afficher_panier_api, name='afficher_panier_api'),
    path('panier/<int:magasin_id>/ajouter/', ajouter_au_panier_api, name='ajouter_panier_api'),#ajuster pour add api/ au début, live j'en ai pas
    path('api/panier/<int:magasin_id>/retirer/', retirer_du_panier_api, name='retirer_panier_api'),
    path('api/panier/<int:magasin_id>/finaliser/', finaliser_vente_api, name='finaliser_panier_api'),
    path("panier/<int:magasin_id>/", afficher_panier, name="panier"),
    path("api/magasins/<int:magasin_id>/ventes/", ventes_par_magasin_api),
    path('api/magasins/<int:magasin_id>/ventes/<int:vente_id>/annuler/', annuler_vente_api, name='annuler_vente_api'),
    path('api/maison_mere/<int:magasin_id>/rapport_ventes/', rapport_ventes_api, name='rapport_ventes_api'),
    path('api/maison_mere/<int:magasin_id>/tableau_de_bord/', tableau_de_bord_api, name='tableau_de_bord_api'),
    path("api/maison_mere/<int:maison_mere_id>/donnees_approvisionnement/", donnees_approvisionnement, name="donnees_approvisionnement"),
    path('api/maison_mere/<int:centre_id>/approvisionner/', approvisionner, name='approvisionner'),

    path('', 
        home_view, 
        name='home'
    ),
    path('magasins/', 
        page_magasins, 
        name='magasins'
    ),
    path(
        'reapprovisionner/<int:magasin_id>/',
        reapprovisionnement_view,
        name='reapprovisionner'
    ),
    path(
        '<int:magasin_id>/recherche/',
        rechercher_produit,
        name='rechercher_produit'
    ),
    path('caisse/<int:magasin_id>/', 
        page_caisse, 
        name='page_caisse'
    ),
    path("magasin/<int:magasin_id>/panier/", 
        afficher_panier, 
        name="panier"
    ),
    path(
        '<int:magasin_id>/panier/ajouter/',
        ajouter_au_panier,
        name='ajouter_panier'
    ),
    path(
        '<int:magasin_id>/panier/retirer/<int:produit_id>/',
        retirer_du_panier,
        name='retirer_du_panier'
    ),
    path(
        '<int:magasin_id>/panier/finaliser/',
        finaliser_vente,
        name='finaliser_panier'
    ),
    path('<int:magasin_id>/ventes/', 
        liste_ventes, 
        name='liste_ventes'
    ),
    path(
        '<int:magasin_id>/ventes/<int:vente_id>/annuler/',
        annuler_vente,
        name='annuler_vente'
    ),
    path(
        'centre/<int:centre_logistique_id>/approvisionner/',
        approvisionner_magasin,
        name='approvisionner_magasin'
    ),
    path("gestion/", 
        admin_page, 
        name="admin_page"
    ),
    path(
        "gestion/<int:magasin_id>/",
        admin_entite,
        name="admin_entite"
    ),
    path(
        'gestion/<int:magasin_id>/rapport/',
        rapport_ventes,
        name='rapport_ventes'
    ),
    path(
        'gestion/<int:magasin_id>/dashboard/',
        tableau_de_bord,
        name='tableau_de_bord'
    ),
    path(
        'gestion/<int:magasin_id>/produits/',
        modifier_produits_depuis_maison_mere,
        name='modifier_produits_depuis_maison_mere'
    ),
    path(
        'gestion/produits/<int:produit_id>/modifier/',
        modifier_produit,
        name='modifier_produit'
    ),
]