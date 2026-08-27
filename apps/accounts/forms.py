from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginForm(forms.Form):
    """
    Formulaire de connexion basé sur l'adresse email.
    """
    email = forms.EmailField(
        label=_("Adresse email"),
        widget=forms.EmailInput(attrs={
            'placeholder': 'votre.email@exemple.com',
            'class': 'md-input',
            'autocomplete': 'email',
            'required': True,
        })
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Votre mot de passe',
            'class': 'md-input',
            'autocomplete': 'current-password',
            'required': True,
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'md-checkbox',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise ValidationError(
                    _("Identifiants incorrects. Veuillez vérifier votre adresse email et mot de passe."),
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise ValidationError(
                    _("Ce compte a été désactivé."),
                    code='inactive',
                )
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)


class RegisterForm(forms.Form):
    """
    Formulaire d'inscription vendeur pour Azoria.
    """
    full_name = forms.CharField(
        label=_("Nom complet"),
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Aïcha Kouamé',
            'class': 'md-input',
            'autocomplete': 'name',
            'required': True,
        })
    )
    email = forms.EmailField(
        label=_("Adresse email"),
        widget=forms.EmailInput(attrs={
            'placeholder': 'aicha@boutique.com',
            'class': 'md-input',
            'autocomplete': 'email',
            'required': True,
        })
    )
    phone = forms.CharField(
        label=_("Numéro WhatsApp / Téléphone"),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+225 07 00 00 00 00',
            'class': 'md-input',
            'autocomplete': 'tel',
        })
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Minimum 8 caractères',
            'class': 'md-input',
            'autocomplete': 'new-password',
            'required': True,
        })
    )
    password_confirm = forms.CharField(
        label=_("Confirmer le mot de passe"),
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Répétez votre mot de passe',
            'class': 'md-input',
            'autocomplete': 'new-password',
            'required': True,
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Une boutique ou un compte existe déjà avec cette adresse email."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', _("Les mots de passe ne correspondent pas."))
        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        names = cleaned_data['full_name'].strip().split(' ', 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

        user = User.objects.create_user(
            email=cleaned_data['email'],
            password=cleaned_data['password'],
            first_name=first_name,
            last_name=last_name,
            phone=cleaned_data.get('phone', ''),
        )
        return user


class UserProfileForm(forms.ModelForm):
    """
    Formulaire pour la mise à jour du profil utilisateur.
    L'email est inclus en lecture seule car l'utilisateur ne doit pas pouvoir le modifier.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'md-input', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'md-input', 'placeholder': 'Nom'}),
            'phone': forms.TextInput(attrs={'class': 'md-input', 'placeholder': '+225 07 00 00 00 00'}),
            'email': forms.EmailInput(attrs={'class': 'md-input bg-slate-100 text-slate-500 cursor-not-allowed', 'readonly': 'readonly'}),
        }
        labels = {
            'first_name': _("Prénom"),
            'last_name': _("Nom"),
            'phone': _("Numéro WhatsApp / Téléphone"),
            'email': _("Adresse email (non modifiable)"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # S'assurer que l'email ne peut pas être soumis
        self.fields['email'].disabled = True
