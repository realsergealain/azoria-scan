from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('creer/', views.shop_create, name='create'),
    path('<uuid:shop_uuid>/<slug:shop_slug>/', views.shop_detail, name='detail'),
]
