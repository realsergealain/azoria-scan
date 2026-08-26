from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Shop, ShopBranding, ShopPayment, ShopProduct

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'owner__email', 'owner__first_name', 'owner__last_name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20
    fieldsets = (
        (_('Informations Principales'), {
            'fields': ('name', 'owner', 'description')
        }),
    )

@admin.register(ShopBranding)
class ShopBrandingAdmin(admin.ModelAdmin):
    list_display = ('shop', 'primary_color', 'has_logo')
    list_filter = ('shop',)
    search_fields = ('shop__name',)
    ordering = ('shop',)
    
    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.short_description = _("Possède un logo")
    has_logo.boolean = True

@admin.register(ShopPayment)
class ShopPaymentAdmin(admin.ModelAdmin):
    list_display = ('shop', 'gateway')
    list_filter = ('gateway', 'shop')
    search_fields = ('shop__name', 'gateway')
    ordering = ('shop',)

@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price', 'created_at', 'has_image')
    list_filter = ('shop', 'created_at')
    search_fields = ('name', 'shop__name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('price',)
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.short_description = _("Possède une image")
    has_image.boolean = True
