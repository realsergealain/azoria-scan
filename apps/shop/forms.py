from django import forms
from .models import Shop, ShopPayment


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
