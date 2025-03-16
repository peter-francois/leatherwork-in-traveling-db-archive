from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import ProductFilterForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.timezone import now
from .utils import get_session_expiration
import stripe
import json
import logging
from django.conf import settings
# pour résoudre le problème de CSRF token
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import timedelta


stripe.api_key = settings.STRIPE_SECRET_KEY


logger = logging.getLogger(__name__)
# Pour Forcer l’envoi du cookie CSRF lors de l’affichage de l’index
@ensure_csrf_cookie
def index(request):    


    # return JsonResponse({"message": "CSRF Cookie Set"})
    return render(request, 'page_vente/index.html')

def tous_les_produits(request):

    all_products = AllProducts.objects.all()
    
    all_products = [product for product in all_products if product.disponible and not product.en_attente_dans_panier]

    all_products.sort(key=lambda product: product.id, reverse=True)

    all_products, form = use_filter(request, all_products, is_all_products=True )

    page_obj = pagination(request,all_products)

    context = {
        'products': page_obj,
        'form': form,
    }

    return render(request, 'page_vente/tous_les_produits.html', context)

def maroquinerie(request):

    all_leather_products = AllProducts.objects.all().filter(categorie='Maroquinerie')
    all_leather_products = [product for product in all_leather_products if product.disponible and not product.en_attente_dans_panier]
    
    all_leather_products.sort(key=lambda product: product.id, reverse=True)

    all_leather_products, form = use_filter(request, all_leather_products, is_all_products=False)

    page_obj = pagination(request,all_leather_products)

    context = {
        'products': page_obj,
        'form': form,
    }

    return render(request, 'page_vente/maroquinerie.html', context)

def macrames(request):

    all_macrame_products = AllProducts.objects.all().filter(categorie='Macrame')
    all_macrame_products = [product for product in all_macrame_products if product.disponible and not product.en_attente_dans_panier]

    all_macrame_products.sort(key=lambda product: product.id, reverse=True)

    all_macrame_products, form = use_filter(request, all_macrame_products, is_all_products=False)

    page_obj = pagination(request,all_macrame_products)

    context = {
        'products': page_obj,
        'form': form,
    }

    return render(request, 'page_vente/macrames.html', context)

def hybride(request):
    all_hybride_products = AllProducts.objects.all().filter(categorie='Hybride')
    all_hybride_products = [product for product in all_hybride_products if product.disponible and not product.en_attente_dans_panier]

    all_hybride_products.sort(key=lambda product: product.id, reverse=True)

    all_hybride_products, form = use_filter(request, all_hybride_products, is_all_products=False)

    page_obj = pagination(request,all_hybride_products)

    context = {
        'products': page_obj,
        'form': form,
    }

    return render(request, 'page_vente/hybride.html', context)

def creation_sur_mesure(request):
    return render(request, 'page_vente/creation_sur_mesure.html')

def panier(request):
    session_key = request.session.session_key
    latest_cgv = CGV.objects.latest('created_at')
    cart = Cart.objects.filter(session_id=session_key).first()
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.prix * item.quantity for item in items)
    expiration_date = get_session_expiration(request)


    return render(request, "page_vente/panier.html", {
        "expiration_date": expiration_date,
        "items": items,
        "total": total,
        "latest_cgv": latest_cgv,
    })

