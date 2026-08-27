from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils.text import slugify

class Shop(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shops', verbose_name=_("Propriétaire"))
    name = models.CharField(max_length=120, verbose_name=_("Nom de la boutique"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    class Meta:
        verbose_name = _("Boutique")
        verbose_name_plural = _("Boutiques")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure slug is unique if needed, but since names could be duplicated, we might need a unique suffix. Let's start simple.
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ShopBranding(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='branding', verbose_name=_("Boutique"))
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True, verbose_name=_("Logo"))
    primary_color = models.CharField(max_length=7, default='#7C3AED', verbose_name=_("Couleur principale"))  # HEX color

    class Meta:
        verbose_name = _("Identité visuelle")
        verbose_name_plural = _("Identités visuelles")

    def __str__(self):
        return f"Marque de {self.shop.name}"

class ShopPayment(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='payment', verbose_name=_("Boutique"))
    GATEWAY_CHOICES = [
        ('mobile_money', '📱 Mobile Money (MTN, Orange, Wave…)'),
        ('livraison', '🚚 Paiement à la livraison'),
        ('virement', '🏦 Virement bancaire'),
    ]
    accepted_payments = models.JSONField(default=list, verbose_name=_("Moyens de paiement acceptés"))
    api_key = models.CharField(max_length=255, blank=True, verbose_name=_("Clé API (Optionnel)"))

    class Meta:
        verbose_name = _("Configuration de paiement")
        verbose_name_plural = _("Configurations de paiement")

    def __str__(self):
        return f"Paiements pour {self.shop.name}"

class ShopProduct(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', verbose_name=_("Boutique"))
    name = models.CharField(max_length=120, verbose_name=_("Nom du produit"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix"))
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_("Image du produit"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date d'ajout"))

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class VisitTracker(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='visits')
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, null=True, blank=True, related_name='visits')
    source = models.CharField(max_length=20, choices=[('direct', 'Lien Direct'), ('qr', 'QR Code')], default='direct')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Visite")
        verbose_name_plural = _("Visites")

    def __str__(self):
        return f"Visite de {self.shop.name} - {self.source}"
