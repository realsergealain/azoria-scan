import json
from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count

from .forms import ShopCreateForm, ShopProductForm
from .models import Shop, ShopBranding, ShopPayment, ShopProduct, Order, OrderItem, VisitTracker, Notification, ProductImage
from .services import (
    generate_styled_qr_code,
    generate_styled_qr_card,
    generate_whatsapp_order_link,
    generate_ai_product_description,
    get_shop_dashboard_analytics
)
from .services_push import send_order_web_push


# ==========================================
# 🏪 GESTION DES BOUTIQUES
# ==========================================

@login_required
def shop_create(request):
    """Création de boutique (modal ou page dédiée)."""
    if Shop.objects.filter(owner=request.user).exists():
        messages.error(request, "Vous possédez déjà une boutique. La création de boutiques multiples n'est pas autorisée.")
        return redirect('core:dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, "Le nom de la boutique est obligatoire.")
            return redirect('core:dashboard')

        category = request.POST.get('category', 'Mode & Habillement')
        description = request.POST.get('description', '')
        
        # Numéro WhatsApp
        raw_phone = request.POST.get('phone', '')
        if raw_phone:
            clean_digits = ''.join(filter(str.isdigit, str(raw_phone)))
            if str(raw_phone).strip().startswith('+'):
                phone = '+' + clean_digits
            elif len(clean_digits) == 10 and not clean_digits.startswith('225'):
                phone = '+225' + clean_digits
            elif clean_digits.startswith('225'):
                phone = '+' + clean_digits
            elif clean_digits.startswith('221') or clean_digits.startswith('223') or clean_digits.startswith('226') or clean_digits.startswith('229') or clean_digits.startswith('228') or clean_digits.startswith('224') or clean_digits.startswith('227'):
                phone = '+' + clean_digits
            else:
                phone = clean_digits
        else:
            phone = getattr(request.user, 'phone', '') or ''

        raw_city = request.POST.get('city', 'Abidjan')
        raw_zone = request.POST.get('zone', '')
        city = f"{raw_zone}, {raw_city}" if (raw_zone and raw_zone not in raw_city) else raw_city

        primary_color = request.POST.get('primary_color', '#7C3AED')
        
        try:
            raw_fee = request.POST.get('delivery_fee', '1500')
            delivery_fee = Decimal(str(raw_fee).replace(' ', '').replace('FCFA', ''))
        except Exception:
            delivery_fee = Decimal('1500')

        accepted_payments = request.POST.getlist('accepted_payments') or ['livraison', 'mobile_money']

        shop = Shop.objects.create(
            owner=request.user,
            name=name,
            category=category,
            description=description,
            phone=phone,
            city=city,
        )

        branding = ShopBranding.objects.create(
            shop=shop,
            primary_color=primary_color,
        )
        if 'logo' in request.FILES:
            branding.logo = request.FILES['logo']
            branding.save()

        ShopPayment.objects.create(
            shop=shop,
            accepted_payments=accepted_payments,
            delivery_fee=delivery_fee,
        )

        messages.success(request, f'🎉 Félicitations ! Votre boutique « {shop.name} » est prête à vendre !')
        return redirect('core:dashboard')

    form = ShopCreateForm()
    return render(request, 'shop/create.html', {'form': form})


@login_required
def shop_settings(request):
    """Page de configuration et branding de la boutique (Mes Boutiques)."""
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        messages.warning(request, "Veuillez d'abord créer une boutique.")
        return redirect('core:dashboard')

    branding, _ = ShopBranding.objects.get_or_create(shop=shop)
    payment, _ = ShopPayment.objects.get_or_create(shop=shop)

    if request.method == 'POST':
        # Règle métier : Modification du nom possible tous les 7 jours
        new_name = request.POST.get('name', '').strip()
        if new_name and new_name != shop.name:
            if shop.is_name_locked:
                messages.warning(request, f"🔒 Le nom de la boutique a été modifié récemment. Vous devez attendre encore {shop.name_unlock_days_left} jour(s) avant de pouvoir le modifier à nouveau.")
            else:
                from django.utils import timezone
                shop.name = new_name
                shop.name_last_changed_at = timezone.now()
                messages.info(request, "Nom de la boutique mis à jour avec succès. La prochaine modification sera possible dans 7 jours.")

        shop.category = request.POST.get('category', shop.category)
        shop.description = request.POST.get('description', shop.description)
        
        # Phone cleaning
        raw_phone = request.POST.get('phone', '')
        if raw_phone:
            clean_digits = ''.join(filter(str.isdigit, str(raw_phone)))
            if str(raw_phone).strip().startswith('+'):
                shop.phone = '+' + clean_digits
            elif len(clean_digits) == 10 and not clean_digits.startswith('225'):
                shop.phone = '+225' + clean_digits
            elif clean_digits.startswith('225') or clean_digits.startswith('221') or clean_digits.startswith('223') or clean_digits.startswith('226') or clean_digits.startswith('229') or clean_digits.startswith('228') or clean_digits.startswith('224') or clean_digits.startswith('227'):
                shop.phone = '+' + clean_digits
            else:
                shop.phone = clean_digits

        raw_city = request.POST.get('city', shop.city)
        raw_zone = request.POST.get('zone', '')
        shop.city = f"{raw_zone}, {raw_city}" if (raw_zone and raw_zone not in raw_city) else raw_city
        shop.save()

        # Branding
        primary_color = request.POST.get('primary_color_text') or request.POST.get('primary_color', branding.primary_color)
        branding.primary_color = primary_color
        if 'logo' in request.FILES:
            branding.logo = request.FILES['logo']
        branding.save()

        # Logistique & Paiements
        if request.POST.get('delivery_fee'):
            payment.delivery_fee = Decimal(request.POST.get('delivery_fee'))
        if request.POST.get('free_delivery_threshold'):
            payment.free_delivery_threshold = Decimal(request.POST.get('free_delivery_threshold'))
        payment.save()

        messages.success(request, "Paramètres de la boutique enregistrés avec succès.")
        return redirect('shop:settings')

    return render(request, 'shop/store_settings.html', {
        'shop': shop,
        'branding': branding,
        'payment': payment,
    })


@login_required
def ai_description_api(request):
    """
    API & HTMX Endpoint pour générer une description via OpenAI (Vision & Fallback textuel).
    Supporte l'upload d'image (Scénario A Vision) et le titre uniquement (Scénario B).
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '') or request.POST.get('cat', '')
        image_file = request.FILES.get('image')
    else:
        name = request.GET.get('name', '').strip()
        category = request.GET.get('cat', '')
        image_file = None

    if not name and not image_file:
        description = "Veuillez saisir un nom d'article ou ajouter une image."
    else:
        ai_data = generate_styled_description_from_ai(name=name, category=category, image_file=image_file)
        description = ai_data.get('description', '')

    # Si la requête est émise par HTMX et cible le textarea de description
    if request.htmx and (request.htmx.target == 'product_desc_input' or request.headers.get('HX-Target') == 'product_desc_input'):
        html_fragment = f'''<textarea id="product_desc_input" name="description" rows="4" 
            placeholder="Décrivez les caractéristiques de l'article ou cliquez sur le bouton Azoria AI pour rédiger..." 
            class="w-full px-4 py-3 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-xs sm:text-sm leading-relaxed transition-all shadow-sm resize-none">{description}</textarea>'''
        return HttpResponse(html_fragment, content_type='text/html')

    return JsonResponse({'description': description})


def generate_styled_description_from_ai(name: str, category: str = "", image_file=None) -> dict:
    return generate_ai_product_description(name=name, category=category, image_file=image_file)


# ==========================================
# 🛒 GESTION DU CATALOGUE PRODUITS
# ==========================================
from .models import ProductImage

@login_required
def product_list(request):
    """Liste des produits du vendeur."""
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
    """Ajout d'un nouveau produit (Supporte HTMX modal)."""
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()

            # Save additional images
            for image in request.FILES.getlist('additional_images'):
                if product.images.count() < 3:
                    ProductImage.objects.create(product=product, image=image)

            messages.success(request, f"Produit '{product.name}' ajouté avec succès.")
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
    """Modification d'un produit (Supporte HTMX modal)."""
    product = get_object_or_404(ShopProduct, uuid=product_uuid, shop__owner=request.user)
    
    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            
            # Delete selected existing images (if any feature sends image IDs to delete)
            # For now, we just append new images up to 3 limit
            for image in request.FILES.getlist('additional_images'):
                if product.images.count() < 3:
                    ProductImage.objects.create(product=product, image=image)

            messages.success(request, f"Produit '{product.name}' modifié avec succès.")
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
    """Suppression d'un produit."""
    product = get_object_or_404(ShopProduct, uuid=product_uuid, shop__owner=request.user)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Produit '{name}' supprimé.")
        return redirect('shop:product_list')
    
    template = 'shop/partials/product_delete_modal.html' if request.headers.get('HX-Request') == 'true' else 'shop/product_confirm_delete.html'
    return render(request, template, {'product': product})


def ai_description_api(request):
    """API endpoint pour le bouton Azoria AI."""
    name = request.GET.get('name', '')
    cat = request.GET.get('cat', '')
    if not name:
        return JsonResponse({'error': 'Nom requis'}, status=400)
    data = generate_ai_product_description(name, cat)
    return JsonResponse(data)


# ==========================================
# 📦 GESTION DES COMMANDES & CLIENTS
# ==========================================

@login_required
def order_list(request):
    """Gestion des commandes pour le vendeur avec onglets de statut."""
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        messages.warning(request, "Veuillez d'abord créer une boutique.")
        return redirect('core:dashboard')

    status_filter = request.GET.get('status', '')
    all_orders = Order.objects.filter(shop=shop)
    
    # Counts
    all_count = all_orders.count()
    pending_count = all_orders.filter(status='pending').count()
    confirmed_count = all_orders.filter(status='confirmed').count()
    shipped_count = all_orders.filter(status='shipped').count()
    delivered_count = all_orders.filter(status='delivered').count()
    cancelled_count = all_orders.filter(status='cancelled').count()

    if status_filter:
        orders = all_orders.filter(status=status_filter)
    else:
        orders = all_orders

    return render(request, 'shop/order_list.html', {
        'shop': shop,
        'orders': orders,
        'status_filter': status_filter,
        'all_count': all_count,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
        'cancelled_count': cancelled_count,
    })


@login_required
@require_POST
def order_status_update(request, order_uuid):
    """Mise à jour du statut d'une commande via HTMX."""
    order = get_object_or_404(Order, uuid=order_uuid, shop__owner=request.user)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
    
    # Renvoyer la carte commande mise à jour
    return render(request, 'shop/partials/order_card.html', {'order': order, 'shop': order.shop})


@login_required
def customer_list(request):
    """Répertoire CRM des clients généré à partir des commandes."""
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return redirect('core:dashboard')

    # Agrégation des clients par numéro de téléphone
    orders = Order.objects.filter(shop=shop)
    customers_map = {}

    for o in orders:
        phone = o.customer_phone
        if phone not in customers_map:
            customers_map[phone] = {
                'name': o.customer_name,
                'phone': o.customer_phone,
                'city': o.customer_city,
                'order_count': 0,
                'total_spent': Decimal('0.00'),
            }
        customers_map[phone]['order_count'] += 1
        if o.status in ['confirmed', 'shipped', 'delivered']:
            customers_map[phone]['total_spent'] += o.total_amount

    customers = list(customers_map.values())
    return render(request, 'shop/customer_list.html', {
        'shop': shop,
        'customers': customers
    })


# ==========================================
# 🎨 STUDIO QR CODES & MARKETING
# ==========================================

@login_required
def qr_studio(request):
    """Studio interactif de QR codes & analytics."""
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return redirect('core:dashboard')

    products = ShopProduct.objects.filter(shop=shop, is_available=True)
    analytics = get_shop_dashboard_analytics(shop)

    return render(request, 'shop/qr_studio.html', {
        'shop': shop,
        'products': products,
        'analytics': analytics,
    })


def shop_qr_code(request, shop_uuid):
    """Génère et sert l'image PNG HD du QR code de la boutique."""
    shop = get_object_or_404(Shop, uuid=shop_uuid)
    url = request.build_absolute_uri(f"/boutique/{shop.uuid}/{shop.slug}/?ref=qr")
    color = shop.branding.primary_color if (hasattr(shop, 'branding') and shop.branding and shop.branding.primary_color) else '#7C3AED'
    logo_file = shop.branding.logo if (hasattr(shop, 'branding') and shop.branding and shop.branding.logo) else None
    
    transparent = request.GET.get('transparent') == 'true'
    show_frame = request.GET.get('frame') != 'false'
    include_name = request.GET.get('name') != 'false'
    is_card = request.GET.get('card') == 'true'

    if is_card:
        buffer = generate_styled_qr_card(
            url, 
            color_hex=color, 
            logo_image=logo_file, 
            shop_name=shop.name if include_name else None,
            show_frame=show_frame,
            transparent=transparent
        )
    else:
        buffer = generate_styled_qr_code(
            url, 
            color_hex=color, 
            logo_image=logo_file, 
            transparent=transparent
        )
    
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    filename = f"qr_card_{shop.slug}.png" if is_card else f"qr_{shop.slug}.png"
    if request.GET.get('download') == 'true':
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    else:
        response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


def product_qr_code(request, product_uuid):
    """Génère et sert l'image PNG HD du QR code d'un produit."""
    product = get_object_or_404(ShopProduct, uuid=product_uuid)
    url = request.build_absolute_uri(f"/boutique/{product.shop.uuid}/{product.shop.slug}/?product={product.uuid}&ref=qr")
    color = product.shop.branding.primary_color if (hasattr(product.shop, 'branding') and product.shop.branding and product.shop.branding.primary_color) else '#7C3AED'
    logo_file = product.shop.branding.logo if (hasattr(product.shop, 'branding') and product.shop.branding and product.shop.branding.logo) else None
    
    transparent = request.GET.get('transparent') == 'true'
    show_frame = request.GET.get('frame') != 'false'
    include_name = request.GET.get('name') != 'false'
    is_card = request.GET.get('card') == 'true'

    if is_card:
        buffer = generate_styled_qr_card(
            url, 
            color_hex=color, 
            logo_image=logo_file, 
            shop_name=f"{product.name} — {product.shop.name}" if include_name else None,
            show_frame=show_frame,
            transparent=transparent
        )
    else:
        buffer = generate_styled_qr_code(
            url, 
            color_hex=color, 
            logo_image=logo_file, 
            transparent=transparent
        )
    
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    filename = f"qr_card_produit_{product.slug}.png" if is_card else f"qr_produit_{product.slug}.png"
    if request.GET.get('download') == 'true':
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    else:
        response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


# ==========================================
# 📱 VITRINE PUBLIQUE & TUNNEL DE COMMANDE
# ==========================================

def shop_detail(request, shop_uuid, shop_slug):
    """Vitrine publique 100% Mobile-First."""
    shop = get_object_or_404(Shop, uuid=shop_uuid, slug=shop_slug, is_active=True)
    
    # Tracking de la visite
    source = request.GET.get('ref', 'direct')
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    VisitTracker.objects.create(
        shop=shop,
        source=source if source in dict(VisitTracker.SOURCE_CHOICES) else 'direct',
        ip_address=client_ip.split(',')[0] if client_ip else None
    )

    products = ShopProduct.objects.filter(shop=shop, is_available=True).prefetch_related('images')
    categories = list(set([p.category for p in products if p.category]))

    return render(request, 'shop/storefront.html', {
        'shop': shop,
        'products': products,
        'categories': categories,
    })


@require_POST
def checkout_view(request, shop_uuid, shop_slug):
    """Traitement de la commande express depuis la vitrine."""
    shop = get_object_or_404(Shop, uuid=shop_uuid, slug=shop_slug)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse("Données invalides", status=400)

    items_data = data.get('items', [])
    if not items_data:
        return HttpResponse("Le panier est vide", status=400)

    # Calcul des montants
    subtotal = Decimal('0.00')
    customer_city = data.get('customer_city', 'Cocody')
    
    # Frais de livraison selon la commune
    if customer_city == 'Intérieur':
        delivery_fee = Decimal('3000.00')
    elif customer_city in ['Bingerville', 'Port-Bouët']:
        delivery_fee = Decimal('2000.00')
    else:
        delivery_fee = shop.payment.delivery_fee if hasattr(shop, 'payment') else Decimal('1500.00')

    # Nettoyage et formatage du téléphone
    raw_phone = data.get('customer_phone', '').strip()
    clean_phone = ''.join(filter(str.isdigit, str(raw_phone)))
    if len(clean_phone) == 10 and not clean_phone.startswith('225'):
        clean_phone = '+225' + clean_phone
    elif clean_phone.startswith('225') and len(clean_phone) == 13:
        clean_phone = '+' + clean_phone
    else:
        clean_phone = raw_phone  # fallback

    # Création de la commande
    order = Order.objects.create(
        shop=shop,
        customer_name=data.get('customer_name', '').strip(),
        customer_phone=clean_phone,
        customer_city=customer_city,
        customer_address=data.get('customer_address', '').strip(),
        payment_method=data.get('payment_method', 'livraison'),
        delivery_fee=delivery_fee,
    )

    for item in items_data:
        prod_id = item.get('id')
        qty = int(item.get('qty', 1))
        unit_price = Decimal(str(item.get('price', 0)))
        product = ShopProduct.objects.filter(uuid=prod_id).first() if prod_id else None
        
        line_total = unit_price * qty
        subtotal += line_total

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=item.get('name', 'Article'),
            unit_price=unit_price,
            quantity=qty,
            total_price=line_total
        )

        # Règle métier : Décrémentation automatique des stocks et alertes
        if product:
            if product.track_stock:
                product.stock = max(0, product.stock - qty)
                if product.stock == 0:
                    product.is_available = False
                    # Créer une notification de rupture de stock
                    Notification.objects.create(
                        shop=shop,
                        title=f"🔴 Rupture de stock : {product.name}",
                        message=f"L'article « {product.name} » est maintenant en rupture de stock suite à la commande {order.order_number}.",
                        notification_type='out_of_stock',
                    )
                elif product.stock <= 3:
                    # Alerte stock faible
                    Notification.objects.create(
                        shop=shop,
                        title=f"⚠️ Stock critique ({product.stock} restants) : {product.name}",
                        message=f"Il ne reste plus que {product.stock} exemplaire(s) pour « {product.name} ».",
                        notification_type='low_stock',
                    )
                product.save()

    order.subtotal = subtotal
    order.total_amount = subtotal + delivery_fee
    order.save()

    # Création de la notification de nouvelle commande pour le vendeur
    formatted_amount = f"{order.total_amount:,.0f}".replace(',', ' ')
    Notification.objects.create(
        shop=shop,
        title=f"📦 Nouvelle commande {order.order_number}",
        message=f"{order.customer_name} ({order.customer_city}) a commandé pour {formatted_amount} FCFA.",
        notification_type='new_order',
        order=order,
    )

    # 🚀 Envoi de la notification WebPush instantanée au vendeur (Hors-Ligne / Smartphone)
    send_order_web_push(order)

    # Lien direct WhatsApp
    whatsapp_url = generate_whatsapp_order_link(order)

    return render(request, 'shop/partials/order_success_modal.html', {
        'order': order,
        'whatsapp_url': whatsapp_url,
    })


