from django.urls import path
from .views import page_caisse, page_magasins, home_view, reapprovisionnement_view, liste_ventes, rechercher_produit, afficher_panier, ajouter_au_panier, retirer_du_panier, finaliser_vente, annuler_vente, admin_page, admin_entite, rapport_ventes, tableau_de_bord, modifier_produits_depuis_maison_mere, modifier_produit, approvisionner_magasin

urlpatterns = [
    path('', home_view, name='home'),
    path('magasins/', page_magasins, name='magasins'),
    path('caisse/<int:magasin_id>/', page_caisse, name='page_caisse'),
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

    path("magasin/<int:magasin_id>/panier/", 
         afficher_panier, 
         name="panier"),
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

    path("gestion/", admin_page, name="admin_page"),
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
    path(
        'centre/<int:centre_logistique_id>/approvisionner/',
        approvisionner_magasin,
        name='approvisionner_magasin'
    ),
]