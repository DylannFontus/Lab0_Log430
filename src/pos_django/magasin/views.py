from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .services import ProduitService, StockService, VenteService, MagasinService
from .models import Magasin, Produit, Stock, Vente

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def page_magasins(request):
    print("page_magasins appelée")
    magasins = MagasinService.get_only_magasins()
    print(f"Magasins récupérés : {magasins}")
    return render(request, "magasins.html", {"magasins": magasins})

def page_caisse(request, magasin_id):
    magasin = MagasinService.get_magasin_by_id(magasin_id)
    action = request.GET.get("action")
    afficher_produits = action == "afficher_produits"

    stocks = StockService.get_stock_par_magasin(magasin_id) if afficher_produits else []

    context = {
        "magasin": magasin,
        "magasin_id": magasin_id,
        "afficher_produits": afficher_produits,
        "stocks": stocks,
    }

    return render(request, "caisse.html", context)


def rechercher_produit(request, magasin_id):
    query = request.GET.get("q", "").strip()
    produits_recherches = []

    if query:
        produits_recherches = ProduitService.rechercher_produits_par_nom_ou_id(query)

    return render(request, "caisse.html", {
        "magasin": MagasinService.get_magasin_by_id(magasin_id),
        "magasin_id": magasin_id,
        "produits_recherches": produits_recherches,
    })


def reapprovisionnement_view(request, magasin_id):
    magasin = MagasinService.get_magasin_by_id(magasin_id)
    centre_logistique = MagasinService.get_centre_logistique()

    stock_centre, stock_local = StockService.get_stock_indexed_by_produit(
        centre_logistique.id, magasin.id
    )

    if request.method == "POST":
        produit_id = int(request.POST["produit_id"])
        quantite = int(request.POST["quantite"])

        try:
            success, msg = StockService.transferer_stock(
                produit_id,
                quantite,
                centre_logistique.id,
                magasin.id
            )
            if success:
                messages.success(request, msg)
                return redirect("reapprovisionner", magasin_id=magasin.id)
            messages.error(request, msg)
        except ValueError as error:
            messages.error(request, str(error))

    context = {
        "magasin": magasin,
        "stock_centre": stock_centre,
        "stock_local": stock_local,
    }
    return render(request, "reapprovisionner.html", context)


def panier_view(request, magasin_id):
    magasin = get_object_or_404(Magasin, id=magasin_id)
    if "panier" not in request.session:
        request.session["panier"] = {}

    panier = request.session["panier"]
    produits = Produit.objects.filter(stock__magasin_id=magasin_id).select_related("stock")
    lignes = []

    for produit in produits:
        pid_str = str(produit.id)
        if pid_str in panier:
            lignes.append({
                "produit": produit,
                "quantite": panier[pid_str],
            })

    context = {
        "magasin": magasin,
        "produits": produits,
        "lignes": lignes,
    }
    return render(request, "panier.html", context)

def liste_ventes(request, magasin_id):
    ventes = Vente.objects.filter(magasin_id=magasin_id).order_by('-date_heure')
    return render(request, 'vente.html', {'ventes': ventes, 'magasin_id': magasin_id})


def annuler_vente(request, magasin_id, vente_id):
    if request.method == "POST":
        VenteService.annuler_vente(magasin_id, vente_id)
    return redirect('liste_ventes', magasin_id=magasin_id)

def ajouter_au_panier(request, magasin_id):
    if request.method == "POST":
        produit_id = int(request.POST["produit_id"])
        quantite = int(request.POST["quantite"])

        panier = request.session.get("panier", {})
        quantite_actuelle = panier.get(str(produit_id), 0)
        nouvelle_quantite = quantite_actuelle + quantite

        stock_dispo = StockService.get_stock_entry(magasin_id, produit_id)
        if not stock_dispo or stock_dispo.quantite < nouvelle_quantite:
            messages.error(request, "Stock insuffisant.")
            return redirect("panier", magasin_id=magasin_id)

        panier[str(produit_id)] = nouvelle_quantite
        request.session["panier"] = panier
        messages.success(request, "Produit ajouté au panier.")

    return redirect("panier", magasin_id=magasin_id)


def retirer_du_panier(request, magasin_id, produit_id):
    panier = request.session.get("panier", {})
    if str(produit_id) in panier:
        del panier[str(produit_id)]
        request.session["panier"] = panier
        messages.success(request, "Produit retiré du panier.")
    else:
        messages.warning(request, "Produit non trouvé dans le panier.")
    return redirect("panier", magasin_id=magasin_id)


