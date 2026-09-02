// Azoria Service Worker - Fast Image & Asset Caching
const CACHE_NAME = 'azoria-v3';
const STATIC_ASSETS = [
    '/static/css/styles.css',
    '/static/js/main.js?v=2.1',
    'https://cdn.tailwindcss.com',
    'https://unpkg.com/lucide@latest',
    'https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js',
    'https://cdn.jsdelivr.net/npm/driver.js@1.3.1/dist/driver.js.iife.js',
    'https://cdn.jsdelivr.net/npm/driver.js@1.3.1/dist/driver.css',
    'https://cdn.jsdelivr.net/npm/alpinejs@3.14.8/dist/cdn.min.js',
    'https://unpkg.com/htmx.org@1.9.10'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS).catch(() => {});
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    const request = event.request;
    const url = new URL(request.url);

    // Cache-First strategy for images (/media/ and /static/images/ and WebP)
    if (request.destination === 'image' || url.pathname.startsWith('/media/') || url.pathname.includes('.webp') || url.pathname.includes('.png') || url.pathname.includes('.jpg')) {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(request).then((cachedResponse) => {
                    if (cachedResponse) {
                        // Fetch in background to update cache (Stale-While-Revalidate)
                        fetch(request).then((networkResponse) => {
                            if (networkResponse && networkResponse.status === 200) {
                                cache.put(request, networkResponse.clone());
                            }
                        }).catch(() => {});
                        return cachedResponse;
                    }
                    return fetch(request).then((networkResponse) => {
                        if (networkResponse && networkResponse.status === 200) {
                            cache.put(request, networkResponse.clone());
                        }
                        return networkResponse;
                    }).catch(() => cachedResponse);
                });
            })
        );
        return;
    }

    // Cache-First for Google Fonts & CDN scripts
    if (url.hostname.includes('googleapis.com') || url.hostname.includes('gstatic.com') || url.hostname.includes('jsdelivr.net') || url.hostname.includes('unpkg.com')) {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(request).then((cachedResponse) => {
                    return cachedResponse || fetch(request).then((networkResponse) => {
                        if (networkResponse && networkResponse.status === 200) {
                            cache.put(request, networkResponse.clone());
                        }
                        return networkResponse;
                    });
                });
            })
        );
        return;
    }

    // Network-First for HTML/AJAX dynamic pages
    event.respondWith(
        fetch(request).catch(() => {
            return caches.match(request);
        })
    );
});

// ==========================================
// 🔔 WEB PUSH NOTIFICATIONS (OFFLINE & BACKGROUND)
// ==========================================

self.addEventListener('push', (event) => {
    let payload = {
        title: '🔔 Nouvelle notification Azoria',
        body: 'Vous avez reçu une nouvelle alerte.',
        icon: '/static/images/logo-icon.png',
        badge: '/static/images/logo-icon.png',
        data: { url: '/boutique/commandes/' }
    };

    if (event.data) {
        try {
            payload = event.data.json();
        } catch (e) {
            payload.body = event.data.text();
        }
    }

    const options = {
        body: payload.body,
        icon: payload.icon || '/static/images/logo-icon.png',
        badge: payload.badge || '/static/images/logo-icon.png',
        tag: payload.tag || 'azoria-notification',
        renotify: true,
        vibrate: [200, 100, 200, 100, 200],
        requireInteraction: true,
        data: payload.data || { url: '/boutique/commandes/' },
        actions: [
            {
                action: 'open_order',
                title: 'Voir la commande 📦'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification(payload.title, options)
    );
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    const targetUrl = (event.notification.data && event.notification.data.url) ? event.notification.data.url : '/boutique/commandes/';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
            // Si un onglet Azoria est déjà ouvert, lui donner le focus et naviguer
            for (const client of clientList) {
                if (client.url && 'focus' in client) {
                    client.navigate(targetUrl);
                    return client.focus();
                }
            }
            // Sinon ouvrir un nouvel onglet vers la commande
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});
