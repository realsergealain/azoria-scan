from django.urls import path
from apps.core.views import (
    home_view,
    dashboard_view,
    dashboard_live_stats,
    faq_view,
    guide_vendeur_view,
    mentions_legales_view,
    confidentialite_view,
)

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('tableau-de-bord/', dashboard_view, name='dashboard'),
    path('tableau-de-bord/live-stats/', dashboard_live_stats, name='dashboard_live_stats'),
    path('faq/', faq_view, name='faq'),
    path('guide-du-vendeur/', guide_vendeur_view, name='guide_vendeur'),
    path('mentions-legales/', mentions_legales_view, name='mentions_legales'),
    path('confidentialite/', confidentialite_view, name='confidentialite'),
]
