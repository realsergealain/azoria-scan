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


from PIL import Image, ImageDraw, ImageFont


def generate_styled_qr_code(
    data: str, 
    color_hex: str = '#7C3AED', 
    logo_image=None, 
    box_size: int = 15, 
    transparent: bool = False
) -> BytesIO:
    """
    Génère un QR Code HD 1:1 parfait, stylisé avec des coins arrondis,
    logo au centre optionnel et fond transparent.
    """
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    rgb_color = hex_to_rgb(color_hex)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=rgb_color)
    ).convert("RGBA")

    if transparent:
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)

    if logo_image:
        try:
            logo = Image.open(logo_image).convert("RGBA")
            qr_w, qr_h = img.size
            logo_max_size = int(qr_w * 0.22)
            logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
            
            logo_w, logo_h = logo.size
            pos_x = (qr_w - logo_w) // 2
            pos_y = (qr_h - logo_h) // 2
            
            padding = 6
            bg_box = Image.new("RGBA", (logo_w + padding*2, logo_h + padding*2), (255, 255, 255, 255))
            img.paste(bg_box, (pos_x - padding, pos_y - padding), bg_box)
            img.paste(logo, (pos_x, pos_y), logo)
        except Exception:
            pass

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def generate_styled_qr_card(
    data: str, 
    color_hex: str = '#7C3AED', 
    logo_image=None, 
    shop_name: str = "Ma Boutique Azoria",
    show_frame: bool = True,
    box_size: int = 15, 
    transparent: bool = False
) -> BytesIO:
    """
    Génère une carte d'affichage QR Code complète avec bandeau 'SCAN ME !',
    Nom de la boutique en haut et QR Code au centre.
    """
    qr_buf = generate_styled_qr_code(data, color_hex=color_hex, logo_image=logo_image, box_size=box_size, transparent=transparent)
    qr_img = Image.open(qr_buf).convert("RGBA")
    qr_w, qr_h = qr_img.size

    rgb_color = hex_to_rgb(color_hex)
    padding = 40
    header_height = 80 if show_frame else 0
    name_height = 50 if shop_name else 0
    card_w = qr_w + (padding * 2)
    card_h = header_height + name_height + qr_h + (padding * 2)

    bg_color = (0, 0, 0, 0) if transparent else (255, 255, 255, 255)
    card = Image.new("RGBA", (card_w, card_h), bg_color)
    draw = ImageDraw.Draw(card)

    # 1. Draw "SCAN ME !" Banner
    if show_frame:
        banner_box = [padding, padding, card_w - padding, padding + header_height]
        draw.rounded_rectangle(banner_box, radius=20, fill=rgb_color + (255,))

        try:
            font_banner = ImageFont.truetype("arial.ttf", 32)
        except Exception:
            font_banner = ImageFont.load_default()

        banner_text = "SCAN ME !"
        bbox = draw.textbbox((0, 0), banner_text, font=font_banner)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = (card_w - text_w) // 2
        text_y = padding + (header_height - text_h) // 2 - 4
        draw.text((text_x, text_y), banner_text, fill=(255, 255, 255, 255), font=font_banner)

    # 2. Draw Shop Name
    if shop_name:
        try:
            font_name = ImageFont.truetype("arial.ttf", 26)
        except Exception:
            font_name = ImageFont.load_default()

        bbox_n = draw.textbbox((0, 0), shop_name, font=font_name)
        name_w = bbox_n[2] - bbox_n[0]
        name_x = (card_w - name_w) // 2
        name_y = padding + header_height + (15 if show_frame else 5)
        draw.text((name_x, name_y), shop_name, fill=(15, 23, 42, 255) if not transparent else (255, 255, 255, 255), font=font_name)

    # 3. Paste QR Code
    qr_y = padding + header_height + name_height + 10
    card.paste(qr_img, (padding, qr_y), qr_img)

    buffer = BytesIO()
    card.save(buffer, format="PNG")
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


def generate_ai_product_description(name: str, category: str = "", image_file=None) -> dict:
    """
    Génère une description e-commerce vendeuse et professionnelle via l'API OpenAI.
    Logique conditionnelle (Fallback) :
    - Scénario A (Image présente) : utilise le modèle Vision (gpt-4o-mini / gpt-4o) avec analyse de l'image.
    - Scénario B (Pas d'image) : utilise le modèle textuel gpt-4o-mini basé sur le nom et la catégorie.
    """
    import os
    import base64
    import openai
    from django.conf import settings

    api_key = getattr(settings, 'OPENAI_API_KEY', None) or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return {
            'title': f"{name} ✨ Tendance & Qualité",
            'description': f"Découvrez notre {name} ! Qualité premium et design élégant. Commandez dès maintenant avec paiement à la livraison.",
            'badge': '🔥 Meilleure Vente'
        }

    # Préparation de l'image si présente (Scénario A)
    base64_image = None
    if image_file:
        try:
            image_bytes = None
            if hasattr(image_file, 'read'):
                image_bytes = image_file.read()
                if hasattr(image_file, 'seek'):
                    image_file.seek(0)
            elif hasattr(image_file, 'path') and os.path.exists(image_file.path):
                with open(image_file.path, 'rb') as f:
                    image_bytes = f.read()

            if image_bytes:
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
        except Exception as e:
            print(f"[Azoria AI] Erreur encodage image vision: {e}")

    model_name = "gpt-4o-mini"

    # Construction des messages selon le scénario
    if base64_image:
        # SCÉNARIO A : Vision avec Image
        prompt_text = (
            f"Analyse attentivement cette image. Rédige une description e-commerce vendeuse, détaillée et professionnelle "
            f"pour le produit '{name}' (Catégorie: '{category or 'Général'}'). "
            f"Base-toi sur l'apparence visuelle, les couleurs, la forme et l'usage suggéré par l'objet. "
            f"Rédige une description de 4 à 6 lignes avec des emojis attrayants et un appel à l'action clair (Paiement à la livraison)."
        )
        messages = [
            {"role": "system", "content": "Tu es un expert copywriter e-commerce vision de classe mondiale."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ]
    else:
        # SCÉNARIO B : Titre uniquement (Fallback Textuel)
        prompt_text = (
            f"En te basant uniquement sur le titre suivant : '{name}' (Catégorie: '{category or 'Général'}'), "
            f"rédige une description e-commerce convaincante, mettant en avant les caractéristiques probables "
            f"et les avantages de ce type de produit. "
            f"Rédige 4 à 6 lignes captivantes avec des emojis et un appel à l'action incitant à commander (Paiement à la livraison)."
        )
        messages = [
            {"role": "system", "content": "Tu es un expert copywriter e-commerce de classe mondiale."},
            {"role": "user", "content": prompt_text}
        ]

    try:
        if hasattr(openai, 'OpenAI'):
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            description = response.choices[0].message.content.strip()
        else:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            description = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Azoria AI] Erreur OpenAI Vision: {e}")
        description = (
            f"✨ Découvrez notre magnifique {name} !\n"
            f"Un article d'exception sélectionné pour sa qualité premium et son design élégant.\n"
            f"⚡ Quantités limitées. Profitez du paiement à la livraison et commandez dès aujourd'hui !"
        )

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
