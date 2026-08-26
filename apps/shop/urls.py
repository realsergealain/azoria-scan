from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('create/', views.ShopCreateWizard.as_view(form_list=views.FORMS), name='create'),
    # Placeholder detail view - can be implemented later
    path('<int:pk>/', views.ShopCreateWizard.as_view(form_list=views.FORMS), name='detail'),
]
