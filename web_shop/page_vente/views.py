from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import ProductFilterForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.utils.timezone import now
from .utils import get_session_expiration

def add_to_cart(request, product_id):
    product = get_object_or_404(AllProducts, id=product_id)

    if not product.disponible:
        return JsonResponse({'success': False, 'message': 'Produit déjà pris'}, status=400)

    # Récupérer l'ID de session unique de Django
    expiration_date = get_session_expiration(request)
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

    return JsonResponse({'success': True, 'message': f'{product.nom} ajouté au panier', "session_expiration": expiration_date.strftime('%Y-%m-%d %H:%M:%S') if expiration_date else None})

def cart_detail(request):
    session_id = request.session.session_key
    if not session_id:
        return JsonResponse({'cart': []})  # Aucun panier trouvé

    cart = Cart.objects.filter(session_id=session_id).first()
    if not cart:
        return JsonResponse({'cart': []})  

    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    data = [{'nom': item.product.nom, 'prix': item.product.prix, 'quantity': item.quantity, 'image1': item.product.image1.url, 
            'image2': item.product.image2.url, 'image3': item.product.image3.url, 'image4': item.product.image4.url, 'id': item.product.id} for item in cart_items]

    return JsonResponse({'cart': data})

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

    return JsonResponse({'success': True, 'message': 'Le panier a été vide'})

def remove_from_cart(request, product_id):
    session_id = request.session.session_key
    if not session_id:
        return JsonResponse({'success': False, 'message': 'Aucun panier trouvé'})
    cart = Cart.objects.filter(session_id=session_id).first()
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if cart_item:
        cart_item.delete()
        cart_item.product.disponible = True  # Rendre le produit disponible
        cart_item.product.save()
        return JsonResponse({'success': True, 'message': 'Article retiré du panier'})
    else:
        return JsonResponse({'success': False, 'message': 'Article non trouvé dans le panier'})

def tous_les_produits(request):
    all_products = AllProducts.objects.all()
    form = ProductFilterForm(request.GET)
    images = []
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
    paginator = Paginator(all_products, 20)  # 20 articles par page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'form': form,
    }

    return render(request, 'page_vente/tous_les_produits.html', context)

def panier(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_id=session_key).first()
    items = CartItem.objects.filter(cart=cart)
    expiration_date = get_session_expiration(request)


    return render(request, "page_vente/panier.html", {
        "expiration_date": expiration_date,
        "items": items
    })

def get_product_images(request, article_id):
    try:
        product = AllProducts.objects.get(id=article_id)
        images = [product.image1.url , product.image2.url, product.image3.url, product.image4.url]
        images = [image for image in images if image]
        return JsonResponse({'images': images, 'nom': product.nom})
    except AllProducts.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def index(request):    
    return render(request, 'page_vente/index.html')

def macrames(request):
    return render(request, 'page_vente/macrames.html')

def a_propos(request):
    return render(request, 'page_vente/a_propos.html')

def maroquinerie(request):
    return render(request, 'page_vente/maroquinerie.html')

def creation_sur_mesure(request):
    return render(request, 'page_vente/creation_sur_mesure.html')

def hybride(request):
    return render(request, 'page_vente/hybride.html')

def contact(request):
    return render(request, 'page_vente/contact.html')