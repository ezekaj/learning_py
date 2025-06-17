// 🚀 REVOLUTIONARY SERVICE WORKER
// Offline-first Python Learning Platform with AI caching

const CACHE_NAME = 'pylearn-ai-v2.0.0';
const STATIC_CACHE = 'pylearn-static-v2.0.0';
const DYNAMIC_CACHE = 'pylearn-dynamic-v2.0.0';
const AI_CACHE = 'pylearn-ai-responses-v1.0.0';

// Files to cache for offline use
const STATIC_FILES = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/manifest.json',
  '/playground',
  '/lessons',
  '/quizzes',
  '/progress',
  '/achievements',
  // AI Assistant files
  '/static/js/ai-assistant.js',
  // Monaco Editor (for offline coding)
  'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs/loader.js',
  'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs/editor/editor.main.js',
  'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs/editor/editor.main.css',
  // Essential libraries
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// AI responses to cache for offline help
const AI_RESPONSES_TO_CACHE = [
  {
    key: 'basic-help',
    response: {
      hint: '💡 Here are some basic Python tips:\n\n• Use print() to display output\n• Variables store data: name = "Python"\n• Use # for comments\n• Indentation matters in Python!',
      type: 'contextual_help'
    }
  },
  {
    key: 'syntax-error-help',
    response: {
      hint: '🔧 Common syntax errors:\n\n• Missing colons after if, for, while, def\n• Incorrect indentation\n• Unmatched parentheses or quotes\n• Using = instead of == for comparison',
      type: 'error_help'
    }
  },
  {
    key: 'function-help',
    response: {
      hint: '✨ Functions in Python:\n\n• Define with: def function_name():\n• Use parameters: def greet(name):\n• Return values: return result\n• Call functions: greet("Python")',
      type: 'concept_help'
    }
  }
];

// Install event - cache static files
self.addEventListener('install', event => {
  console.log('🚀 Service Worker installing...');
  
  event.waitUntil(
    Promise.all([
      // Cache static files
      caches.open(STATIC_CACHE).then(cache => {
        console.log('📦 Caching static files...');
        return cache.addAll(STATIC_FILES);
      }),
      
      // Cache AI responses for offline help
      caches.open(AI_CACHE).then(cache => {
        console.log('🤖 Caching AI responses...');
        const cachePromises = AI_RESPONSES_TO_CACHE.map(item => {
          const request = new Request(`/offline-ai/${item.key}`);
          const response = new Response(JSON.stringify(item.response), {
            headers: { 'Content-Type': 'application/json' }
          });
          return cache.put(request, response);
        });
        return Promise.all(cachePromises);
      })
    ]).then(() => {
      console.log('✅ Service Worker installed successfully!');
      self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('🔄 Service Worker activating...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== STATIC_CACHE && 
              cacheName !== DYNAMIC_CACHE && 
              cacheName !== AI_CACHE) {
            console.log('🗑️ Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Service Worker activated!');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve cached content or fetch from network
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Handle different types of requests
  if (request.method === 'GET') {
    if (isStaticFile(request.url)) {
      // Static files - cache first
      event.respondWith(cacheFirst(request));
    } else if (isAPIRequest(request.url)) {
      // API requests - network first with offline fallback
      event.respondWith(networkFirstWithOfflineFallback(request));
    } else if (isAIRequest(request.url)) {
      // AI requests - special handling for offline AI
      event.respondWith(handleAIRequest(request));
    } else {
      // Other requests - network first
      event.respondWith(networkFirst(request));
    }
  }
});

// Cache strategies
async function cacheFirst(request) {
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
    console.log('❌ Cache first failed:', error);
    return new Response('Offline - Content not available', { status: 503 });
  }
}

async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    return new Response('Offline - Content not available', { status: 503 });
  }
}

async function networkFirstWithOfflineFallback(request) {
  try {
    const networkResponse = await fetch(request);
    return networkResponse;
  } catch (error) {
    // Return offline fallback for specific API endpoints
    if (request.url.includes('/api/execute_code')) {
      return new Response(JSON.stringify({
        success: false,
        error: 'Code execution requires internet connection',
        offline: true
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({
      error: 'Offline - This feature requires internet connection',
      offline: true
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

async function handleAIRequest(request) {
  try {
    // Try network first for real AI
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      // Cache successful AI responses
      const cache = await caches.open(AI_CACHE);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    // Fallback to cached AI responses
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Provide basic offline AI help
    return new Response(JSON.stringify({
      success: true,
      ai_response: {
        hint: '🤖 Offline AI: I\'m working with limited capabilities offline. Here are some general Python tips:\n\n• Check your syntax carefully\n• Use print() to debug your code\n• Break complex problems into smaller steps\n• Remember Python is case-sensitive!',
        type: 'offline_help'
      },
      personality: '🤖 Pythia (Offline Mode)'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Helper functions
function isStaticFile(url) {
  return url.includes('/static/') || 
         url.includes('.css') || 
         url.includes('.js') || 
         url.includes('.png') || 
         url.includes('.jpg') || 
         url.includes('.ico') ||
         url.includes('cdnjs.cloudflare.com') ||
         url.includes('cdn.tailwindcss.com');
}

function isAPIRequest(url) {
  return url.includes('/api/') && !url.includes('/api/ai_') && !url.includes('/api/code_analysis');
}

function isAIRequest(url) {
  return url.includes('/api/ai_') || 
         url.includes('/api/code_analysis') || 
         url.includes('/api/natural_language_code');
}

// Background sync for offline actions
self.addEventListener('sync', event => {
  console.log('🔄 Background sync triggered:', event.tag);
  
  if (event.tag === 'sync-progress') {
    event.waitUntil(syncUserProgress());
  } else if (event.tag === 'sync-code-snippets') {
    event.waitUntil(syncCodeSnippets());
  }
});

async function syncUserProgress() {
  try {
    // Get offline progress data
    const offlineData = await getOfflineData('user-progress');
    if (offlineData) {
      // Sync with server
      await fetch('/api/sync_progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(offlineData)
      });
      
      // Clear offline data after successful sync
      await clearOfflineData('user-progress');
      console.log('✅ User progress synced successfully');
    }
  } catch (error) {
    console.log('❌ Failed to sync user progress:', error);
  }
}

async function syncCodeSnippets() {
  try {
    const offlineSnippets = await getOfflineData('code-snippets');
    if (offlineSnippets) {
      await fetch('/api/sync_snippets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(offlineSnippets)
      });
      
      await clearOfflineData('code-snippets');
      console.log('✅ Code snippets synced successfully');
    }
  } catch (error) {
    console.log('❌ Failed to sync code snippets:', error);
  }
}

// IndexedDB helpers for offline data
async function getOfflineData(key) {
  // Simplified - in real implementation, use IndexedDB
  return null;
}

async function clearOfflineData(key) {
  // Simplified - in real implementation, use IndexedDB
  return true;
}

// Push notifications for learning reminders
self.addEventListener('push', event => {
  console.log('📱 Push notification received');
  
  const options = {
    body: 'Time for your daily Python practice! 🐍',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      url: '/playground'
    },
    actions: [
      {
        action: 'practice',
        title: 'Start Coding',
        icon: '/static/icons/play-icon.png'
      },
      {
        action: 'dismiss',
        title: 'Later',
        icon: '/static/icons/dismiss-icon.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('Python Learning Reminder', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.action === 'practice') {
    event.waitUntil(
      clients.openWindow('/playground')
    );
  } else if (event.action === 'dismiss') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

console.log('🚀 Revolutionary Service Worker loaded successfully!');
