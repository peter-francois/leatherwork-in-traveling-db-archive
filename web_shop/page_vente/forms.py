from django import forms

class ProductFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Recherche", widget=forms.TextInput(attrs={'placeholder': 'Rechercher...'}))
    category = forms.CharField(required=False, label="Catégorie", widget=forms.TextInput(attrs={'placeholder': 'Catégorie'}))
    min_price = forms.DecimalField(required=False, label="Prix min", min_value=0)
    max_price = forms.DecimalField(required=False, label="Prix max", min_value=0)