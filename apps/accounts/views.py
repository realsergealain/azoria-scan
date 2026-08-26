from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import LoginForm, RegisterForm


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
            login(request, user)
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
