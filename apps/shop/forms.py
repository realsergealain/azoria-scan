from django import forms
from .models import Shop, ShopPayment, ShopProduct


class ShopCreateForm(forms.Form):
    """Formulaire enrichi de création de boutique."""

    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex : Fatou Fashion Chic ✨',
            'autocomplete': 'off',
            'class': 'w-full px-4 py-3 rounded-2xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-sm transition-all outline-none font-bold',
        }),
        label='Nom de votre boutique',
        error_messages={'required': 'Le nom de la boutique est obligatoire.'},
    )

    category = forms.CharField(
        required=False,
        initial='Mode & Habillement',
        max_length=80,
    )

    phone = forms.CharField(
        required=False,
        max_length=25,
    )

    city = forms.CharField(
        required=False,
        initial='Cocody',
        max_length=80,
    )

    description = forms.CharField(
        required=False,
        max_length=400,
        widget=forms.Textarea(attrs={
            'placeholder': 'Décrivez brièvement vos articles et votre univers… (optionnel)',
            'rows': 2,
            'class': 'w-full px-4 py-3 rounded-2xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-sm transition-all outline-none resize-none',
        }),
        label='Description (facultative)',
    )

    primary_color = forms.CharField(
        required=False,
        initial='#7C3AED',
        max_length=7,
    )

    delivery_fee = forms.DecimalField(
        required=False,
        initial=1500,
        max_digits=10,
        decimal_places=2,
    )

    accepted_payments = forms.MultipleChoiceField(
        choices=ShopPayment.GATEWAY_CHOICES,
        initial=['livraison', 'mobile_money'],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class ShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['name', 'category', 'price', 'compare_price', 'stock', 'track_stock', 'description', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'product_name_input',
                'placeholder': 'Ex: Robe Saharienne Chic',
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm font-medium transition-all shadow-sm',
                'required': True,
            }),
            'category': forms.TextInput(attrs={
                'id': 'product_category_input',
                'placeholder': 'Ex: Robes, Chaussures, Mèches...',
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm font-medium transition-all shadow-sm',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Prix de vente (FCFA)',
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm font-bold transition-all shadow-sm',
                'min': '100',
                'step': '1',
                'required': True,
            }),
            'compare_price': forms.NumberInput(attrs={
                'placeholder': 'Prix barré / Promo (Optionnel)',
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm font-medium transition-all shadow-sm',
                'min': '0',
                'step': '1',
            }),
            'stock': forms.NumberInput(attrs={
                'placeholder': 'Ex: 25',
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm font-bold transition-all shadow-sm',
                'min': '0',
                'step': '1',
            }),
            'track_stock': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded-lg text-brand-600 focus:ring-brand-500 border-slate-300 dark:border-slate-600 transition-colors',
            }),
            'description': forms.Textarea(attrs={
                'id': 'product_desc_input',
                'placeholder': 'Décrivez les caractéristiques de l\'article ou cliquez sur le bouton Azoria AI pour rédiger...',
                'rows': 3,
                'class': 'w-full px-4 py-3 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-xs sm:text-sm leading-relaxed transition-all shadow-sm resize-none',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-xs text-slate-500 file:mr-3 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-all cursor-pointer',
                'accept': 'image/*',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded-lg text-brand-600 focus:ring-brand-500 border-slate-300 dark:border-slate-600 transition-colors',
            }),
        }
        labels = {
            'name': 'Nom de l\'article',
            'category': 'Catégorie',
            'price': 'Prix de vente (FCFA)',
            'compare_price': 'Prix barré / Promo (Optionnel)',
            'stock': 'Quantité en stock',
            'track_stock': 'Gérer et décompter le stock automatiquement',
            'description': 'Description détaillée',
            'image': 'Photo principale',
            'is_available': 'Article actif & disponible',
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Le prix de vente doit être strictement supérieur à 0.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("La quantité en stock ne peut pas être négative.")
        return stock or 0

