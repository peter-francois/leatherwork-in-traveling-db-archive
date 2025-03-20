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
from django.urls import reverse
import base64
import os



stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


logger = logging.getLogger(__name__)
# Pour Forcer l’envoi du cookie CSRF lors de l’affichage de l’index
@ensure_csrf_cookie
def index(request):
    nonce = generate_nonce()
    return render(request, 'page_vente/index.html', {'nonce': nonce})

def tous_les_produits(request):
    nonce = generate_nonce()
    all_products = AllProducts.objects.all()

    all_products = [product for product in all_products if product.disponible and not product.en_attente_dans_panier]

    all_products.sort(key=lambda product: product.id, reverse=True)

    all_products, form = use_filter(request, all_products, is_all_products=True )

    page_obj = pagination(request,all_products)

    context = {
        'products': page_obj,
        'form': form,
        'nonce': nonce
    }

    return render(request, 'page_vente/tous_les_produits.html', context)

def maroquinerie(request):
    nonce = generate_nonce()

    all_leather_products = AllProducts.objects.all().filter(categorie='Maroquinerie')
    all_leather_products = [product for product in all_leather_products if product.disponible and not product.en_attente_dans_panier]

    all_leather_products.sort(key=lambda product: product.id, reverse=True)

    all_leather_products, form = use_filter(request, all_leather_products, is_all_products=False)

    page_obj = pagination(request,all_leather_products)

    context = {
        'products': page_obj,
        'form': form,
        'nonce': nonce
    }

    return render(request, 'page_vente/maroquinerie.html', context)

def macrames(request):
    nonce = generate_nonce()

    all_macrame_products = AllProducts.objects.all().filter(categorie='Macrame')
    all_macrame_products = [product for product in all_macrame_products if product.disponible and not product.en_attente_dans_panier]

    all_macrame_products.sort(key=lambda product: product.id, reverse=True)

    all_macrame_products, form = use_filter(request, all_macrame_products, is_all_products=False)

    page_obj = pagination(request,all_macrame_products)

    context = {
        'products': page_obj,
        'form': form,
        'nonce': nonce
    }

    return render(request, 'page_vente/macrames.html', context)

def hybride(request):
    nonce = generate_nonce()
    all_hybride_products = AllProducts.objects.all().filter(categorie='Hybride')
    all_hybride_products = [product for product in all_hybride_products if product.disponible and not product.en_attente_dans_panier]

    all_hybride_products.sort(key=lambda product: product.id, reverse=True)

    all_hybride_products, form = use_filter(request, all_hybride_products, is_all_products=False)

    page_obj = pagination(request,all_hybride_products)

    context = {
        'products': page_obj,
        'form': form,
        'nonce': nonce
    }

    return render(request, 'page_vente/hybride.html', context)

def creation_sur_mesure(request):
    nonce = generate_nonce()
    return render(request, 'page_vente/creation_sur_mesure.html', {'nonce': nonce})

def panier(request):
    nonce = generate_nonce()
    session_key = request.session.session_key
    latest_cgv = CGV.objects.latest('created_at')
    cart = Cart.objects.filter(session_id=session_key, paid=False).first()
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.prix * item.quantity for item in items)
    expiration_date = get_session_expiration(request)

    return render(request, "page_vente/panier.html", {
        "expiration_date": expiration_date,
        "items": items,
        "total": total,
        "latest_cgv": latest_cgv,
        'nonce': nonce
    })

def a_propos(request):
    nonce = generate_nonce()
    return render(request, 'page_vente/a_propos.html', {'nonce': nonce})

def add_to_cart(request, product_id):
    product = get_object_or_404(AllProducts, id=product_id)

    if not product.disponible or product.en_attente_dans_panier:
        return JsonResponse({'success': False, 'message': 'Produit déjà pris'}, status=400)

    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # Vérifier si un panier existe pour cette session
    cart, created = Cart.objects.get_or_create(session_id=session_id,defaults={'uuid': uuid.uuid4()})

    if cart.paid:
        request.session.create()
        session_id = request.session.session_key
        cart = Cart.objects.create(session_id=session_id, uuid=uuid.uuid4())

    # Récupérer l'expiration de la session
    expiration_date = get_session_expiration(request)


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
        "session_expiration": expiration_date.strftime('%Y-%m-%d %H:%M:%S') if expiration_date else None,
    })

