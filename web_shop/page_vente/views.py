from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import ProductFilterForm


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
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if search:
            all_products = all_products.filter(nom__icontains=search)
        if category:
            all_products = all_products.filter(categorie__icontains=category)
        if min_price is not None:
            all_products = all_products.filter(prix__gte=min_price)
        if max_price is not None:
            all_products = all_products.filter(prix__lte=max_price)
    
    

    return render(request, 'page_vente/tous_les_produits.html', {'all_products': all_products, 'form': form})

def maroquinerie(request):
    return render(request, 'page_vente/maroquinerie.html')

def creation_sur_mesure(request):
    return render(request, 'page_vente/creation_sur_mesure.html')

def autres_produits(request):
    return render(request, 'page_vente/autres_produits.html')

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