# ==========================================
# 🔔 SYSTÈME DE NOTIFICATIONS EN DIRECT (HTMX)
# ==========================================

@login_required
def notifications_badge(request):
    """Retourne le badge et le dropdown des notifications en direct pour HTMX."""
    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return HttpResponse("")
    
    notifications = Notification.objects.filter(shop=shop).order_by('-created_at')[:8]
    unread_count = Notification.objects.filter(shop=shop, is_read=False).count()
    
    return render(request, 'shop/partials/notifications_dropdown.html', {
        'shop': shop,
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def notifications_mark_read(request):
    """Marque toutes les notifications du vendeur comme lues."""
    shop = Shop.objects.filter(owner=request.user).first()
    if shop:
        Notification.objects.filter(shop=shop, is_read=False).update(is_read=True)
    
    notifications = Notification.objects.filter(shop=shop).order_by('-created_at')[:8]
    return render(request, 'shop/partials/notifications_dropdown.html', {
        'shop': shop,
        'notifications': notifications,
        'unread_count': 0,
        'is_open': True,
    })


@login_required
def notification_mark_single_read(request, notification_uuid):
    """Marque une notification individuelle comme lue."""
    shop = Shop.objects.filter(owner=request.user).first()
    if shop:
        notif = Notification.objects.filter(shop=shop, uuid=notification_uuid).first()
        if notif:
            notif.is_read = True
            notif.save(update_fields=['is_read'])
            
    notifications = Notification.objects.filter(shop=shop).order_by('-created_at')[:8]
    unread_count = Notification.objects.filter(shop=shop, is_read=False).count()
    return render(request, 'shop/partials/notifications_dropdown.html', {
        'shop': shop,
        'notifications': notifications,
        'unread_count': unread_count,
        'is_open': True,
    })