def cart_detail(request):
    session_id = request.session.session_key
    if not session_id:
        return JsonResponse({'cart': []})  # Aucun panier trouvé

    cart = Cart.objects.filter(session_id=session_id, paid=False).first()

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

    cart = Cart.objects.filter(session_id=session_id, paid=False).first()
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
    cart = Cart.objects.filter(session_id=session_id, paid=False).first()
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

def get_total(cart, add_insurance):

    # Calculer le total en centimes
    total = Cart.get_total(cart)
    total_centimes = int(round(total * 100))

    # Ajouter l'assurance en centimes si nécessaire
    if total_centimes > 5000:
        if total_centimes > 37500:
            total_centimes += 800
        elif total_centimes > 25000:
            total_centimes += 650
        elif total_centimes > 12500:
            total_centimes += 500
        else:
            total_centimes += 350
    elif 2500 < total_centimes <= 5000:
        if add_insurance:
            total_centimes += 200

    # Ajouter les frais de port en centimes
    total_centimes += 500

    # Vérification du total
    if total_centimes <= 0:
        return JsonResponse({'error': 'Montant invalide.'}, status=400)

    return total_centimes  # Total en centimes

def checkout(request):
    nonce = generate_nonce()
    cart_uuid = request.GET.get('cart_uuid')
    cart = Cart.objects.filter(uuid=cart_uuid, paid=False).first()
    front_total = float(request.GET.get('front_total'))

    if not cart:
        return JsonResponse({'error': 'Panier invalide ou expiré.'}, status=400)

    # Récupérer les paramètres envoyés par le front
    add_insurance = request.GET.get('insurance') == '1'
    acceptCGV = request.GET.get('acceptCGV') == '1'
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

    # Calcul du total en centimes
    total_centimes = get_total(cart, add_insurance)

    # Convertir le montant du front-end en centimes pour la comparaison
    front_total_centimes = int(round(front_total * 100))

    # Comparaison en centimes
    if front_total_centimes != total_centimes:
        return JsonResponse({'error': 'Problème de cohérence des montants', 'total': total_centimes / 100, 'front_total': front_total}, status=400)

    # Créer la session de paiement Stripe
    list_products = []
    for item in cart.cartitem_set.all():
        list_products.append({
            'name': item.product.nom,
        })
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f"Commande de {cart.cartitem_set.count()} article{'s' if cart.cartitem_set.count() > 1 else ''}",
                    },
                    'unit_amount': total_centimes,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=("http://localhost:8002/payment_success?session_id={CHECKOUT_SESSION_ID}" if settings.DEBUG else "https://www.leatherworkintravelingdb.com/payment_success?session_id={CHECKOUT_SESSION_ID}"),
            cancel_url=("http://localhost:8002/payment_cancel" if settings.DEBUG else "https://www.leatherworkintravelingdb.com/payment_cancel"),
            metadata={
                            'cart_uuid': str(cart_uuid),
                            'acceptCGV': str(acceptCGV),
                            'cgv_version': str(cart.cgv_accepted.version),
                            'add_insurance': str(add_insurance),
                            'total_verified': total_centimes,
                            'list_products': str(list_products)
                        },
            shipping_address_collection={
                'allowed_countries': ['FR','DE','AT','BE','ES','IT','LU','NL','PT'],
            },
        )
        return redirect(checkout_session.url, {'nonce': nonce})
    except stripe.error.StripeError as e:
        logger.error(f"Erreur Stripe : {e}")
        return JsonResponse({'error': 'Erreur de paiement, veuillez réessayer.'}, status=500)
    except Exception as e:
        logger.exception("Erreur inattendue lors de la création de la session Stripe.")
        return JsonResponse({'error': 'Une erreur est survenue.'}, status=500)

