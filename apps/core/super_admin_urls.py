from django.urls import path
from apps.core.super_admin_views import (
    super_admin_dashboard,
    super_admin_users_partial,
    super_admin_toggle_user_status,
    super_admin_shops_partial,
    super_admin_toggle_shop_status,
    super_admin_orders_partial,
)

app_name = 'super_admin'

urlpatterns = [
    path('', super_admin_dashboard, name='dashboard'),
    path('users/', super_admin_users_partial, name='users_partial'),
    path('users/<uuid:user_id>/toggle/', super_admin_toggle_user_status, name='toggle_user'),
    path('shops/', super_admin_shops_partial, name='shops_partial'),
    path('shops/<uuid:shop_uuid>/toggle/', super_admin_toggle_shop_status, name='toggle_shop'),
    path('orders/', super_admin_orders_partial, name='orders_partial'),
]
