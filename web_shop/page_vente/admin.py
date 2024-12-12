from django.contrib import admin
from .models import *


class MaroquinerieAdmin(admin.ModelAdmin):
    actions = ['rendre_disponible', 'rendre_indisponible']
    list_display = ('nom', 'disponible', 'type', 'ornement', 'prix')
    search_fields = ['nom', 'type']

    def rendre_disponible(self,  request, queryset):
        queryset.update(disponible=True)

    def rendre_indisponible(self, request, queryset):
        queryset.update(disponible=False)



class MacrameAdmin(admin.ModelAdmin):
    actions = ['rendre_disponible', 'rendre_indisponible']
    list_display = ('nom', 'disponible', 'type', 'ornement', 'prix')
    search_fields = ['nom','type']
    def rendre_disponible(self,  request, queryset):
        queryset.update(disponible=True)

    def rendre_indisponible(self, request, queryset):
        queryset.update(disponible=False)

class TogetherAdmin(admin.ModelAdmin):
    actions = ['rendre_disponible', 'rendre_indisponible']
    list_display = ('nom', 'disponible', 'type', 'ornement', 'prix')
    search_fields = ['nom','type']
    def rendre_disponible(self,  request, queryset):
        queryset.update(disponible=True)

    def rendre_indisponible(self, request, queryset):
        queryset.update(disponible=False)


admin.site.register(Macrame, MacrameAdmin)
admin.site.register(Maroquinerie, MaroquinerieAdmin)
admin.site.register(Together, TogetherAdmin)





# Register your models here.