def success_view(request):
    nonce = generate_nonce()
    session_id = request.GET.get('session_id')
    if not session_id:
        logger.error("Session ID manquant.")
        return redirect('/', {'nonce': nonce})

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status != 'paid':
            return redirect('/')

       # 🔹 Vérifier si `metadata` existe avant d'accéder à `cart_uuid`
        if not session.metadata or "cart_uuid" not in session.metadata:
            return redirect('/')

        cart_uuid = session.metadata["cart_uuid"]
        add_insurance = session.metadata['add_insurance'] == '1'

        # ✅ Convertir cart_uuid en format UUID
        try:
            cart_uuid = uuid.UUID(cart_uuid)  # Transforme la string en UUID valide
        except ValueError:
            logger.error("UUID du panier invalide.")
            return redirect('/')

        cart = get_object_or_404(Cart, uuid=cart_uuid)

        # Vérifier que le total correspond bien
        total_verified_centimes = session.amount_total
        if total_verified_centimes != get_total(cart, add_insurance):
            logger.error(f"Montant invalide. Total vérifié: {total_verified_centimes}, Total du panier: {get_total(cart, add_insurance)}")
            return redirect('/')

        total_verified = round(total_verified_centimes / 100, 2)
        return render(request, 'page_vente/payment_success.html', {
            'order_id': cart.id,
            'total_amount': total_verified,
            'payment_date': cart.paid_at if cart.paid_at else "Non disponible",
            'nonce': nonce
        })

    except stripe.error.StripeError:
        logger.error("Erreur Stripe lors de la récupération de la session.")
        return redirect('/', {'nonce': nonce})

def cancel_view(request):
    nonce = generate_nonce()
    return render(request, 'page_vente/payment_cancel.html', {'nonce': nonce})

@csrf_exempt  # Désactive la protection CSRF pour recevoir les requêtes Stripe
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature', '')


    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)
    # 🎯 Si un paiement est réussi
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # 🔹 Vérifier si `metadata` existe avant d'accéder à `cart_uuid`
        metadata = session.get("metadata", {})
        cart_uuid = metadata.get("cart_uuid")

        cart = get_object_or_404(Cart, uuid=cart_uuid)
        if not cart.paid:  # Vérifier que le panier n'a pas déjà été traité
            cart.paid = True
            cart.paid_at = now()
            cart.cart_expires_at = cart.paid_at + timedelta(days=10*365)
            cart.save()
        # 🔄 Mettre à jour la disponibilité des produits du panier
            for item in cart.cartitem_set.all():
                product = item.product
                product.disponible = False
                product.en_attente_dans_panier = False
                product.save()

        logger.info(f"✅ Paiement reçu pour le panier {cart_uuid}")

        # Récupérer les informations du client
        customer_email = session.get('customer_details', {}).get('email', 'Email inconnu')
        customer_name = session.get('customer_details', {}).get('name', 'Nom inconnu')
        shipping_address = session.get('customer_details', {}).get('address', {})
        list_products = metadata.get('list_products')


        # Vous pouvez maintenant utiliser ces informations pour envoyer un email de confirmation
        send_email_to_owner(customer_email, customer_name, shipping_address, list_products)

    return JsonResponse({'status': 'success'}, status=200)

