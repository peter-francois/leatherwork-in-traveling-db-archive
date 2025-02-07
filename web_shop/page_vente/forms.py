from django import forms
from .models import *


types = AllProducts.objects.values_list('type', flat=True).distinct()

class ProductFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Recherche", widget=forms.TextInput(attrs={'placeholder': 'Rechercher...'}))
    type = forms.CharField(required=False, label="Type", widget=forms.Select(choices= [('---', '---')]+ [(type, type) for type in types]))
    min_price = forms.DecimalField(required=False, label="Prix min", min_value=0)
    max_price = forms.DecimalField(required=False, label="Prix max", min_value=0)