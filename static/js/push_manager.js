/**
 * Azoria Push Notification Manager
 * Gère l'abonnement WebPush du navigateur, la demande de permission et la communication avec l'API Django.
 */

(function () {
    'use strict';

    function urlB64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const AzoriaPush = {
        isSupported: function () {
            return ('serviceWorker' in navigator) && ('PushManager' in window) && ('Notification' in window);
        },

        getPermissionState: function () {
            if (!this.isSupported()) return 'unsupported';
            return Notification.permission; // 'default', 'granted', 'denied'
        },

        getVapidPublicKey: async function () {
            try {
                const response = await fetch('/mon-compte/api/push/vapid-key/');
                const data = await response.json();
                if (data.status === 'success' && data.public_key) {
                    return data.public_key;
                }
                throw new Error('Clé VAPID introuvable');
            } catch (e) {
                console.error('Erreur récupération clé VAPID:', e);
                return null;
            }
        },

        isSubscribed: async function () {
            if (!this.isSupported()) return false;
            try {
                const registration = await navigator.serviceWorker.ready;
                const subscription = await registration.pushManager.getSubscription();
                return subscription !== null;
            } catch (e) {
                console.error('Erreur vérification abonnement:', e);
                return false;
            }
        },

        subscribe: async function () {
            if (!this.isSupported()) {
                throw new Error("Votre navigateur ne supporte pas les notifications push.");
            }

            // 1. Demande de permission native
            const permission = await Notification.requestPermission();
            if (permission !== 'granted') {
                throw new Error("Permission de notification refusée par l'utilisateur.");
            }

            // 2. Récupérer la clé publique VAPID
            const vapidKey = await this.getVapidPublicKey();
            if (!vapidKey) {
                throw new Error("Impossible de récupérer la clé VAPID du serveur.");
            }

            // 3. Obtenir le Service Worker prêt
            const registration = await navigator.serviceWorker.ready;

            // 4. Souscription auprès du service Push (Google/Mozilla/Apple)
            const applicationServerKey = urlB64ToUint8Array(vapidKey);
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: applicationServerKey
            });

            // 5. Enregistrement sur le backend Django
            const response = await fetch('/mon-compte/api/push/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') || ''
                },
                body: JSON.stringify(subscription.toJSON())
            });

            const result = await response.json();
            if (result.status === 'success') {
                return true;
            } else {
                throw new Error(result.message || "Erreur lors de l'enregistrement de l'abonnement.");
            }
        },

        unsubscribe: async function () {
            if (!this.isSupported()) return false;
            const registration = await navigator.serviceWorker.ready;
            const subscription = await registration.pushManager.getSubscription();
            if (!subscription) return true;

            const endpoint = subscription.endpoint;
            await subscription.unsubscribe();

            await fetch('/mon-compte/api/push/unsubscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') || ''
                },
                body: JSON.stringify({ endpoint: endpoint })
            });

            return true;
        },

        sendTestPush: async function () {
            const response = await fetch('/mon-compte/api/push/test/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') || ''
                }
            });
            return await response.json();
        }
    };

    window.AzoriaPush = AzoriaPush;
})();
