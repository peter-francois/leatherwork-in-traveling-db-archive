from django.contrib import admin
from .models import *
from django.contrib import messages
from .forms import *

class AllProductsAdmin(admin.ModelAdmin):
    actions = ['rendre_disponible', 'rendre_indisponible']
    list_display = ('nom','categorie','disponible', 'type', 'ornement', 'prix')
    search_fields = ['nom','categorie', 'type']
    list_filter = ['categorie', 'disponible']

    def rendre_disponible(self,  request, queryset):
        queryset.update(disponible=True)

    def rendre_indisponible(self, request, queryset):
        queryset.update(disponible=False)
    

    def on_save_model(self, request, obj, form, change):
        super().on_save_model(request, obj, form, change)  # Appeler la méthode parente
        forms.update_type(self)

    
admin.site.register(AllProducts, AllProductsAdmin)