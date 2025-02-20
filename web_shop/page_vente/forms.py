from django import forms
from .models import *




class ProductFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_type(self)
        self.fields['type'].widget.choices = [('---', '---')] + [(type, type) for type in AllProducts.objects.values_list('type', flat=True).distinct()]

    search = forms.CharField(required=False, label="Recherche", widget=forms.TextInput(attrs={'placeholder': 'Rechercher...'}))
    type = forms.CharField(required=False, label="Type", widget=forms.Select(choices= [('---', '---')]))
    min_price = forms.DecimalField(required=False, label="Prix min", min_value=0)
    max_price = forms.DecimalField(required=False, label="Prix max", min_value=0)

def update_type(self):
    types = AllProducts.objects.values_list('type', flat=True).distinct()
    self.fields['type'].choices = [('---', '---')] + [(type, type) for type in types]