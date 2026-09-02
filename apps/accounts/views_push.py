import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from apps.accounts.models import PushSubscription
from apps.shop.services_push import notify_user_push


@require_GET
def get_vapid_key_api(request):
    """
    Retourne la clé publique VAPID nécessaire pour s'abonner côté navigateur.
    """
    return JsonResponse({
        "status": "success",
        "public_key": settings.VAPID_PUBLIC_KEY
    })


@login_required
@require_POST
def subscribe_push_api(request):
    """
    Enregistre ou met à jour un abonnement Push pour l'utilisateur connecté.
    """
    try:
        data = json.loads(request.body)
        endpoint = data.get('endpoint')
        keys = data.get('keys', {})
        p256dh = keys.get('p256dh')
        auth = keys.get('auth')

        if not endpoint or not p256dh or not auth:
            return JsonResponse({"status": "error", "message": "Données d'abonnement incomplètes."}, status=400)

        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

        subscription, created = PushSubscription.objects.update_or_create(
            endpoint=endpoint,
            defaults={
                'user': request.user,
                'p256dh': p256dh,
                'auth': auth,
                'user_agent': user_agent
            }
        )

        return JsonResponse({
            "status": "success",
            "message": "Notifications activées avec succès !",
            "created": created
        })
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "JSON invalide."}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
@require_POST
def unsubscribe_push_api(request):
    """
    Désabonne un appareil des notifications push.
    """
    try:
        data = json.loads(request.body)
        endpoint = data.get('endpoint')
        if endpoint:
            PushSubscription.objects.filter(user=request.user, endpoint=endpoint).delete()
        return JsonResponse({"status": "success", "message": "Désabonnement réussi."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
@require_POST
def test_push_api(request):
    """
    Envoie immédiatement une notification Push de test sur l'appareil du vendeur.
    """
    count = notify_user_push(
        user=request.user,
        title="🔔 Test Azoria — Notification Active !",
        body="Félicitations ! Vous recevrez désormais vos alertes de commandes même en quittant le site.",
        url="/boutique/commandes/"
    )

    if count > 0:
        return JsonResponse({
            "status": "success",
            "message": f"Notification envoyée avec succès sur {count} appareil(s) !"
        })
    else:
        return JsonResponse({
            "status": "warning",
            "message": "Aucun appareil abonné trouvé. Veuillez d'abord autoriser les notifications."
        }, status=400)
