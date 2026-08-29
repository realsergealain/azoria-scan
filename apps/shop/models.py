from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid
import random
import os
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

def shop_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('users', str(instance.shop.owner.id), 'shops', str(instance.shop.uuid), 'branding', f"logo.{ext}")

def shop_banner_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('users', str(instance.shop.owner.id), 'shops', str(instance.shop.uuid), 'branding', f"banner.{ext}")

def product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('users', str(instance.shop.owner.id), 'shops', str(instance.shop.uuid), 'products', f"{uuid.uuid4().hex}.{ext}")

def secondary_product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('users', str(instance.product.shop.owner.id), 'shops', str(instance.product.shop.uuid), 'products', f"{uuid.uuid4().hex}.{ext}")



class Shop(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shops', verbose_name=_("Propriétaire"))
    name = models.CharField(max_length=120, verbose_name=_("Nom de la boutique"))
    category = models.CharField(max_length=80, default="Mode & Habillement", verbose_name=_("Catégorie"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    phone = models.CharField(max_length=25, blank=True, verbose_name=_("Numéro WhatsApp pour commandes"), help_text=_("Ex: +225 0700000000"))
    city = models.CharField(max_length=80, default="Abidjan", verbose_name=_("Ville / Commune"))
    is_active = models.BooleanField(default=True, verbose_name=_("Boutique active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    class Meta:
        verbose_name = _("Boutique")
        verbose_name_plural = _("Boutiques")
        ordering = ['-created_at']

    @property
    def is_name_locked(self) -> bool:
        """Indique si le nom de la boutique est verrouillé (plus de 7 jours après création)."""
        from django.utils import timezone
        from datetime import timedelta
        if not self.created_at:
            return False
        return (timezone.now() - self.created_at) > timedelta(days=7)

    @property
    def name_unlock_days_left(self) -> int:
        """Nombre de jours restants avant le verrouillage définitif du nom."""
        from django.utils import timezone
        from datetime import timedelta
        if not self.created_at:
            return 7
        diff = timedelta(days=7) - (timezone.now() - self.created_at)
        return max(0, diff.days + 1 if diff.total_seconds() > 0 else 0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "boutique"
            slug = base_slug
            counter = 1
            while Shop.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ShopBranding(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='branding', verbose_name=_("Boutique"))
    logo = ProcessedImageField(upload_to=shop_logo_path,
                               processors=[ResizeToFill(400, 400)],
                               format='WEBP',
                               options={'quality': 85},
                               max_length=255,
                               blank=True, null=True, verbose_name=_("Logo"))
    banner = ProcessedImageField(upload_to=shop_banner_path,
                                 processors=[ResizeToFill(1200, 400)],
                                 format='WEBP',
                                 options={'quality': 85},
                                 max_length=255,
                                 blank=True, null=True, verbose_name=_("Bannière"))
    slogan = models.CharField(max_length=150, blank=True, verbose_name=_("Slogan"))
    primary_color = models.CharField(max_length=7, default='#7C3AED', verbose_name=_("Couleur principale (HEX)"))

    class Meta:
        verbose_name = _("Identité visuelle")
        verbose_name_plural = _("Identités visuelles")

    def __str__(self):
        return f"Marque de {self.shop.name}"


class ShopPayment(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='payment', verbose_name=_("Boutique"))
    GATEWAY_CHOICES = [
        ('livraison', '🚚 Paiement à la livraison (Cash / Wave à réception)'),
        ('mobile_money', '📱 Mobile Money (Wave, Orange, MTN, Moov)'),
        ('virement', '🏦 Virement bancaire'),
    ]
    accepted_payments = models.JSONField(default=list, verbose_name=_("Moyens de paiement acceptés"))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00, verbose_name=_("Frais de livraison par défaut (FCFA)"))
    free_delivery_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Livraison offerte à partir de (FCFA)"))
    accepted_delivery_zones = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Zones de livraison"),
        help_text=_("Liste des communes/villes desservies")
    )
    api_key = models.CharField(max_length=255, blank=True, verbose_name=_("Clé API (Optionnel)"))

    class Meta:
        verbose_name = _("Configuration de paiement & livraison")
        verbose_name_plural = _("Configurations de paiement & livraison")

    def __str__(self):
        return f"Paiements & Livraison pour {self.shop.name}"


class ShopProduct(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', verbose_name=_("Boutique"))
    name = models.CharField(max_length=150, verbose_name=_("Nom du produit"))
    category = models.CharField(max_length=80, blank=True, default="Général", verbose_name=_("Catégorie"))
    description = models.TextField(blank=True, verbose_name=_("Description du produit"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix (FCFA)"))
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Prix barré / Promo (FCFA)"))
    image = ProcessedImageField(upload_to=product_image_path,
                                processors=[ResizeToFit(1024, 1024)],
                                format='WEBP',
                                options={'quality': 85},
                                max_length=255,
                                blank=True, null=True, verbose_name=_("Image principale"))
    is_available = models.BooleanField(default=True, verbose_name=_("Disponible en stock"))
    stock = models.PositiveIntegerField(default=10, verbose_name=_("Quantité en stock"))
    track_stock = models.BooleanField(default=True, verbose_name=_("Suivre le stock"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date d'ajout"))

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "produit"
            slug = base_slug
            counter = 1
            while ShopProduct.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        # Si le stock est épuisé et suivi, adapter is_available
        if self.track_stock and self.stock <= 0:
            self.is_available = False
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self) -> bool:
        if not self.is_available:
            return False
        if self.track_stock and self.stock <= 0:
            return False
        return True

    @property
    def discount_percent(self):
        if self.compare_price and self.compare_price > self.price:
            diff = self.compare_price - self.price
            return int(round((diff / self.compare_price) * 100))
        return 0

    def __str__(self):
        return f"{self.name} ({self.shop.name})"


class ProductImage(models.Model):
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name='images', verbose_name=_("Produit"))
    image = ProcessedImageField(upload_to=secondary_product_image_path,
                                processors=[ResizeToFit(1024, 1024)],
                                format='WEBP',
                                options={'quality': 85},
                                max_length=255,
                                verbose_name=_("Image supplémentaire"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Image produit")
        verbose_name_plural = _("Images produit")
        ordering = ['created_at']

    def __str__(self):
        return f"Image de {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '🟡 Reçue (En attente)'),
        ('confirmed', '🔵 Confirmée'),
        ('shipped', '🟣 En livraison / En route'),
        ('delivered', '🟢 Livrée'),
        ('cancelled', '🔴 Annulée'),
    ]

    PAYMENT_CHOICES = [
        ('livraison', 'Paiement à la livraison (Cash)'),
        ('wave', 'Wave'),
        ('orange_money', 'Orange Money'),
        ('mtn', 'MTN Mobile Money'),
        ('moov', 'Moov Money'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_number = models.CharField(max_length=30, unique=True, editable=False, verbose_name=_("Numéro de commande"))
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders', verbose_name=_("Boutique"))
    
    # Informations client
    customer_name = models.CharField(max_length=120, verbose_name=_("Nom du client"))
    customer_phone = models.CharField(max_length=30, verbose_name=_("Téléphone WhatsApp"))
    customer_city = models.CharField(max_length=80, verbose_name=_("Commune / Ville"))
    customer_address = models.CharField(max_length=255, verbose_name=_("Précision adresse / Carrefour / Repère"))
    notes = models.TextField(blank=True, verbose_name=_("Instructions spéciales"))

    # Montants
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name=_("Sous-total (FCFA)"))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Frais de livraison (FCFA)"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name=_("Total TTC (FCFA)"))
    
    # Statut & Paiement
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_("Statut"))
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='livraison', verbose_name=_("Mode de paiement"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de commande"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Dernière mise à jour"))

    class Meta:
        verbose_name = _("Commande")
        verbose_name_plural = _("Commandes")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            rand_suffix = random.randint(1000, 9999)
            self.order_number = f"#AZ-{rand_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} ({self.total_amount} FCFA)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Commande"))
    product = models.ForeignKey(ShopProduct, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items', verbose_name=_("Produit"))
    product_name = models.CharField(max_length=150, verbose_name=_("Nom du produit au moment de l'achat"))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix unitaire (FCFA)"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantité"))
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Total ligne (FCFA)"))

    class Meta:
        verbose_name = _("Article de commande")
        verbose_name_plural = _("Articles de commande")

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} ({self.total_price} FCFA)"


class VisitTracker(models.Model):
    SOURCE_CHOICES = [
        ('direct', 'Lien Direct / Bio'),
        ('qr', 'QR Code Flash'),
        ('tiktok', 'TikTok'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='visits', verbose_name=_("Boutique"))
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, null=True, blank=True, related_name='visits', verbose_name=_("Produit"))
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='direct', verbose_name=_("Canal d'accès"))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("Adresse IP"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de visite"))

    class Meta:
        verbose_name = _("Visite")
        verbose_name_plural = _("Visites")
        ordering = ['-created_at']

    def __str__(self):
        return f"Visite de {self.shop.name} via {self.source}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_order', '📦 Nouvelle commande'),
        ('low_stock', '⚠️ Stock faible'),
        ('out_of_stock', '🔴 Rupture de stock'),
        ('system', 'ℹ️ Information système'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='notifications', verbose_name=_("Boutique"))
    title = models.CharField(max_length=150, verbose_name=_("Titre"))
    message = models.TextField(verbose_name=_("Message"))
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='new_order', verbose_name=_("Type"))
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications', verbose_name=_("Commande associée"))
    is_read = models.BooleanField(default=False, verbose_name=_("Lu"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.shop.name}"

