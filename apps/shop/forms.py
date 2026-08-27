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
        fields = ['name', 'category', 'price', 'compare_price', 'description', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'product_name_input',
                'placeholder': 'Ex: Robe Saharienne Chic',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 outline-none text-xs sm:text-sm font-medium',
                'required': True,
            }),
            'category': forms.TextInput(attrs={
                'id': 'product_category_input',
                'placeholder': 'Ex: Robes, Chaussures, Mèches...',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 outline-none text-xs sm:text-sm font-medium',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Prix de vente (FCFA)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 outline-none text-xs sm:text-sm font-bold',
                'min': '0',
                'step': '1',
                'required': True,
            }),
            'compare_price': forms.NumberInput(attrs={
                'placeholder': 'Prix barré / Promo (Optionnel)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 outline-none text-xs sm:text-sm font-medium',
                'min': '0',
                'step': '1',
            }),
            'description': forms.Textarea(attrs={
                'id': 'product_desc_input',
                'placeholder': 'Décrivez les caractéristiques de l\'article ou cliquez sur le bouton Azoria AI pour rédiger...',
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 outline-none text-xs leading-relaxed',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-xs text-slate-500 file:mr-3 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-colors',
                'accept': 'image/*',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded text-brand-600 focus:ring-brand-500 border-slate-300',
            }),
        }
        labels = {
            'name': 'Nom de l\'article',
            'category': 'Catégorie',
            'price': 'Prix de vente (FCFA)',
            'compare_price': 'Prix barré / Promo (Optionnel)',
            'description': 'Description détaillée',
            'image': 'Photo de l\'article',
            'is_available': 'Disponible immédiatement',
        }
