import hashlib
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from apps.accounts.models import User
from apps.shop.models import Shop, Order, ShopProduct


class HomeView(TemplateView):
    """
    Page d'accueil principale pour Azoria.
    Présente la plateforme de Social Commerce, les fonctionnalités,
    des démonstrations interactives et les avantages pour les vendeurs.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Données réelles extraites de la base de données
        active_sellers = Shop.objects.filter(is_active=True).values('owner').distinct().count()
        if active_sellers == 0:
            active_sellers = User.objects.filter(is_active=True, is_staff=False).count()
        
        total_orders = Order.objects.count()
        total_products = ShopProduct.objects.filter(is_available=True).count()
        cities_count = Shop.objects.filter(is_active=True).values('city').distinct().count() or 1

        def fmt_count(val: int) -> str:
            if val >= 1000:
                return f"{val:,}".replace(',', ' ') + "+"
            return str(val)

        context['active_sellers_count'] = active_sellers
        context['total_orders_count'] = total_orders
        context['total_products_count'] = total_products
        context['cities_count'] = cities_count

        context['stats'] = [
            {'label': 'Vendeurs actifs', 'value': fmt_count(active_sellers)},
            {'label': 'Commandes traitées', 'value': fmt_count(total_orders)},
            {'label': 'Articles en catalogue', 'value': fmt_count(total_products)},
            {'label': 'Villes et communes couvertes', 'value': fmt_count(cities_count)},
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


class FaqView(TemplateView):
    """Page dédiée Foire Aux Questions pour acheteurs et vendeurs."""
    template_name = 'core/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq_categories'] = [
            {
                'name': 'Démarrage & Inscription',
                'icon': 'rocket',
                'questions': [
                    {
                        'q': 'Comment créer ma boutique en ligne sur Azoria ?',
                        'a': 'Il vous suffit de cliquer sur "Créer ma boutique", de renseigner le nom de votre marque, votre numéro WhatsApp et d\'ajouter vos premiers articles. Votre boutique est prête et accessible en moins de 2 minutes.'
                    },
                    {
                        'q': 'Ai-je besoin d\'une carte bancaire pour démarrer ?',
                        'a': 'Non, aucune carte bancaire n\'est demandée pour créer votre boutique. Le plan Starter est 100% gratuit et vous permet de tester immédiatement la vente.'
                    },
                    {
                        'q': 'Comment mes clients accèdent-ils à mes produits ?',
                        'a': 'Vous disposez d\'un lien unique (ex: azoria.link/votre-boutique) et d\'un QR Code que vous pouvez coller dans votre bio TikTok, vos stories Instagram, vos statuts WhatsApp ou sur vos packagings.'
                    },
                ]
            },
            {
                'name': 'Paiement & Commandes',
                'icon': 'wallet',
                'questions': [
                    {
                        'q': 'Comment fonctionne le paiement à la livraison ?',
                        'a': 'Lors de la commande, le client choisit le paiement à la livraison (Cash on Delivery). Vous recevez la commande instantanément dans votre tableau de bord, vous l\'expédiez et vous encaissez directement à la réception.'
                    },
                    {
                        'q': 'Comment suis-je informé d\'une nouvelle commande ?',
                        'a': 'Chaque nouvelle commande apparaît immédiatement sur votre tableau de bord vendeur avec le récapitulatif complet : nom du client, numéro de téléphone, ville, commune, articles commandés et total.'
                    },
                    {
                        'q': 'Puis-je personnaliser les frais de livraison ?',
                        'a': 'Oui ! Vous pouvez définir des frais de livraison personnalisés par zone géographique (Abidjan par commune, et villes de l\'intérieur via les transporteurs).'
                    },
                ]
            },
            {
                'name': 'Azoria AI & Outils',
                'icon': 'sparkles',
                'questions': [
                    {
                        'q': 'Qu\'est-ce que l\'intelligence artificielle Azoria AI ?',
                        'a': 'Azoria AI génère automatiquement des descriptions de produits vendeuses et attractives à partir de simples mots-clés, adaptées au style des réseaux sociaux en Afrique.'
                    },
                    {
                        'q': 'Comment fonctionne le QR Code dynamique ?',
                        'a': 'Azoria génère un QR code haute résolution pour votre boutique ou pour chaque produit spécifique. Vos clients le scannent avec leur appareil photo et arrivent directement sur la fiche produit sans rien taper.'
                    },
                ]
            },
        ]
        return context


def faq_view(request):
    return FaqView.as_view()(request)


class GuideVendeurView(TemplateView):
    """Guide complet et bonnes pratiques pour les vendeurs sur réseaux sociaux."""
    template_name = 'core/guide_vendeur.html'


def guide_vendeur_view(request):
    return GuideVendeurView.as_view()(request)


class MentionsLegalesView(TemplateView):
    """Page légale et informations éditeur."""
    template_name = 'core/mentions_legales.html'


def mentions_legales_view(request):
    return MentionsLegalesView.as_view()(request)


class ConfidentialiteView(TemplateView):
    """Politique de confidentialité et protection des données personnelles."""
    template_name = 'core/confidentialite.html'


def confidentialite_view(request):
    return ConfidentialiteView.as_view()(request)


@login_required
def dashboard_view(request):
    """Tableau de bord principal du vendeur avec métriques avancées, KPIs et graphiques."""
    from apps.shop.models import Shop
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

    recent_ids = "-".join([str(getattr(o, 'id', '')) for o in analytics.get('recent_orders', [])])
    state_str = f"{analytics.get('total_orders')}-{analytics.get('total_revenue')}-{analytics.get('total_products')}-{analytics.get('total_visits')}-{analytics.get('active_orders')}-{recent_ids}"
    state_hash = hashlib.md5(state_str.encode('utf-8')).hexdigest()

    return render(request, 'core/dashboard.html', {
        'shops': shops,
        'primary_shop': primary_shop,
        'shop_count': shops.count(),
        'analytics': analytics,
        'state_hash': state_hash,
        'shop_form': ShopCreateForm(),
    })


@login_required
def dashboard_live_stats(request):
    """Fragment HTMX pour l'actualisation en temps réel (Polling) des KPIs et commandes récentes.
    Option 1 : Si les métriques sont identiques, renvoie HTTP 204 No Content pour éviter tout re-rendu/re-animation.
    """
    from apps.shop.models import Shop
    from apps.shop.services import get_shop_dashboard_analytics
    
    shop = Shop.objects.filter(owner=request.user).select_related('branding', 'payment').first()
    if not shop:
        return render(request, 'core/partials/dashboard_live_feed.html', {'analytics': {}, 'primary_shop': None, 'state_hash': ''})
    
    analytics = get_shop_dashboard_analytics(shop)
    
    recent_ids = "-".join([str(getattr(o, 'id', '')) for o in analytics.get('recent_orders', [])])
    state_str = f"{analytics.get('total_orders')}-{analytics.get('total_revenue')}-{analytics.get('total_products')}-{analytics.get('total_visits')}-{analytics.get('active_orders')}-{recent_ids}"
    state_hash = hashlib.md5(state_str.encode('utf-8')).hexdigest()
    
    client_hash = request.headers.get('X-Dashboard-Hash') or request.GET.get('hash')
    
    # 204 No Content : HTMX conserve le DOM actuel intact sans aucune animation intempestive
    if client_hash == state_hash and request.headers.get('HX-Request'):
        response = HttpResponse(status=204)
        response['X-Dashboard-Hash'] = state_hash
        return response
    
    response = render(request, 'core/partials/dashboard_live_feed.html', {
        'primary_shop': shop,
        'analytics': analytics,
        'state_hash': state_hash,
    })
    response['X-Dashboard-Hash'] = state_hash
    return response
