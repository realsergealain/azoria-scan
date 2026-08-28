import urllib.parse
from io import BytesIO
from decimal import Decimal
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Q


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convertit une couleur Hex (#7C3AED) en tuple RGB."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (124, 58, 237)  # Violet Azoria par défaut


def generate_styled_qr_code(data: str, color_hex: str = '#7C3AED', box_size: int = 10) -> BytesIO:
    """
    Génère un QR Code haute définition, stylisé avec des coins arrondis
    et la couleur principale de la boutique.
    """
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)

    rgb_color = hex_to_rgb(color_hex)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=rgb_color)
    )

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def generate_whatsapp_order_link(order) -> str:
    """
    Génère un lien direct WhatsApp pour envoyer la commande au vendeur avec un formatage parfait.
    """
    shop = order.shop
    seller_phone = shop.phone or (shop.owner.phone if hasattr(shop.owner, 'phone') else '')
    
    # Nettoyage du numéro de téléphone (retire espaces, tirets, etc.)
    clean_phone = ''.join(filter(str.isdigit, str(seller_phone)))
    if clean_phone and not clean_phone.startswith(('225', '+225')) and len(clean_phone) == 10:
        clean_phone = '225' + clean_phone  # Format Côte d'Ivoire par défaut

    items_text = []
    for item in order.items.all():
        items_text.append(f"• {item.quantity}x *{item.product_name}* ({int(item.total_price):,} FCFA)")
    items_list_str = "\n".join(items_text)

    payment_label = dict(order.PAYMENT_CHOICES).get(order.payment_method, order.payment_method)

    message = (
        f"🛍️ *NOUVELLE COMMANDE — {shop.name}*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 *N° Commande :* {order.order_number}\n"
        f"👤 *Client :* {order.customer_name}\n"
        f"📞 *WhatsApp Client :* {order.customer_phone}\n"
        f"📍 *Lieu de livraison :* {order.customer_city} - {order.customer_address}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛒 *Articles commandés :*\n{items_list_str}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💵 *Sous-total :* {int(order.subtotal):,} FCFA\n"
        f"🚚 *Frais de livraison :* {int(order.delivery_fee):,} FCFA\n"
        f"💰 *TOTAL À PAYER :* {int(order.total_amount):,} FCFA\n"
        f"💳 *Règlement :* {payment_label}\n"
    )

    if order.notes:
        message += f"📝 *Précision :* {order.notes}\n"

    message += f"\n_Commande générée via Azoria Link 🔗_"

    encoded_msg = urllib.parse.quote(message)
    if clean_phone:
        return f"https://wa.me/{clean_phone}?text={encoded_msg}"
    return f"https://wa.me/?text={encoded_msg}"


def generate_ai_product_description(name: str, category: str = "") -> dict:
    """
    Génère un titre accrocheur, une description vendeuse et des arguments percutants pour Azoria AI via OpenAI.
    """
    import openai
    from django.conf import settings
    
    # Récupérer la clé API depuis .env ou settings
    openai.api_key = getattr(settings, 'OPENAI_API_KEY', None)
    import os
    if not openai.api_key:
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        
    if not openai.api_key:
        # Fallback de sécurité si pas de clé
        return {
            'title': f"{name} ✨ Tendance & Qualité",
            'description': f"Découvrez notre {name} ! Qualité premium et design élégant. Commandez dès maintenant avec paiement à la livraison.",
            'badge': '🔥 Meilleure Vente'
        }

    prompt = (
        f"Tu es un expert en e-commerce, dropshipping et copywriting pour le marché africain (Côte d'Ivoire, Sénégal, etc). "
        f"Ton but est de rédiger une description TRES VENDEUSE, accrocheuse, pour inciter les clients sur WhatsApp et TikTok à acheter.\n\n"
        f"Produit : {name}\n"
        f"Catégorie : {category}\n\n"
        f"Rédige UNIQUEMENT la description du produit (pas de titre, pas de blabla). La description doit être courte (maximum 4 lignes) "
        f"avec des emojis, et mettre en valeur la qualité, la fiabilité, et encourager à commander avec paiement à la livraison."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert copywriter e-commerce."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        description = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erreur OpenAI: {e}")
        description = f"Découvrez notre magnifique {name} ! Un article de qualité supérieure qui saura vous satisfaire. Commandez dès aujourd'hui."

    return {
        'title': f"{name} ✨ Tendance & Qualité",
        'description': description,
        'badge': '🔥 Meilleure Vente'
    }


def get_shop_dashboard_analytics(shop) -> dict:
    """
    Calcule toutes les métriques de la boutique pour le tableau de bord et les graphiques ApexCharts.
    """
    from .models import Order, VisitTracker, ShopProduct

    # 1. Commandes & Revenus
    orders = Order.objects.filter(shop=shop)
    total_orders = orders.count()
    active_orders = orders.filter(status__in=['pending', 'confirmed', 'shipped']).count()
    
    total_revenue = orders.filter(status__in=['confirmed', 'shipped', 'delivered']).aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')

    # 2. Produits
    total_products = ShopProduct.objects.filter(shop=shop, is_available=True).count()

    # 3. Visites (Direct vs QR)
    visits = VisitTracker.objects.filter(shop=shop)
    total_visits = visits.count()
    qr_visits = visits.filter(source='qr').count()
    direct_visits = total_visits - qr_visits

    # 4. Données pour les 7 derniers jours (ApexCharts)
    today = timezone.now().date()
    days_labels = []
    sales_data = []
    visits_data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime('%a')  # Lun, Mar...
        days_labels.append(day_str)

        day_sales = orders.filter(
            status__in=['confirmed', 'shipped', 'delivered'],
            created_at__date=day
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        sales_data.append(int(day_sales))

        day_visits = visits.filter(created_at__date=day).count()
        visits_data.append(day_visits)

    # 5. Dernières commandes
    recent_orders = orders.order_by('-created_at')[:6]

    return {
        'total_revenue': f"{int(total_revenue):,} FCFA",
        'total_orders': total_orders,
        'active_orders': active_orders,
        'total_products': total_products,
        'total_visits': total_visits,
        'qr_visits': qr_visits,
        'direct_visits': direct_visits,
        'days_labels': days_labels,
        'sales_data': sales_data,
        'visits_data': visits_data,
        'recent_orders': recent_orders,
    }
