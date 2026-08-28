from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from django.db.models import Sum, Count

from .models import Shop, ShopBranding, ShopPayment, ShopProduct


class ShopResource(resources.ModelResource):
    total_orders = fields.Field(column_name='Nombre de commandes')
    total_sales = fields.Field(column_name='Total des ventes (FCFA)')
    owner_email = fields.Field(attribute='owner__email', column_name='Email Propriétaire')

    class Meta:
        model = Shop
        fields = ('id', 'name', 'owner_email', 'total_orders', 'total_sales', 'created_at')
        export_order = ('id', 'name', 'owner_email', 'total_orders', 'total_sales', 'created_at')

    def dehydrate_total_orders(self, shop):
        return getattr(shop, 'total_orders_count', 0)

    def dehydrate_total_sales(self, shop):
        return getattr(shop, 'total_sales_sum', 0)


@admin.register(Shop)
class ShopAdmin(ImportExportModelAdmin, ModelAdmin):
    resource_class = ShopResource
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            total_orders_count=Count('orders', distinct=True),
            total_sales_sum=Sum('orders__total_amount')
        )
        return qs

@admin.register(ShopBranding)
class ShopBrandingAdmin(ModelAdmin):
    list_display = ('shop', 'primary_color', 'has_logo')
    list_filter = ('shop',)
    search_fields = ('shop__name',)
    ordering = ('shop',)
    
    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.short_description = _("Possède un logo")
    has_logo.boolean = True

@admin.register(ShopPayment)
class ShopPaymentAdmin(ModelAdmin):
    list_display = ('shop', 'accepted_payments')
    list_filter = ('shop',)
    search_fields = ('shop__name',)
    ordering = ('shop',)

@admin.register(ShopProduct)
class ShopProductAdmin(ModelAdmin):
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
