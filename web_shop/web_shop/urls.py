"""
URL configuration for web_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from page_vente import views
from django.contrib.sitemaps.views import sitemap as django_sitemap
from page_vente.sitemaps import StaticSitemap
from django.views.i18n import JavaScriptCatalog
from django.contrib.sitemaps.views import sitemap

app_name = 'main'

sitemaps = {
    'static': StaticSitemap('fr'), 
    'static_en': StaticSitemap('en'),
}

"""urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('page_vente.urls')),
]"""
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('page_vente.urls')),  # Inclusion des URLs de ton app
    path('i18n/', include('django.conf.urls.i18n')),  # Activation du changement de langue
)

urlpatterns += [
    path('sitemap.xml', views.sitemap_index, name='sitemap-index'),
    path('sitemap-fr.xml', views.sitemap_lang, {'lang': 'fr'}, name='sitemap-fr'),
    path('sitemap-en.xml', views.sitemap_lang, {'lang': 'en'}, name='sitemap-en'),
    path('api/', include('page_vente.api_urls')),  # Déplacer API dans un autre fichier
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
