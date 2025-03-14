from django.contrib import admin
from .models import *
from django.contrib import messages
from .forms import *
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction




class AllProductsForm(forms.ModelForm):
    class Meta:
        model = AllProducts
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        for field in ['image1', 'image2', 'image3', 'image4']:
            image_file = cleaned_data.get(field)
            if image_file:
                if hasattr(image_file, 'size') and image_file.size > 10 * 1024 * 1024:  # 10 Mo
                    raise ValidationError({field: _('Le fichier est trop volumineux. La taille maximale est de 10 Mo.')})
        return cleaned_data


class AllProductsAdmin(admin.ModelAdmin):
    actions = ['rendre_disponible', 'rendre_indisponible','retirer_du_panier']
    list_display = ('nom','categorie','disponible','en_attente_dans_panier', 'type', 'description', 'prix')
    search_fields = ['nom','categorie', 'type']
    list_filter = ['categorie', 'disponible']
    form = AllProductsForm

    def rendre_disponible(self,  request, queryset):
        queryset.update(disponible=True)

    def rendre_indisponible(self, request, queryset):
        queryset.update(disponible=False)

    def retirer_du_panier(self, request, queryset):
        articles_id = list(queryset.values_list('id', flat=True))

        with transaction.atomic():
            # Suppression des articles du panier liés aux produits
            deleted_count, _ = CartItem.objects.filter(product__in=articles_id).delete()

            # Mise à jour du statut en attente
            queryset.update(en_attente_dans_panier=False)

        # Message pour l’utilisateur
        if deleted_count > 0:
            messages.success(request, f"{deleted_count} article(s) n'est plus disponible dans votre panier.")    
        

    def on_save_model(self, request, obj, form, change):
        super().on_save_model(request, obj, form, change)  # Appeler la méthode parente
        forms.update_type(self)

@admin.register(CGV)
class CGVAdmin(admin.ModelAdmin):
    list_display = ('version', 'created_at')
    ordering = ('-created_at',)

    
admin.site.register(AllProducts, AllProductsAdmin)