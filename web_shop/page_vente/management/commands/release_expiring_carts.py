from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from page_vente.models import Cart, CartItem
from datetime import timedelta
from django.conf import settings

class Command(BaseCommand):
    help = "Libère les articles des paniers qui vont expirer bientôt"

    def handle(self, *args, **kwargs):
        # Seuil de libération des articles (ex: 1 heure avant expiration)
        expiration_threshold = now() + timedelta(hours=1)

        # Trouver les sessions qui vont expirer bientôt
        expiring_sessions = Session.objects.filter(expire_date__lte=expiration_threshold)

        if not expiring_sessions.exists():
            self.stdout.write("✅ Aucun panier expiré à libérer.")
            return

        # Récupérer et supprimer les paniers correspondants
        expired_session_keys = expiring_sessions.values_list('session_key', flat=True)
        expired_carts = Cart.objects.filter(session_id__in=expired_session_keys)

        # Libérer les produits de ces paniers
        for cart in expired_carts:
            for item in CartItem.objects.filter(cart=cart):
                product = item.product
                product.disponible = True  # Remettre l'article disponible
                product.save()
            cart.delete()  # Supprimer le panier après avoir libéré les produits

        # Supprimer les sessions expirées
        expiring_sessions.delete()

        self.stdout.write("✔️ Produits des paniers bientôt expirés libérés")

        # Supprimer les sessions expirées
        for session_key in expired_session_keys:
            settings.SESSION_ENGINE.SessionStore(session_key).delete()
        