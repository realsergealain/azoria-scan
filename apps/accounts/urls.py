from django.urls import path
from apps.accounts.views import login_view, logout_view, register_view, profile_settings_view
from apps.accounts.views_push import get_vapid_key_api, subscribe_push_api, unsubscribe_push_api, test_push_api

app_name = 'accounts'

urlpatterns = [
    path('connexion/', login_view, name='login'),
    path('inscription/', register_view, name='register'),
    path('deconnexion/', logout_view, name='logout'),
    path('parametres/', profile_settings_view, name='settings'),
    
    # Web Push Notification Endpoints
    path('api/push/vapid-key/', get_vapid_key_api, name='push_vapid_key'),
    path('api/push/subscribe/', subscribe_push_api, name='push_subscribe'),
    path('api/push/unsubscribe/', unsubscribe_push_api, name='push_unsubscribe'),
    path('api/push/test/', test_push_api, name='push_test'),
]
