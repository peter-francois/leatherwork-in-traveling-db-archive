from django import forms
from .models import *




class ProductFilterForm(forms.Form):
    
    search = forms.CharField(required=False, label="Recherche", widget=forms.TextInput(attrs={'placeholder': 'Rechercher...', 'id': 'search_field'}))
    type = forms.CharField(required=False, label="Type", widget=forms.Select(choices= [('---', '---')]))
    min_price = forms.DecimalField(required=False, label="Prix min", min_value=0)
    max_price = forms.DecimalField(required=False, label="Prix max", min_value=0)
    
    def __init__(self, *args, **kwargs):
        categorie = kwargs.pop('categorie', None)  # Récupérer la catégorie depuis les arguments
        super().__init__(*args, **kwargs)
        # update_type(self)
        # self.fields['type'].widget.choices = [('---', '---')] + [(type, type) for type in AllProducts.objects.values_list('type', flat=True).distinct()]
        # Si une catégorie est fournie, filtrer les types disponibles
        if categorie:
            types = AllProducts.objects.filter(categorie=categorie).values_list('type', flat=True).distinct()
            self.fields['type'].widget.choices = [('---', '---')] +[(t, t) for t in types]  # Mettre à jour les choix
        else:
            self.fields['type'].widget.choices = [('---', '---')] + [(type, type) for type in AllProducts.objects.values_list('type', flat=True).distinct()]



# def update_type(self):
#     types = AllProducts.objects.values_list('type', flat=True).distinct()
#     self.fields['type'].choices = [('---', '---')] + [(type, type) for type in types]