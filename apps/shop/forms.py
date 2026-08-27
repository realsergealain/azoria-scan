from django import forms
from .models import Shop, ShopPayment, ShopProduct


class ShopCreateForm(forms.Form):
    """Formulaire simplifié de création de boutique en une seule étape."""

    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex : Boutique de Fatou ✨',
            'autocomplete': 'off',
            'autofocus': True,
        }),
        label='Nom de votre boutique',
        error_messages={'required': 'Le nom de la boutique est obligatoire.'},
    )

    description = forms.CharField(
        required=False,
        max_length=400,
        widget=forms.Textarea(attrs={
            'placeholder': 'Décrivez brièvement ce que vous vendez… (optionnel)',
            'rows': 3,
        }),
        label='Description (facultative)',
    )

    accepted_payments = forms.MultipleChoiceField(
        choices=ShopPayment.GATEWAY_CHOICES,
        initial=['livraison'],
        widget=forms.CheckboxSelectMultiple,
        label='Moyens de paiement acceptés',
        error_messages={'required': 'Veuillez sélectionner au moins un moyen de paiement.'},
    )

class ShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['name', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Robe de soirée rouge',
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all',
                'required': True,
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Prix en FCFA',
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all',
                'min': '0',
                'step': '1',
                'required': True,
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-colors',
                'accept': 'image/*',
            }),
        }
        labels = {
            'name': 'Nom du produit',
            'price': 'Prix',
            'image': 'Image du produit',
        }
