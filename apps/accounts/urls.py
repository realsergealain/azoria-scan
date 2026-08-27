from django.urls import path
from apps.accounts.views import login_view, logout_view, register_view, profile_settings_view

app_name = 'accounts'

urlpatterns = [
    path('connexion/', login_view, name='login'),
    path('inscription/', register_view, name='register'),
    path('deconnexion/', logout_view, name='logout'),
    path('parametres/', profile_settings_view, name='settings'),
]
