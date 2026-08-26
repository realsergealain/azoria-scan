from django import forms
from .models import Shop, ShopBranding, ShopPayment, ShopProduct

class ShopBasicInfoForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Nom de votre boutique'}),
            'description': forms.Textarea(attrs={'class': 'auth-input', 'rows': 3, 'placeholder': 'Description (facultative)'}),
        }

class ShopBrandingForm(forms.ModelForm):
    class Meta:
        model = ShopBranding
        fields = ['logo', 'primary_color']
        widgets = {
            'logo': forms.ClearableFileInput(attrs={'class': 'auth-input'}),
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'auth-input'}),
        }

class ShopPaymentForm(forms.ModelForm):
    class Meta:
        model = ShopPayment
        fields = ['gateway', 'api_key']
        widgets = {
            'gateway': forms.Select(attrs={'class': 'auth-input'}),
            'api_key': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Clé API (si nécessaire)'}),
        }

class ShopProductImportForm(forms.Form):
    csv_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'auth-input'}))
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Nom du produit'}))
    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'auth-input'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'auth-input'}))
