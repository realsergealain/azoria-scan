from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import LoginForm, RegisterForm, UserProfileForm


def login_view(request):
    """
    Vue de connexion vendeur.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    next_url = request.GET.get('next', 'core:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Gestion de la session "Se souvenir de moi"
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Expire à la fermeture du navigateur
            else:
                request.session.set_expiry(1209600)  # 2 semaines

            messages.success(request, _(f"Bienvenue {user.full_name} ! Vous êtes connecté."))
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'next': next_url,
    })


def register_view(request):
    """
    Vue d'inscription vendeur.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, _(f"Félicitations {user.full_name} ! Votre compte Azoria a été créé avec succès."))
            return redirect('shop:create')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form,
    })


def logout_view(request):
    """
    Vue de déconnexion.
    """
    logout(request)
    messages.info(request, _("Vous avez été déconnecté avec succès."))
    return redirect('accounts:login')


@login_required
def profile_settings_view(request):
    """
    Vue de gestion du profil utilisateur et des paramètres de sécurité (mot de passe).
    """
    user = request.user
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            password_form = PasswordChangeForm(user=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, _("Vos informations personnelles ont été mises à jour."))
                return redirect('accounts:settings')
        elif 'change_password' in request.POST:
            profile_form = UserProfileForm(instance=user)
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Empêche la déconnexion
                messages.success(request, _("Votre mot de passe a été modifié avec succès."))
                return redirect('accounts:settings')
    else:
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    return render(request, 'accounts/settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
