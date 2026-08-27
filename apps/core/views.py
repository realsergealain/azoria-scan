from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Page d'accueil principale pour Azoria.
    Présente la plateforme de Social Commerce, les fonctionnalités,
    des démonstrations interactives et les avantages pour les vendeurs.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['stats'] = [
            {'label': 'Vendeurs actifs', 'value': '2 400+'},
            {'label': 'Commandes traitées', 'value': '85 000+'},
            {'label': 'Taux de satisfaction', 'value': '99.4%'},
            {'label': 'Villes et communes couvertes', 'value': '120+'},
        ]
        
        context['channels'] = [
            {'name': 'TikTok', 'icon': 'video', 'badge': 'Bio & Live TikTok', 'color': 'from-pink-500 to-rose-600'},
            {'name': 'WhatsApp', 'icon': 'message-circle', 'badge': 'Statuts & Groupes', 'color': 'from-emerald-500 to-green-600'},
            {'name': 'Instagram', 'icon': 'instagram', 'badge': 'Reels & Stories', 'color': 'from-purple-500 to-pink-500'},
            {'name': 'Facebook', 'icon': 'facebook', 'badge': 'Posts & Marketplace', 'color': 'from-blue-600 to-indigo-600'},
            {'name': 'QR Codes', 'icon': 'qr-code', 'badge': 'Affiches & Emballages', 'color': 'from-violet-600 to-purple-800'},
        ]
        
        return context


def home_view(request):
    return HomeView.as_view()(request)


@login_required
def dashboard_view(request):
    """Tableau de bord principal du vendeur connecté avec métriques réelles."""
    from apps.shop.models import Shop, ShopProduct, Order, VisitTracker
    from apps.shop.forms import ShopCreateForm
    from apps.shop.services import get_shop_dashboard_analytics
    
    shops = Shop.objects.filter(owner=request.user).select_related('branding', 'payment')
    primary_shop = shops.first()

    if primary_shop:
        analytics = get_shop_dashboard_analytics(primary_shop)
    else:
        analytics = {
            'total_revenue': '0 FCFA',
            'total_orders': 0,
            'active_orders': 0,
            'total_products': 0,
            'total_visits': 0,
            'qr_visits': 0,
            'direct_visits': 0,
            'days_labels': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
            'sales_data': [0, 0, 0, 0, 0, 0, 0],
            'visits_data': [0, 0, 0, 0, 0, 0, 0],
            'recent_orders': [],
        }

    return render(request, 'core/dashboard.html', {
        'shops': shops,
        'primary_shop': primary_shop,
        'shop_count': shops.count(),
        'analytics': analytics,
        'shop_form': ShopCreateForm(),
    })
