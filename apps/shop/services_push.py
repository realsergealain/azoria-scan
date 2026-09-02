import json
import logging
from django.conf import settings
from pywebpush import webpush, WebPushException

logger = logging.getLogger(__name__)


def send_web_push_notification(subscription, payload):
    """
    Envoie une notification Push chiffrée via le protocole VAPID.
    Nettoie automatiquement les abonnements expirés ou révoqués (HTTP 410 / 404).
    """
    subscription_info = {
        "endpoint": subscription.endpoint,
        "keys": {
            "p256dh": subscription.p256dh,
            "auth": subscription.auth
        }
    }

    try:
        response = webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={
                "sub": settings.VAPID_ADMIN_EMAIL
            },
            ttl=86400
        )
        return True
    except WebPushException as ex:
        logger.warning(f"Erreur WebPush pour {subscription.user.email}: {ex}")
        # Si le navigateur ou le serveur push signale que l'abonnement n'existe plus (404/410)
        if ex.response is not None and ex.response.status_code in [404, 410]:
            logger.info(f"Suppression de l'abonnement expiré/révoqué: {subscription.id}")
            subscription.delete()
        return False
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'envoi WebPush: {e}")
        return False


def notify_user_push(user, title, body, url="/boutique/commandes/", icon="/static/images/logo-icon.png", tag="azoria-order"):
    """
    Envoie une notification push à tous les appareils enregistrés d'un utilisateur.
    """
    subscriptions = user.push_subscriptions.all()
    if not subscriptions.exists():
        return 0

    payload = {
        "title": title,
        "body": body,
        "icon": icon,
        "badge": icon,
        "tag": tag,
        "data": {
            "url": url
        }
    }

    success_count = 0
    for sub in subscriptions:
        if send_web_push_notification(sub, payload):
            success_count += 1
            
    return success_count


def send_order_web_push(order):
    """
    Déclenche une notification Push au propriétaire de la boutique lors d'une nouvelle commande.
    """
    try:
        shop = order.shop
        owner = shop.owner

        customer_name = order.customer_name or "Un client"
        total_formatted = f"{int(order.total_amount):,} FCFA".replace(",", " ")
        items_count = order.items.count()
        item_text = f"{items_count} article{'s' if items_count > 1 else ''}"

        title = "🔔 Nouvelle commande reçue !"
        body = f"{customer_name} a commandé {item_text} ({total_formatted}) sur {shop.name}."
        url = f"/boutique/commandes/"

        return notify_user_push(
            user=owner,
            title=title,
            body=body,
            url=url,
            tag=f"order-{order.id}"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'alerte push pour la commande #{order.id}: {e}")
        return 0
