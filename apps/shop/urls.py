from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('create/', views.shop_create, name='create'),
    path('<int:pk>/', views.shop_detail, name='detail'),
]
