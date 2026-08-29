from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Dashboard Actions
    path('creer/', views.shop_create, name='create'),
    path('parametres/', views.shop_settings, name='settings'),
    path('produits/', views.product_list, name='product_list'),
    path('produits/ajouter/', views.product_create, name='product_create'),
    path('produits/<uuid:product_uuid>/modifier/', views.product_update, name='product_update'),
    path('produits/<uuid:product_uuid>/supprimer/', views.product_delete, name='product_delete'),
    path('commandes/', views.order_list, name='order_list'),
    path('commandes/<uuid:order_uuid>/statut/', views.order_status_update, name='order_status_update'),
    path('clients/', views.customer_list, name='customer_list'),
    path('qr-codes/', views.qr_studio, name='qr_studio'),
    path('api/ai-description/', views.ai_description_api, name='ai_description_api'),

    # QR Codes Images Serving
    path('<uuid:shop_uuid>/qr/', views.shop_qr_code, name='shop_qr'),
    path('produits/<uuid:product_uuid>/qr/', views.product_qr_code, name='product_qr'),

    # Public Storefront & Checkout
    path('<uuid:shop_uuid>/<slug:shop_slug>/checkout/', views.checkout_view, name='checkout'),
    path('<uuid:shop_uuid>/<slug:shop_slug>/', views.shop_detail, name='detail'),

    # Notifications System (HTMX)
    path('notifications/badge/', views.notifications_badge, name='notifications_badge'),
    path('notifications/marquer-lues/', views.notifications_mark_read, name='notifications_mark_read'),
]