def afficher_panier(request, magasin_id):
    panier = request.session.get("panier", {})
    produits = Produit.objects.filter(id__in=panier.keys())
    details = []

    for produit in produits:
        quantite = panier[str(produit.id)]
        stock = StockService.get_stock_entry(magasin_id, produit.id)
        details.append({
            "produit": produit,
            "quantite": quantite,
            "stock_dispo": stock.quantite if stock else 0,
            "total": quantite * produit.prix,
        })

    total_panier = sum(item["total"] for item in details)

    magasin = Magasin.objects.get(id=magasin_id)
    produits_disponibles = StockService.get_produits_disponibles(
        magasin_id
    )

    return render(request, "panier.html", {
        "details": details,
        "total_panier": total_panier,
        "magasin": magasin,
        "magasin_id": magasin_id,
        "produits_disponibles": produits_disponibles,
    })


def finaliser_vente(request, magasin_id):
    panier = request.session.get("panier", {})
    if not panier:
        messages.warning(request, "Le panier est vide.")
        return redirect("panier", magasin_id=magasin_id)

    try:
        VenteService.creer_vente(panier, magasin_id)
        request.session["panier"] = {}
        messages.success(request, "Vente enregistrée avec succès.")
    except Exception as e:
        # Exception générique pour capturer toute erreur inattendue
        messages.error(request, f"Erreur lors de la vente : {e}")

    return redirect("liste_ventes", magasin_id=magasin_id)

def admin_page(request):
    magasins = MagasinService.get_all_magasins()
    entites_admin = [m for m in magasins if m.type != 'magasin']
    return render(request, 'gestion.html', {'entites_admin': entites_admin})


def admin_entite(request, magasin_id):
    magasin = MagasinService.get_magasin_by_id(magasin_id)
    if magasin.type == 'admin':
        return render(request, 'maison_mere.html', {'magasin': magasin})
    return render(request, 'centre_logistique.html', {'magasin': magasin})


def rapport_ventes(request, magasin_id):
    magasin = MagasinService.get_magasin_by_id(magasin_id)
    ventes_par_magasin = VenteService.get_ventes_par_magasin()
    produits_plus_vendus = VenteService.get_produits_les_plus_vendus()
    stocks_restant = StockService.get_stock_total_par_magasin()

    context = {
        'magasin': magasin,
        'ventes_par_magasin': ventes_par_magasin,
        'produits_plus_vendus': produits_plus_vendus,
        'stocks_restant': stocks_restant
    }
    return render(request, 'rapport_ventes.html', context)


def tableau_de_bord(request, magasin_id):
    magasin = Magasin.objects.get(id=magasin_id)
    stats = VenteService.get_dashboard_stats()
    return render(request, 'tableau_de_bord.html', {'magasin': magasin, 'stats': stats})


def modifier_produits_depuis_maison_mere(request, magasin_id):
    produits = ProduitService.get_tous_les_produits()
    return render(request, 'modifier_produits.html', {
        'produits': produits,
        'magasin_id': magasin_id
    })


@require_POST
def modifier_produit(request, produit_id):
    nom = request.POST.get("nom")
    prix = float(request.POST.get("prix"))
    description = request.POST.get("description")
    ProduitService.mettre_a_jour_produit(produit_id, nom, prix, description)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def approvisionner_magasin(request, centre_logistique_id):
    centre = Magasin.objects.get(id=centre_logistique_id)
    magasins = Magasin.objects.exclude(id=centre_logistique_id)
    produits = Produit.objects.all()
    stock_centre_dict = StockService.get_stock_dict_for_magasin(centre_logistique_id)

    if request.method == "POST":
        destination_id = int(request.POST.get("destination_magasin_id"))
        messages_list = []
        for produit in produits:
            qte_str = request.POST.get(f"quantite_{produit.id}")
            if qte_str:
                quantite = int(qte_str)
                if quantite > 0:
                    try:
                        StockService.transferer_stock(
                            produit.id, quantite, centre_logistique_id, destination_id
                        )
                        messages_list.append(f"{quantite}x {produit.nom} transféré.")
                    except ValueError as e:
                        messages_list.append(f"{produit.nom} : {str(e)}")

        request.session['messages'] = messages_list
        return redirect('approvisionner_magasin', centre_logistique_id=centre_logistique_id)

    return render(request, 'approvisionnement.html', {
        'centre_logistique': centre,
        'magasins': magasins,
        'produits': produits,
        'stock_centre_dict': stock_centre_dict,
    })
