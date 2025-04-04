from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return [
            'boutique:index',
            'boutique:macrames',
            'boutique:maroquinerie',
            'boutique:creation-sur-mesure',
            'boutique:hybride',
            'boutique:produits',
            'boutique:panier',
            'boutique:a_propos',
            'boutique:payment_success',
            'boutique:payment_cancel',
            'boutique:cgv',
            'boutique:cookies',
            'boutique:legal_mentions',
            'boutique:privacy_policy',
        ]

    def location(self, item):
        return reverse(item)  # Génère les URLs automatiquement