def a_propos(request):
    return render(request, 'page_vente/a_propos.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(AllProducts, id=product_id)

    if not product.disponible or product.en_attente_dans_panier:
        return JsonResponse({'success': False, 'message': 'Produit déjà pris'}, status=400)

    # Récupérer l'expiration de la session
    expiration_date = get_session_expiration(request)


    
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # Vérifier si un panier existe pour cette session
    cart, created = Cart.objects.get_or_create(session_id=session_id,defaults={'uuid': uuid.uuid4()})

    # Ajouter le produit au panier
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    # Marquer le produit comme en attente dans le panier
    product.en_attente_dans_panier = True
    product.save()

    return JsonResponse({
        'success': True, 
        'message': f'{product.nom} ajouté au panier',
        'cart_uuid': str(cart.uuid),
        "session_expiration": expiration_date.strftime('%Y-%m-%d %H:%M:%S') if expiration_date else None})

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

    return JsonResponse({'cart': data,})

def vider_panier(request):
    session_id = request.session.session_key
    if not session_id:
        return JsonResponse({'success': False, 'message': 'Aucun panier trouvé'})

    cart = Cart.objects.filter(session_id=session_id).first()
    if not cart:
        return JsonResponse({'success': False, 'message': 'Le panier est déjà vide'})

    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.product.en_attente_dans_panier = False
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
        cart_item.product.en_attente_dans_panier = False
        cart_item.product.save()
        cart_item.delete()
        return JsonResponse({'success': True, 'message': 'Article retiré du panier', 'article': {"id": cart_item.product.id, "prix": cart_item.product.prix}})
    else:
        return JsonResponse({'success': False, 'message': 'Article non trouvé dans le panier'})

def get_product_images(request, article_id):
    try:
        product = AllProducts.objects.get(id=article_id)
        images = [
            product.image1.url if product.image1 else None,
            product.image2.url if product.image2 else None,
            product.image3.url if product.image3 else None,
            product.image4.url if product.image4 else None,
            ]
        images = [image for image in images if image]
        return JsonResponse({'images': images, 'nom': product.nom, 'description': product.description if product.description else None, 'prix': product.prix})
    except AllProducts.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def use_filter(request, product_views, is_all_products):
    if not product_views:
        return product_views, None

    if is_all_products:
        form = ProductFilterForm(request.GET, categorie=None)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            type = form.cleaned_data.get('type')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')

            if search:
                product_views = [product for product in product_views if search.lower() in product.nom.lower()]
            if type:
                if type == '---':
                    type = None
                else:
                    product_views = [product for product in product_views if product.type == type]
            if min_price is not None:
                product_views = [product for product in product_views if product.prix >= min_price]
            if max_price is not None:
                product_views = [product for product in product_views if product.prix <= max_price]
        
        return product_views, form
    else:
        categorie = product_views[0].categorie if hasattr(product_views[0], 'categorie') else None
        if not categorie:
            return product_views, None
        form = ProductFilterForm(request.GET, categorie=categorie)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            type = form.cleaned_data.get('type')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')

            if search:
                product_views = [product for product in product_views if search.lower() in product.nom.lower()]
            if type:
                if type == '---':
                    type = None
                else:
                    product_views = [product for product in product_views if product.type == type]
            if min_price is not None:
                product_views = [product for product in product_views if product.prix >= min_price]
            if max_price is not None:
                product_views = [product for product in product_views if product.prix <= max_price]
        
        return product_views, form

def pagination(request,product_views):

    paginator = Paginator(product_views, 20)  # 20 articles par page
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)

def checkout(request):
    
    cart_uuid = request.GET.get('cart_uuid')
    front_total = float(request.GET.get('front_total'))
    cart = Cart.objects.filter(uuid=cart_uuid, paid=False).first()

    if not cart:
        return JsonResponse({'error': 'Panier invalide ou expiré.'}, status=400)

    # select_for_update() lors de la récupération des articles pour verrouiller les lignes et éviter les conflits
    cart_items = CartItem.objects.select_for_update().filter(cart=cart)

    if not cart_items:
        logger.error("Le panier est vide.")
        return JsonResponse({'error': 'Le panier est vide'}, status=400)

    # Récupérer les paramètres envoyés par le front
    add_insurance = request.GET.get('insurance') == '1'
    acceptCGV = request.GET.get('acceptCGV') == '1'
    # Vérifier si l'utilisateur a accepté les conditions générales de vente
    if not acceptCGV:
        logger.error("L'utilisateur n'a pas accepté les conditions générales de vente.")
        return JsonResponse({'error': 'Vous devez accepter les conditions générales de vente'}, status=400)
    
    # Récupérer la dernière version des CGV
    latest_cgv = CGV.objects.latest('created_at')

    # Enregistrer l'acceptation des CGV
    if not cart.cgv_accepted:
        cart.cgv_accepted = latest_cgv
        cart.cgv_accepted_at = now()
        cart.cgv_expires_at = cart.cgv_accepted_at + timedelta(days=5*365)
        cart.save()
        
    # Calcul du montant total sécurisé côté serveur
    total = sum(item.product.prix * item.quantity for item in CartItem.objects.filter(cart__uuid=cart_uuid))


    # Ajouter l'assurance si nécessaire

    if total > 50:
        if total > 375:
            total += 8.00
        elif total > 250:
            total += 6.50
        elif total > 125:
            total += 5.00
        else:
            total += 3.50
    elif 25 < total <= 50 and add_insurance:
        total += 2.00

    # Appliquer les frais de port
    total += 5
    if total <= 0:
        return JsonResponse({'error': 'Montant invalide.'}, status=400)
    
    # Vérifications de cohérance entre le montant envoyé par le front et le montant total sécurisé côté serveur
    if front_total != total:
        return JsonResponse({'error': 'Probleme de cohérence des montants', 'total': total, 'front_total': front_total}, status=400)
    

    return JsonResponse({'versionCGV': latest_cgv.version,'cgv_accepted_at': cart.cgv_accepted_at, 'total': total,'articles_quantity': cart.cartitem_set.count(),'add_insurance': add_insurance,'acceptCGV': acceptCGV,'cart_uuid': cart_uuid})

    # Créer la session de paiement Stripe
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f"Commande de {cart.cartitem_set.count()} article{'s' if cart.cartitem_set.count() > 1 else ''}",
                        'metadata': {
                            'cart_uuid': str(cart_uuid),
                            'acceptCGV': str(acceptCGV),
                            'cgv_version': str(cart.cgv_accepted.version),
                            'add_insurance': str(add_insurance),
                            'total_verified': int(total * 100)
                        }
                    },
                    'unit_amount': int(total * 100),  # Stripe utilise des centimes
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'https://localhost:8001/success?session_id={checkout_session.id}' if settings.DEBUG else f'https://tonsite.com/success?session_id={checkout_session.id}',
            cancel_url='https://localhost:8001/cancel' if settings.DEBUG else 'https://tonsite.com/cancel',
        )
        return redirect(checkout_session.url)
    # Gestion des erreurs spécifiques à Stripe
    except stripe.error.StripeError as e:
        logger.error(f"Erreur Stripe : {e}")
        return JsonResponse({'error': 'Erreur de paiement, veuillez réessayer.'}, status=500)
    # Gestion des autres erreurs
    except Exception as e:
        logger.exception("Erreur inattendue lors de la création de la session Stripe.")
        return JsonResponse({'error': 'Une erreur est survenue.'}, status=500)

