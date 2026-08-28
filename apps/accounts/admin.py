from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from django.db.models import Sum, Count

from apps.accounts.models import User


class UserResource(resources.ModelResource):
    total_orders = fields.Field(column_name='Nombre de commandes')
    total_sales = fields.Field(column_name='Total des ventes (FCFA)')

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'total_orders', 'total_sales', 'date_joined')
        export_order = ('id', 'email', 'first_name', 'last_name', 'phone', 'total_orders', 'total_sales', 'date_joined')

    def dehydrate_total_orders(self, user):
        return getattr(user, 'total_orders_count', 0)

    def dehydrate_total_sales(self, user):
        return getattr(user, 'total_sales_sum', 0)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin, ModelAdmin):
    resource_class = UserResource
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            total_orders_count=Count('shop__orders', distinct=True),
            total_sales_sum=Sum('shop__orders__total_amount')
        )
        return qs

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informations personnelles'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active'),
        }),
    )
