from django.urls import path
from . import views
from page_vente.views import *
from django.utils.translation import gettext_lazy as _



app_name = 'boutique'


urlpatterns = [
    path('', views.index, name="index"),
    path(_('produits/macrames/'), views.macrames, name="macrames"),
    path(_('produits/maroquinerie/'), views.maroquinerie, name="maroquinerie"),
    path(_('creation-sur-mesure/'), views.creation_sur_mesure, name="creation-sur-mesure"),
    path(_('produits/hybride/'), views.hybride, name="hybride"),
    path(_('produits/'), views.produits, name="produits"),
    path(_('panier/'), views.panier, name="panier"),
    path(_('contact/'), views.contact, name="contact"),
    # path(_('a_propos/'), views.a_propos, name="a_propos"),
    path(_('cgv/'), views.cgv_view, name="cgv"),
    path(_('cookies/'), views.cookies_view, name="cookies"),
    path(_('mentions-legales/'), views.legal_mentions_view, name="legal_mentions"),
    path(_('politique-confidentialite/'), views.privacy_policy_view, name="privacy_policy"),
    path(_('paiement_reussi/'), views.success_view, name='paiement_reussi'),
    path(_('paiement_annule/'), views.cancel_view, name='paiement_annule'),
]