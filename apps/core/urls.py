from django.urls import path
from apps.core.views import home_view, dashboard_view

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('tableau-de-bord/', dashboard_view, name='dashboard'),
]
