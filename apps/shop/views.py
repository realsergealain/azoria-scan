from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse

from .forms import ShopCreateForm, ShopProductForm
from .models import Shop, ShopBranding, ShopPayment, ShopProduct, VisitTracker
from .services import generate_styled_qr_code


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


def shop_detail(request, shop_uuid, shop_slug):
    """Vue de détail d'une boutique (stub — à enrichir ultérieurement)."""
    # Ici, nous permettons l'accès public. La vue est censée être publique pour les acheteurs !
    # Retrait du `login_required` dans un vrai contexte public, mais laissons-le si c'est pour l'admin.
    # Attendez, `shop_detail` devrait être public si c'est la boutique.
    shop = get_object_or_404(Shop, uuid=shop_uuid, slug=shop_slug)
    
    # Tracking
    source = 'qr' if request.GET.get('ref') == 'qr' else 'direct'
    VisitTracker.objects.create(shop=shop, source=source)
    
    return render(request, 'shop/detail.html', {'shop': shop})

def shop_qr_code(request, shop_uuid):
    """Sert l'image du QR code de la boutique."""
    shop = get_object_or_404(Shop, uuid=shop_uuid)
    # L'URL absolue de la boutique
    url = request.build_absolute_uri(f"/boutique/{shop.uuid}/{shop.slug}/?ref=qr")
    
    # Couleur de la marque ou par défaut
    color = shop.branding.primary_color if hasattr(shop, 'branding') else '#7C3AED'
    
    buffer = generate_styled_qr_code(url, color_hex=color)
    return HttpResponse(buffer, content_type="image/png")

def product_qr_code(request, product_uuid):
    """Sert l'image du QR code d'un produit."""
    product = get_object_or_404(ShopProduct, uuid=product_uuid)
    # Dans un vrai cas, on lierait vers une page de détail produit. Ici on pointe vers la boutique avec une ancre.
    url = request.build_absolute_uri(f"/boutique/{product.shop.uuid}/{product.shop.slug}/?product={product.uuid}&ref=qr")
    
    color = product.shop.branding.primary_color if hasattr(product.shop, 'branding') else '#7C3AED'
    
    buffer = generate_styled_qr_code(url, color_hex=color)
    return HttpResponse(buffer, content_type="image/png")


@login_required
def product_list(request):
    """Affiche la liste des produits pour la boutique principale du vendeur."""
    # MVP: on prend la première boutique du vendeur
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        messages.warning(request, "Veuillez d'abord créer une boutique.")
        return redirect('core:dashboard')
        
    products = ShopProduct.objects.filter(shop=shop).order_by('-created_at')
    
    return render(request, 'shop/product_list.html', {
        'shop': shop,
        'products': products,
    })

@login_required
def product_create(request):
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            messages.success(request, f"Produit '{product.name}' ajouté avec succès.")
            if request.headers.get('HX-Request') == 'true':
                return redirect('shop:product_list')
            return redirect('shop:product_list')
    else:
        form = ShopProductForm()

    template = 'shop/partials/product_form_modal.html' if request.headers.get('HX-Request') == 'true' else 'shop/product_form.html'
    return render(request, template, {
        'form': form,
        'shop': shop,
        'is_update': False
    })

@login_required
def product_update(request, product_uuid):
    product = get_object_or_404(ShopProduct, uuid=product_uuid, shop__owner=request.user)
    
    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Produit '{product.name}' mis à jour.")
            if request.headers.get('HX-Request') == 'true':
                return redirect('shop:product_list')
            return redirect('shop:product_list')
    else:
        form = ShopProductForm(instance=product)

    template = 'shop/partials/product_form_modal.html' if request.headers.get('HX-Request') == 'true' else 'shop/product_form.html'
    return render(request, template, {
        'form': form,
        'product': product,
        'is_update': True
    })

@login_required
def product_delete(request, product_uuid):
    product = get_object_or_404(ShopProduct, uuid=product_uuid, shop__owner=request.user)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Produit '{name}' supprimé.")
        if request.headers.get('HX-Request') == 'true':
            return redirect('shop:product_list')
        return redirect('shop:product_list')
    
    template = 'shop/partials/product_delete_modal.html' if request.headers.get('HX-Request') == 'true' else 'shop/product_confirm_delete.html'
    return render(request, template, {'product': product})
