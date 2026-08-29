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


@login_required
def dashboard_live_stats(request):
    """Fragment HTMX pour l'actualisation en temps réel (Polling) des KPIs et commandes récentes."""
    from apps.shop.models import Shop
    from apps.shop.services import get_shop_dashboard_analytics
    
    shop = Shop.objects.filter(owner=request.user).select_related('branding', 'payment').first()
    if not shop:
        return render(request, 'core/partials/dashboard_live_feed.html', {'analytics': {}, 'primary_shop': None})
    
    analytics = get_shop_dashboard_analytics(shop)
    return render(request, 'core/partials/dashboard_live_feed.html', {
        'primary_shop': shop,
        'analytics': analytics,
    })

