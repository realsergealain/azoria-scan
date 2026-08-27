from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('creer/', views.shop_create, name='create'),
    path('produits/', views.product_list, name='product_list'),
    path('produits/ajouter/', views.product_create, name='product_create'),
    path('produits/<uuid:product_uuid>/modifier/', views.product_update, name='product_update'),
    path('produits/<uuid:product_uuid>/supprimer/', views.product_delete, name='product_delete'),
    path('<uuid:shop_uuid>/qr/', views.shop_qr_code, name='shop_qr'),
    path('produits/<uuid:product_uuid>/qr/', views.product_qr_code, name='product_qr'),
    path('<uuid:shop_uuid>/<slug:shop_slug>/', views.shop_detail, name='detail'),
]
