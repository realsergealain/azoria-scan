import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, Q
from django.contrib import messages

from apps.accounts.models import User
from apps.shop.models import Shop, Order, ShopProduct, VisitTracker


def staff_required(user):
    """Vérification stricte que l'utilisateur est administrateur / staff."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(staff_required, login_url='accounts:login')
def super_admin_dashboard(request):
    """
    Tableau de bord principal du Super Admin.
    Présente les KPIs globaux de la plateforme, le flux d'activité et la gestion centrale.
    """
    total_users = User.objects.count()
    total_shops = Shop.objects.count()
    total_orders = Order.objects.count()

    # Calcul du CA Global généré sur toute la plateforme
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0')

    # Activités récentes (Timeline globale)
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_shops = Shop.objects.order_by('-created_at')[:5]
    recent_orders = Order.objects.select_related('shop').order_by('-created_at')[:5]

    # Construction du flux d'activité
    activities = []
    for u in recent_users:
        activities.append({
            'type': 'user_registered',
            'title': 'Nouvel utilisateur inscrit',
            'desc': f"{u.full_name} ({u.email})",
            'time': u.date_joined,
            'icon': 'user-plus',
            'color': 'emerald'
        })
    for s in recent_shops:
        activities.append({
            'type': 'shop_created',
            'title': 'Nouvelle boutique créée',
            'desc': f"Boutique « {s.name} » par {s.owner.full_name}",
            'time': s.created_at,
            'icon': 'store',
            'color': 'brand'
        })
    for o in recent_orders:
        activities.append({
            'type': 'order_placed',
            'title': 'Nouvelle commande passée',
            'desc': f"Commande #{o.order_number} sur {o.shop.name} ({o.total_amount} FCFA)",
            'time': o.created_at,
            'icon': 'shopping-bag',
            'color': 'blue'
        })

    # Tri global des activités chronologiquement
    activities.sort(key=lambda x: x['time'], reverse=True)
    activities = activities[:10]

    # Data lists
    users = User.objects.all().order_by('-date_joined')
    shops = Shop.objects.select_related('owner').order_by('-created_at')
    orders = Order.objects.select_related('shop').order_by('-created_at')

    return render(request, 'core/super_admin/dashboard.html', {
        'total_users': total_users,
        'total_shops': total_shops,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'activities': activities,
        'users': users[:20],
        'shops': shops[:20],
        'orders': orders[:20],
    })


@login_required
@user_passes_test(staff_required, login_url='accounts:login')
def super_admin_users_partial(request):
    """Recherche et filtrage HTMX des utilisateurs."""
    q = request.GET.get('q', '').strip()
    users = User.objects.all()

    if q:
        users = users.filter(
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone__icontains=q)
        )

    return render(request, 'core/super_admin/partials/user_table.html', {'users': users[:50]})


@login_required
@user_passes_test(staff_required, login_url='accounts:login')
@require_POST
def super_admin_toggle_user_status(request, user_id):
    """Suspendre ou Réactiver un utilisateur (CRUD Admin)."""
    target_user = get_object_or_404(User, id=user_id)
    
    # Empêcher de désactiver son propre compte admin
    if target_user == request.user:
        return HttpResponse('<script>alert("Action impossible sur votre propre compte admin.");</script>', status=400)

    target_user.is_active = not target_user.is_active
    target_user.save()

    # Si la requête vient de HTMX, renvoyer la ligne mise à jour
    if request.headers.get('HX-Request'):
        users = User.objects.all().order_by('-date_joined')[:50]
        return render(request, 'core/super_admin/partials/user_table.html', {'users': users})

    messages.success(request, f"Le statut de {target_user.email} a été mis à jour.")
    return redirect('super_admin:dashboard')


@login_required
@user_passes_test(staff_required, login_url='accounts:login')
def super_admin_shops_partial(request):
    """Recherche et filtrage HTMX des boutiques."""
    q = request.GET.get('q', '').strip()
    shops = Shop.objects.select_related('owner').all()

    if q:
        shops = shops.filter(
            Q(name__icontains=q) |
            Q(slug__icontains=q) |
            Q(owner__email__icontains=q)
        )

    return render(request, 'core/super_admin/partials/shop_table.html', {'shops': shops[:50]})


@login_required
@user_passes_test(staff_required, login_url='accounts:login')
@require_POST
def super_admin_toggle_shop_status(request, shop_uuid):
    """Bloquer ou Débloquer une boutique (Modération Admin)."""
    shop = get_object_or_404(Shop, uuid=shop_uuid)
    shop.is_active = not shop.is_active
    shop.save()

    if request.headers.get('HX-Request'):
        shops = Shop.objects.select_related('owner').all().order_by('-created_at')[:50]
        return render(request, 'core/super_admin/partials/shop_table.html', {'shops': shops})

    messages.success(request, f"La boutique « {shop.name} » a été modifiée.")
    return redirect('super_admin:dashboard')


@login_required
@user_passes_test(staff_required, login_url='accounts:login')
def super_admin_orders_partial(request):
    """Recherche et filtrage HTMX des commandes globales."""
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    orders = Order.objects.select_related('shop').all()

    if q:
        orders = orders.filter(
            Q(order_number__icontains=q) |
            Q(customer_name__icontains=q) |
            Q(customer_phone__icontains=q) |
            Q(shop__name__icontains=q)
        )

    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'core/super_admin/partials/order_table.html', {'orders': orders[:50]})
