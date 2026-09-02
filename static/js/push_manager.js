/**
 * Azoria Push Notification Manager
 * Gère l'abonnement WebPush du navigateur, la demande de permission et la communication avec l'API Django.
 */

(function () {
    'use strict';

    function urlB64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
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

    async function getOrRegisterSW() {
        if (!('serviceWorker' in navigator)) {
            throw new Error("Les Service Workers ne sont pas supportés par votre navigateur.");
        }
        
        let reg = await navigator.serviceWorker.getRegistration('/');
        if (!reg) {
            console.log("[Azoria Push] Enregistrement du Service Worker /sw.js...");
            reg = await navigator.serviceWorker.register('/sw.js', { scope: '/' });
        }
        
        // Attendre que le SW soit prêt ou actif
        if (reg.active) {
            return reg;
        }

        return new Promise((resolve) => {
            const timeout = setTimeout(() => {
                resolve(reg);
            }, 3000);

            navigator.serviceWorker.ready.then((readyReg) => {
                clearTimeout(timeout);
                resolve(readyReg);
            }).catch(() => {
                clearTimeout(timeout);
                resolve(reg);
            });
        });
    }

    const AzoriaPush = {
        isSupported: function () {
            const hasSW = 'serviceWorker' in navigator;
            const hasPush = 'PushManager' in window;
            const hasNotif = 'Notification' in window;
            return hasSW && hasPush && hasNotif;
        },

        getPermissionState: function () {
            if (!this.isSupported()) return 'unsupported';
            return Notification.permission; // 'default', 'granted', 'denied'
        },

        getVapidPublicKey: async function () {
            try {
                const response = await fetch('/mon-compte/api/push/vapid-key/');
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                const data = await response.json();
                if (data.status === 'success' && data.public_key) {
                    return data.public_key;
                }
                throw new Error('Clé VAPID introuvable dans la réponse serveur.');
            } catch (e) {
                console.error('[Azoria Push] Erreur récupération clé VAPID:', e);
                return null;
            }
        },

        isSubscribed: async function () {
            if (!this.isSupported()) return false;
            try {
                const registration = await getOrRegisterSW();
                if (!registration || !registration.pushManager) return false;
                const subscription = await registration.pushManager.getSubscription();
                return subscription !== null;
            } catch (e) {
                console.warn('[Azoria Push] Vérification abonnement:', e);
                return false;
            }
        },

        subscribe: async function () {
            if (!this.isSupported()) {
                throw new Error("Ce navigateur ne supporte pas les notifications push Web (nécessite HTTPS ou localhost).");
            }

            // 1. Vérification de la permission
            if (Notification.permission === 'denied') {
                throw new Error("Les notifications sont bloquées dans les paramètres de votre navigateur. Veuillez cliquer sur le cadenas 🔒 à côté de l'URL pour autoriser les notifications.");
            }

            console.log("[Azoria Push] Demande d'autorisation de notification...");
            const permission = await Notification.requestPermission();
            if (permission !== 'granted') {
                throw new Error("Vous avez refusé l'autorisation des notifications.");
            }

            // 2. Récupérer la clé VAPID
            console.log("[Azoria Push] Récupération de la clé VAPID...");
            const vapidKey = await this.getVapidPublicKey();
            if (!vapidKey) {
                throw new Error("Impossible de joindre le serveur pour récupérer la clé VAPID.");
            }

            // 3. Obtenir le Service Worker
            console.log("[Azoria Push] Obtention du Service Worker...");
            const registration = await getOrRegisterSW();
            if (!registration || !registration.pushManager) {
                throw new Error("Le gestionnaire de push du Service Worker n'est pas disponible.");
            }

            // 4. Souscription auprès du serveur de push du navigateur
            console.log("[Azoria Push] Inscription PushManager...");
            const applicationServerKey = urlB64ToUint8Array(vapidKey);
            
            let subscription = await registration.pushManager.getSubscription();
            if (!subscription) {
                subscription = await registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: applicationServerKey
                });
            }

            // 5. Sauvegarde sur le backend Django
            console.log("[Azoria Push] Enregistrement de l'abonnement sur Django...");
            const response = await fetch('/mon-compte/api/push/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') || ''
                },
                body: JSON.stringify(subscription.toJSON())
            });

            if (!response.ok) {
                throw new Error(`Erreur serveur (${response.status}) lors de l'enregistrement de l'abonnement.`);
            }

            const result = await response.json();
            if (result.status === 'success') {
                console.log("[Azoria Push] Abonnement réussi !");
                return true;
            } else {
                throw new Error(result.message || "Erreur inconnue lors de l'enregistrement.");
            }
        },

        unsubscribe: async function () {
            if (!this.isSupported()) return false;
            try {
                const registration = await getOrRegisterSW();
                if (!registration || !registration.pushManager) return true;
                
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

                console.log("[Azoria Push] Désabonnement réussi.");
                return true;
            } catch (e) {
                console.error('[Azoria Push] Erreur lors du désabonnement:', e);
                return false;
            }
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