def success_view(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('/')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status != 'paid':
            return redirect('/')

        # Récupérer le panier via metadata
        cart_uuid = session.metadata.get('cart_uuid')
        cart = get_object_or_404(Cart, uuid=cart_uuid)

        # Vérifier que le total correspond bien
        total_verified = int(session.unit_amount) / 100
        if total_verified != cart.get_total():
            return redirect('/')

        return render(request, 'page_vente/payment_success.html', {
            'order_id': cart.id,
            'total_amount': total_verified,
            'payment_date': cart.paid_at
        })

    except stripe.error.StripeError:
        return redirect('/')

def cancel_view(request):
    return render(request, 'page_vente/payment_cancel.html')

@csrf_exempt  # Désactive la protection CSRF pour recevoir les requêtes Stripe
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature', '')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # 🎯 Si un paiement est réussi
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        cart_uuid = session.get('metadata', {}).get('cart_uuid')

        if cart_uuid:
            cart = get_object_or_404(Cart, uuid=cart_uuid)
            if not cart.paid:  # Vérifier que le panier n'a pas déjà été traité
                cart.paid = True
                cart.paid_at = now()
                cart.cart_expires_at = cart.paid_at + timedelta(days=10*365)
                cart.cartitem_set.update(product__disponible=False, product__en_attente_dans_panier=False)
                cart.save()

    return JsonResponse({'status': 'success'}, status=200)

def cgv_view(request):
    latest_cgv = CGV.objects.latest('created_at')
    return render(request, 'page_vente/cgv.html', {'cgv': latest_cgv})

def cookies_view(request):
    latest_cookies = CookiesPolicy.objects.latest('created_at')
    return render(request, 'page_vente/cookies.html', {'cookies': latest_cookies})

def legal_mentions_view(request):
    latest_legal_mentions = LegalMention.objects.latest('created_at')
    return render(request, 'page_vente/mentions-legales.html', {'legal_mentions': latest_legal_mentions})

def privacy_policy_view(request):
    latest_privacy_policy = PrivacyPolicy.objects.latest('created_at')
    return render(request, 'page_vente/politique-confidentialite.html', {'privacy_policy': latest_privacy_policy})

def get_number_of_products_in_cart(request):
    session_key = request.session.session_key

    # Vérifie si le session_key est valide
    if not session_key:
        return JsonResponse({'success': False, 'number_of_products': 0})

    try:
        # Récupère le panier lié à la session
        cart = Cart.objects.filter(session_id=session_key).first()

        # Si aucun panier n'est trouvé
        if not cart:
            return JsonResponse({'success': False, 'number_of_products': 0})

        # Comptage des articles dans le panier
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items_count = cart_items.count()
        return JsonResponse({'success': True, 'number_of_products': cart_items_count})

    except ObjectDoesNotExist:
        # Si une erreur se produit avec l'accès aux objets, retourner une réponse vide
        return JsonResponse({'success': False, 'number_of_products': 0})