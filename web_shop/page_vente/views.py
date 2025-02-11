from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import ProductFilterForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect


@require_POST
@csrf_protect
def rendre_indisponible(request, product_id):
    try:
        product = AllProducts.objects.get(id=product_id)
        product.disponible = False
        product.save()
        return JsonResponse({'status': 'success'})
    except AllProducts.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
# Create your views here.
def index(request):    
    return render(request, 'page_vente/index.html')


    """macrames_objects = Macrame.objects.all()
    macrames_disponible = [macrame.nom for macrame in macrames_objects if macrame.disponible == True]
    maroquinerie_objects = Maroquinerie.objects.all()
    maroquinerie_disponible = [maroquinerie.nom for maroquinerie in maroquinerie_objects if maroquinerie.disponible == True]
    together_objects = Together.objects.all()
    together_disponible = [together.nom for together in together_objects if together.disponible == True]
    liste_objects_disponible = []
    if macrames_disponible:
        liste_objects_disponible.append("Marcramés disponible")
    else:
        liste_objects_disponible.append("Macramés indisponible")
    if maroquinerie_disponible:
        liste_objects_disponible.append("Maroquinerie disponible")
    else:
        liste_objects_disponible.append("Maroquinerie indisponible")
    if together_disponible:
        liste_objects_disponible.append("Together disponible")
    else:
        liste_objects_disponible.append("Together indisponible")
    return HttpResponse("Liste Objects disponible: " + str(liste_objects_disponible))"""


def macrames(request):
    return render(request, 'page_vente/macrames.html')

def tous_les_produits(request):
    all_products = AllProducts.objects.all()
    form = ProductFilterForm(request.GET)

    all_products = [product for product in all_products if product.disponible]

    if form.is_valid():
        search = form.cleaned_data.get('search')
        type = form.cleaned_data.get('type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if search:
            all_products = [product for product in all_products if search.lower() in product.nom.lower()]
        if type:
            if type == '---':
                type = None
            else:
                all_products = [product for product in all_products if product.type == type]
        if min_price is not None:
            all_products = [product for product in all_products if product.prix >= min_price]
        if max_price is not None:
            all_products = [product for product in all_products if product.prix <= max_price]

    # Pagination
    paginator = Paginator(all_products, 20)  # 20 articles per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'form': form
    }

    return render(request, 'page_vente/tous_les_produits.html', context)

def maroquinerie(request):
    return render(request, 'page_vente/maroquinerie.html')

def creation_sur_mesure(request):
    return render(request, 'page_vente/creation_sur_mesure.html')

def hybride(request):
    return render(request, 'page_vente/hybride.html')

def contact(request):
    return render(request, 'page_vente/contact.html')

def panier(request):
    return render(request, 'page_vente/panier.html')

def a_propos(request):
    return render(request, 'page_vente/a_propos.html')


    """
    macrames_objects = Macrame.objects.all()

    # Collier
    macrames_colliers_names = [macrame.nom for macrame in macrames_objects if macrame.type == "Collier" and
                               macrame.disponible == True]
    macrames_colliers_names_str = ""
    if macrames_colliers_names:
        if len(macrames_colliers_names) > 1:
            macrames_colliers_names_str = ", ".join(macrames_colliers_names)
        else:
            macrames_colliers_names_str = macrames_colliers_names[0]

    # Bracelet
    macrames_bracelet_names = [macrame.nom for macrame in macrames_objects if macrame.type == "Bracelet" and
                               macrame.disponible == True]
    macrames_bracelets_names_str = ""
    if macrames_bracelet_names:
        if len(macrames_bracelet_names) > 1:
            macrames_bracelets_names_str = ", ".join(macrames_bracelet_names)
        else:
            macrames_bracelets_names_str = macrames_bracelet_names[0]

    # Murale
    macrames_murales_names = [macrame.nom for macrame in macrames_objects if macrame.type == "Murale" and
                              macrame.disponible == True]
    macrames_murales_names_str = ""
    if macrames_murales_names:
        if len(macrames_murales_names) > 1:
            macrames_murales_names_str = ", ".join(macrames_murales_names)
        else:
            macrames_murales_names_str = macrames_murales_names[0]

    # Boucles d'oreilles
    macrames_boucles_d_oreilles_names = [macrame.nom for macrame in macrames_objects if
                                         macrame.type == "Boucles d'oreilles" and
                                         macrame.disponible == True]
    macrames_boucles_d_oreilles_names_str = ""
    if macrames_boucles_d_oreilles_names:
        if len(macrames_boucles_d_oreilles_names) > 1:
            macrames_boucles_d_oreilles_names_str = ", ".join(macrames_boucles_d_oreilles_names)
        else:
            macrames_boucles_d_oreilles_names_str = macrames_boucles_d_oreilles_names[0]

    # Divers
    macrames_divers_names = [macrame.nom for macrame in macrames_objects if macrame.type == "Diver" and
                             macrame.disponible == True]
    macrames_divers_names_str = ""
    if macrames_divers_names:
        if len(macrames_divers_names) > 1:
            macrames_divers_names_str = ", ".join(macrames_divers_names)
        else:
            macrames_divers_names_str = macrames_divers_names[0]
    list_macrames_complette = ""
    if any([macrames_colliers_names_str,
            macrames_bracelets_names_str,
            macrames_boucles_d_oreilles_names_str,
            macrames_divers_names_str]):
        list_macrames_complette = f  Les colliers: {macrames_colliers_names_str}<br>
                                        Les bracelets: {macrames_bracelets_names_str}<br>
                                        Les murales: {macrames_murales_names_str}<br>
                                        Les boucles d'oreilles: {macrames_boucles_d_oreilles_names_str}<br>
                                        Les divers: {macrames_divers_names_str}
    else:
        list_macrames_complette = "Désolé, il n'y a pas de macrames_objects en ce moment"
    return HttpResponse("Les macramés:<br>" + list_macrames_complette)"""

