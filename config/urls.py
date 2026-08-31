"""
URL configuration for Azoria project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customization of Django Admin Panel
admin.site.site_header = "Administration Azoria"
admin.site.site_title = "Portail Admin Azoria"
admin.site.index_title = "Tableau de Bord Principal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('super-admin/', include('apps.core.super_admin_urls', namespace='super_admin')),
    path('mon-compte/', include('apps.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.core.urls', namespace='core')),
    path('boutique/', include('apps.shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
