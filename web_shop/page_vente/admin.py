from django.contrib import admin
from .models import *
from django.contrib import messages

class AllProductsAdmin(admin.ModelAdmin):
    actions = ['rendre_disponible', 'rendre_indisponible']
    list_display = ('nom','categorie','disponible', 'type', 'ornement', 'prix')
    search_fields = ['nom','categorie', 'type']
    list_filter = ['categorie', 'disponible']

    def rendre_disponible(self,  request, queryset):
        queryset.update(disponible=True)

    def rendre_indisponible(self, request, queryset):
        queryset.update(disponible=False)
    
    def lien_image_check(self, request, queryset, link):
        if not link:
            return None
        if not ("https://dl.dropboxusercontent.com" in link or "www.dropbox.com" in link) :
            messages.error(request,"Le lien de l'image est incorrect.")
            return None
        return link
        
    def save_model(self, request, obj, form, change):
        links = [obj.lien_image1, obj.lien_image2, obj.lien_image3, obj.lien_image4]
        link_fields = ['lien_image1', 'lien_image2', 'lien_image3', 'lien_image4']
        validated_links = [self.lien_image_check(request, obj, link) for link in links]
        
        for link_field, validated_link in zip(link_fields, validated_links):
            setattr(obj, link_field, validated_link if validated_link is not None else None)
        
        super().save_model(request, obj, form, change)
    
admin.site.register(AllProducts, AllProductsAdmin)