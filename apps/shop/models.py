from django.db import models
from django.conf import settings

class Shop(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ShopBranding(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='branding')
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#7C3AED')  # HEX color

    def __str__(self):
        return f"Branding for {self.shop.name}"

class ShopPayment(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='payment')
    GATEWAY_CHOICES = [
        ('mobile_money', '📱 Mobile Money (MTN, Orange, Wave…)'),
        ('livraison', '🚚 Paiement à la livraison'),
        ('virement', '🏦 Virement bancaire'),
    ]
    gateway = models.CharField(max_length=30, choices=GATEWAY_CHOICES, default='livraison')
    api_key = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Payment ({self.gateway}) for {self.shop.name}"

class ShopProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
