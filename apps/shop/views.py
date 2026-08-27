from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ShopCreateForm
from .models import Shop, ShopBranding, ShopPayment


@login_required
def shop_create(request):
    """Vue simple de création de boutique — 1 seul formulaire, pas de wizard."""
    form = ShopCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Création de la boutique
        shop = Shop.objects.create(
            owner=request.user,
            name=form.cleaned_data['name'],
            description=form.cleaned_data.get('description', ''),
        )

        # Branding par défaut (logo vide, couleur violette Azoria)
        ShopBranding.objects.create(shop=shop, primary_color='#7C3AED')

        # Paiement avec les modes choisis
        ShopPayment.objects.create(
            shop=shop,
            accepted_payments=form.cleaned_data['accepted_payments'],
        )

        messages.success(request, f'🎉 Boutique « {shop.name} » créée avec succès !')
        return redirect('core:dashboard')

    return render(request, 'shop/create.html', {'form': form})


@login_required
def shop_detail(request, shop_uuid, shop_slug):
    """Vue de détail d'une boutique (stub — à enrichir ultérieurement)."""
    shop = get_object_or_404(Shop, uuid=shop_uuid, slug=shop_slug, owner=request.user)
    return render(request, 'shop/detail.html', {'shop': shop})