def send_email_to_owner(customer_email, customer_name, shipping_address, list_products):
    # Exemple d'envoi d'email à l'administrateur du site (propriétaire du compte Stripe)
    from django.core.mail import send_mail

    subject = 'Nouvelle commande reçue'
    message = f"""
    <html>
    <body>
    <p>Une nouvelle commande a été passée par {customer_name}.</p>
    <p>Détails de la commande :</p>
    <ul>
        <li>Email client : {customer_email}</li>
        <li>Pays : {shipping_address.get('country', 'Pays inconnu')}</li>
        <li>Adresse de livraison : {shipping_address.get('line1', 'Adresse inconnue')}, {shipping_address.get('line2', '')}, {shipping_address.get('city', 'Ville inconnue')}</li>
        <li>Code postal : {shipping_address.get('postal_code', 'Code postal inconnu')}</li>
        <li>Ville : {shipping_address.get('city', 'Ville inconnue')}</li>
    </ul>
    <p>Produits commandés :</p>
    <ul>
    {''.join(f'<li><img src="{product['image_url']}" alt="{product['name']}" style="width:100px;" /> {product['name']}</li>' for product in list_products)}
    </ul>
    <p>Merci de traiter la commande.</p>
    </body>
    </html>
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Adresse email de l'expéditeur
        [settings.CLIENT_EMAIL],
    )

def cgv_view(request):
    nonce = generate_nonce()
    latest_cgv = CGV.objects.latest('created_at')
    return render(request, 'page_vente/cgv.html', {'cgv': latest_cgv, 'nonce': nonce})

def cookies_view(request):
    nonce = generate_nonce()
    latest_cookies = CookiesPolicy.objects.latest('created_at')
    return render(request, 'page_vente/cookies.html', {'cookies': latest_cookies, 'nonce': nonce})

def legal_mentions_view(request):
    nonce = generate_nonce()
    latest_legal_mentions = LegalMention.objects.latest('created_at')
    return render(request, 'page_vente/mentions-legales.html', {'legal_mentions': latest_legal_mentions, 'nonce': nonce})

def privacy_policy_view(request):
    nonce = generate_nonce()
    latest_privacy_policy = PrivacyPolicy.objects.latest('created_at')
    return render(request, 'page_vente/politique-confidentialite.html', {'privacy_policy': latest_privacy_policy, 'nonce': nonce})

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
        if cart.paid:
            return JsonResponse({'success': False, 'number_of_products': 0})

        # Comptage des articles dans le panier
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items_count = cart_items.count()
        return JsonResponse({'success': True, 'number_of_products': cart_items_count})

    except ObjectDoesNotExist:
        # Si une erreur se produit avec l'accès aux objets, retourner une réponse vide
        return JsonResponse({'success': False, 'number_of_products': 0})

def get_document_content(request, document_type, lang):
    nonce = generate_nonce()
    try:
        if document_type == 'CGV':
            latest_cgv = CGV.objects.latest('created_at')
            content = latest_cgv.content_fr if lang == 'fr' else latest_cgv.content_en
            cookies_url = reverse('boutique:cookies')
            privacy_policy_url = reverse('boutique:privacy_policy')
            content = content.replace("cookies_url", cookies_url)
            content = content.replace("privacy_policy_url", privacy_policy_url)
        elif document_type == 'Cookies':
            latest_cookies = CookiesPolicy.objects.latest('created_at')
            content = latest_cookies.content_fr if lang == 'fr' else latest_cookies.content_en
        elif document_type == 'LegalMentions':
            latest_legal_mentions = LegalMention.objects.latest('created_at')
            content = latest_legal_mentions.content_fr if lang == 'fr' else latest_legal_mentions.content_en
            cookies_url = reverse('boutique:cookies')
            cgv_url = reverse('boutique:cgv')
            privacy_policy_url = reverse('boutique:privacy_policy')
            content = content.replace("cookies_url", cookies_url)
            content = content.replace("cgv_url", cgv_url)
            content = content.replace("privacy_policy_url", privacy_policy_url)

        elif document_type == 'PrivacyPolicy':
            latest_privacy_policy = PrivacyPolicy.objects.latest('created_at')
            content = latest_privacy_policy.content_fr if lang == 'fr' else latest_privacy_policy.content_en
        else:
            return JsonResponse({'error': 'Invalid document type'}, status=400)

        return HttpResponse(content, content_type="text/html")

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_nonce():
    return base64.b64encode(os.urandom(16)).decode('utf-8')