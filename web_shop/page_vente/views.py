from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import ProductFilterForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect

def add_to_cart(request, product_id):
    product = get_object_or_404(AllProducts, id=product_id)

    if not product.disponible:
        return JsonResponse({'success': False, 'message': 'Produit déjà pris'}, status=400)

    # Récupérer l'ID de session unique de Django
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Vérifier si un panier existe pour cette session
    cart, created = Cart.objects.get_or_create(session_id=session_id)

    # Ajouter le produit au panier
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    # Marquer le produit comme indisponible
    product.disponible = False
    product.save()

    return JsonResponse({'success': True, 'message': f'{product.nom} ajouté au panier'})

def cart_detail(request):
    session_id = request.session.session_key
    if not session_id:
        return JsonResponse({'cart': []})  # Aucun panier trouvé

    cart = Cart.objects.filter(session_id=session_id).first()
    if not cart:
        return JsonResponse({'cart': []})  

    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    data = [{'nom': item.product.nom, 'prix': item.product.prix, 'quantity': item.quantity, 'lien_image1': item.product.lien_image1} for item in cart_items]

    return JsonResponse({'cart': data})

# Vider le panier et rendre les produits à nouveau disponibles
def vider_panier(request):
    session_id = request.session.session_key
    if not session_id:
        return JsonResponse({'success': False, 'message': 'Aucun panier trouvé'})

    cart = Cart.objects.filter(session_id=session_id).first()
    if not cart:
        return JsonResponse({'success': False, 'message': 'Le panier est déjà vide'})

    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.product.disponible = True  # Rendre le produit disponible
        item.product.save()
        item.delete()

    cart.delete()  # Supprimer le panier après suppression des articles

    return JsonResponse({'success': True, 'message': 'Le panier a été vidé'})

@require_GET
def get_product_details(request, article_id):
    try:
        product = AllProducts.objects.get(id=article_id)
        return JsonResponse({'status': 'success', 'data': {
            'id': product.id,
            'nom': product.nom,
            'prix': product.prix,
            'disponible': product.disponible
        }})
    except AllProducts.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

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

@require_POST
@csrf_protect
def rendre_disponible(request, product_id):
    try:
        product = AllProducts.objects.get(id=product_id)
        product.disponible = True
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

    def update_lien(lien_image):
        if "www.dropbox.com" in lien_image:
            lien_image = lien_image.replace("www.dropbox.com", "dl.dropboxusercontent.com")
        if "st=" in lien_image:  
            lien_image = lien_image.split("&st=")[0].rstrip("&")
        return lien_image

    for product in all_products:
        if product.lien_image1:
            product.lien_image1 = update_lien(product.lien_image1)
        if product.lien_image2:
            product.lien_image2 = update_lien(product.lien_image2)
        if product.lien_image3:
            product.lien_image3 = update_lien(product.lien_image3)
        if product.lien_image4:
            product.lien_image4 = update_lien(product.lien_image4)
        product.save()


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
    return HttpResponse("Les macramés:<br>" + list_macrames_complette)
    """