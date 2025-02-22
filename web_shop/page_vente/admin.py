from django.contrib import admin
from .models import *
from django.contrib import messages
from .forms import *
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
    actions = ['rendre_disponible', 'rendre_indisponible']
    list_display = ('nom','categorie','disponible', 'type', 'ornement', 'prix')
    search_fields = ['nom','categorie', 'type']
    list_filter = ['categorie', 'disponible']
    form = AllProductsForm

    def rendre_disponible(self,  request, queryset):
        queryset.update(disponible=True)

    def rendre_indisponible(self, request, queryset):
        queryset.update(disponible=False)
    

    def on_save_model(self, request, obj, form, change):
        super().on_save_model(request, obj, form, change)  # Appeler la méthode parente
        forms.update_type(self)



    
admin.site.register(AllProducts, AllProductsAdmin)