/**
 * Service Worker for Python Learning Platform
 * Implements caching strategies for improved performance
 */

const CACHE_NAME = 'python-learning-v1';
const STATIC_CACHE = 'static-v1';
const DYNAMIC_CACHE = 'dynamic-v1';

// Resources to cache immediately
const STATIC_ASSETS = [
    '/',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/js/performance.js',
    '/static/images/logo.png',
    '/static/fonts/roboto.woff2',
    '/offline.html'
];

// Resources to cache on first request
const DYNAMIC_ASSETS = [
    '/dashboard',
    '/lessons',
    '/challenges',
    '/quizzes',
    '/progress'
];

/**
 * Install Event - Cache static assets
 */
self.addEventListener('install', event => {
    console.log('Service Worker installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static assets...');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('Static assets cached successfully');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Failed to cache static assets:', error);
            })
    );
});

/**
 * Activate Event - Clean up old caches
 */
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker activated');
                return self.clients.claim();
            })
    );
});

/**
 * Fetch Event - Implement caching strategies
 */
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip external requests
    if (url.origin !== location.origin) {
        return;
    }
    
    // Different strategies for different types of requests
    if (isStaticAsset(request.url)) {
        event.respondWith(cacheFirstStrategy(request));
    } else if (isAPIRequest(request.url)) {
        event.respondWith(networkFirstStrategy(request));
    } else if (isPageRequest(request.url)) {
        event.respondWith(staleWhileRevalidateStrategy(request));
    } else {
        event.respondWith(networkFirstStrategy(request));
    }
});

/**
 * Cache First Strategy - For static assets
 */
async function cacheFirstStrategy(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('Cache first strategy failed:', error);
        return getOfflineResponse(request);
    }
}

/**
 * Network First Strategy - For API requests
 */
async function networkFirstStrategy(request) {
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('Network failed, trying cache:', error);
        
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        return getOfflineResponse(request);
    }
}

/**
 * Stale While Revalidate Strategy - For pages
 */
async function staleWhileRevalidateStrategy(request) {
    const cache = await caches.open(DYNAMIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    const networkResponsePromise = fetch(request)
        .then(response => {
            if (response.ok) {
                cache.put(request, response.clone());
            }
            return response;
        })
        .catch(error => {
            console.log('Network request failed:', error);
            return null;
        });
    
    // Return cached response immediately if available
    if (cachedResponse) {
        // Update cache in background
        networkResponsePromise.catch(() => {}); // Ignore errors
        return cachedResponse;
    }
    
    // Wait for network response if no cache
    const networkResponse = await networkResponsePromise;
    return networkResponse || getOfflineResponse(request);
}

/**
 * Helper Functions
 */
function isStaticAsset(url) {
    return url.includes('/static/') || 
           url.endsWith('.css') || 
           url.endsWith('.js') || 
           url.endsWith('.png') || 
           url.endsWith('.jpg') || 
           url.endsWith('.jpeg') || 
           url.endsWith('.gif') || 
           url.endsWith('.svg') || 
           url.endsWith('.woff') || 
           url.endsWith('.woff2');
}

function isAPIRequest(url) {
    return url.includes('/api/');
}

function isPageRequest(url) {
    return !isStaticAsset(url) && !isAPIRequest(url) && !url.includes('.');
}

async function getOfflineResponse(request) {
    if (isPageRequest(request.url)) {
        const offlinePage = await caches.match('/offline.html');
        return offlinePage || new Response('Offline', { status: 503 });
    }
    
    if (isAPIRequest(request.url)) {
        return new Response(
            JSON.stringify({ 
                error: 'Offline', 
                message: 'This feature requires an internet connection' 
            }),
            { 
                status: 503,
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
    
    return new Response('Resource not available offline', { status: 503 });
}

/**
 * Background Sync for offline actions
 */
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    try {
        // Get pending actions from IndexedDB
        const pendingActions = await getPendingActions();
        
        for (const action of pendingActions) {
            try {
                await fetch(action.url, {
                    method: action.method,
                    headers: action.headers,
                    body: action.body
                });
                
                // Remove successful action
                await removePendingAction(action.id);
            } catch (error) {
                console.log('Background sync failed for action:', action.id);
            }
        }
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}

/**
 * Push Notifications
 */
self.addEventListener('push', event => {
    const options = {
        body: event.data ? event.data.text() : 'New update available!',
        icon: '/static/images/icon-192.png',
        badge: '/static/images/badge-72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'View',
                icon: '/static/images/checkmark.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/images/xmark.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Python Learning Platform', options)
    );
});

/**
 * Notification Click Handler
 */
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/dashboard')
        );
    }
});

/**
 * Cache Management
 */
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(clearAllCaches());
    }
});

async function clearAllCaches() {
    const cacheNames = await caches.keys();
    await Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
    );
}

/**
 * IndexedDB helpers for offline storage
 */
async function getPendingActions() {
    // Simplified - in real implementation, use IndexedDB
    return [];
}

async function removePendingAction(id) {
    // Simplified - in real implementation, use IndexedDB
    return true;
}

console.log('Service Worker loaded successfully');
