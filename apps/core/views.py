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
        
        # Données de démonstration et présentation
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
        
        context['features'] = [
            {
                'id': 'onboarding',
                'badge': 'Création Express',
                'title': 'Créez votre boutique en 2 minutes',
                'desc': 'Renseignez votre nom, vos catégories et obtenez immédiatement votre lien unique personnalisé (ex: azoria.link/votre-boutique). Sans compétence technique requise.',
                'icon': 'sparkles',
            },
            {
                'id': 'sharing',
                'badge': 'Social Commerce',
                'title': 'Partagez sur WhatsApp, TikTok & Instagram',
                'desc': 'Fini les va-et-vient infinis par messages pour demander nom, taille, couleur et adresse. Vos clients commandent directement en 30 secondes.',
                'icon': 'share-2',
            },
            {
                'id': 'ai',
                'badge': 'Azoria AI',
                'title': 'Génération IA de fiches produits',
                'desc': 'Azoria AI rédige pour vous des titres percutants, des descriptions vendeuses et les points forts de vos articles en 1 clic.',
                'icon': 'bot',
            },
            {
                'id': 'delivery',
                'badge': 'Logistique & Paiement',
                'title': 'Livraison locale et paiement à la livraison',
                'desc': 'Tarification automatique selon la commune (Cocody, Yopougon, Marcory...) ou expédition vers l\'intérieur avec transporteurs partenaires.',
                'icon': 'truck',
            },
        ]
        
        context['faqs'] = [
            {
                'q': 'Ai-je besoin d\'un ordinateur ou de compétences en informatique ?',
                'a': 'Non, absolument pas ! Azoria a été conçu spécialement pour être 100% géré depuis votre smartphone en quelques clics.',
            },
            {
                'q': 'Comment mes clients paient-ils leurs commandes ?',
                'a': 'Azoria intègre nativement le paiement à la livraison (Cash on Delivery / Wave / Orange Money à la réception), qui est le mode le plus plébiscité et rassurant pour les acheteurs.',
            },
            {
                'q': 'Puis-je utiliser mon propre QR Code pour mes emballages et flyers ?',
                'a': 'Oui ! Azoria génère automatiquement un QR Code haute définition pour votre boutique complète ainsi que pour chaque produit individuel ou campagne promo.',
            },
            {
                'q': 'Est-ce que je peux livrer à l\'intérieur du pays ?',
                'a': 'Absolument. Vous pouvez configurer des tarifs pour vos livraisons urbaines ainsi que des options d\'expédition par compagnies de transport partenaires (UTB, CTE, etc.) pour toutes les villes de l\'intérieur.',
            },
        ]
        
        return context


def home_view(request):
    return HomeView.as_view()(request)


@login_required
def dashboard_view(request):
    """Tableau de bord principal du vendeur."""
    from apps.shop.models import Shop
    shops = Shop.objects.filter(owner=request.user).select_related('branding', 'payment')
    return render(request, 'core/dashboard.html', {
        'shops': shops,
        'shop_count': shops.count(),
    })
