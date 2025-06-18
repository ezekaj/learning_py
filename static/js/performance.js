/**
 * Web Performance Optimization Module
 * Implements lazy loading, caching, and performance monitoring
 */

class WebPerformanceOptimizer {
    constructor() {
        this.cache = new Map();
        this.lazyImages = [];
        this.performanceMetrics = {};
        this.init();
    }

    init() {
        this.setupLazyLoading();
        this.setupServiceWorker();
        this.setupPerformanceMonitoring();
        this.optimizeAssetLoading();
    }

    /**
     * Lazy Loading Implementation
     */
    setupLazyLoading() {
        // Lazy load images
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));

        // Lazy load content sections
        const contentSections = document.querySelectorAll('.lazy-content');
        const contentObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadContent(entry.target);
                }
            });
        });

        contentSections.forEach(section => contentObserver.observe(section));
    }

    /**
     * Service Worker Setup for Caching
     */
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }
    }

    /**
     * Performance Monitoring
     */
    setupPerformanceMonitoring() {
        // Monitor page load performance
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            this.performanceMetrics = {
                loadTime: perfData.loadEventEnd - perfData.loadEventStart,
                domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                firstPaint: this.getFirstPaint(),
                firstContentfulPaint: this.getFirstContentfulPaint()
            };

            // Send metrics to server (optional)
            this.sendPerformanceMetrics();
        });

        // Monitor resource loading
        const observer = new PerformanceObserver((list) => {
            list.getEntries().forEach((entry) => {
                if (entry.duration > 1000) { // Log slow resources
                    console.warn('Slow resource:', entry.name, entry.duration + 'ms');
                }
            });
        });
        observer.observe({entryTypes: ['resource']});
    }

    /**
     * Optimize Asset Loading
     */
    optimizeAssetLoading() {
        // Preload critical resources
        this.preloadCriticalResources();
        
        // Defer non-critical JavaScript
        this.deferNonCriticalJS();
        
        // Optimize font loading
        this.optimizeFontLoading();
    }

    preloadCriticalResources() {
        const criticalResources = [
            '/static/css/main.css',
            '/static/js/main.js'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            document.head.appendChild(link);
        });
    }

    deferNonCriticalJS() {
        const scripts = document.querySelectorAll('script[data-defer]');
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.src = script.src;
            newScript.defer = true;
            script.parentNode.replaceChild(newScript, script);
        });
    }

    optimizeFontLoading() {
        // Use font-display: swap for better performance
        const style = document.createElement('style');
        style.textContent = `
            @font-face {
                font-family: 'Roboto';
                src: url('/static/fonts/roboto.woff2') format('woff2');
                font-display: swap;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Content Loading with Caching
     */
    async loadContent(element) {
        const url = element.dataset.src;
        if (!url) return;

        // Check cache first
        if (this.cache.has(url)) {
            element.innerHTML = this.cache.get(url);
            element.classList.remove('lazy-content');
            return;
        }

        try {
            const response = await fetch(url);
            const content = await response.text();
            
            // Cache the content
            this.cache.set(url, content);
            
            // Load content
            element.innerHTML = content;
            element.classList.remove('lazy-content');
            
        } catch (error) {
            console.error('Failed to load content:', error);
            element.innerHTML = '<p>Failed to load content</p>';
        }
    }

    /**
     * Performance Metrics Helpers
     */
    getFirstPaint() {
        const paintEntries = performance.getEntriesByType('paint');
        const firstPaint = paintEntries.find(entry => entry.name === 'first-paint');
        return firstPaint ? firstPaint.startTime : 0;
    }

    getFirstContentfulPaint() {
        const paintEntries = performance.getEntriesByType('paint');
        const fcp = paintEntries.find(entry => entry.name === 'first-contentful-paint');
        return fcp ? fcp.startTime : 0;
    }

    sendPerformanceMetrics() {
        // Send metrics to server for monitoring
        fetch('/api/performance-metrics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.performanceMetrics)
        }).catch(error => {
            console.log('Failed to send performance metrics:', error);
        });
    }

    /**
     * Image Optimization
     */
    optimizeImages() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            // Add loading="lazy" for native lazy loading
            if (!img.hasAttribute('loading')) {
                img.loading = 'lazy';
            }

            // Optimize image format based on browser support
            if (this.supportsWebP() && !img.src.includes('.webp')) {
                const webpSrc = img.src.replace(/\.(jpg|jpeg|png)$/, '.webp');
                img.src = webpSrc;
            }
        });
    }

    supportsWebP() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }

    /**
     * Network Optimization
     */
    setupNetworkOptimization() {
        // Implement request batching
        this.requestQueue = [];
        this.batchTimeout = null;

        // Prefetch likely next pages
        this.setupPrefetching();
    }

    batchRequests(url, data) {
        this.requestQueue.push({ url, data });
        
        if (this.batchTimeout) {
            clearTimeout(this.batchTimeout);
        }

        this.batchTimeout = setTimeout(() => {
            this.processBatchedRequests();
        }, 100); // Batch requests for 100ms
    }

    async processBatchedRequests() {
        if (this.requestQueue.length === 0) return;

        const requests = [...this.requestQueue];
        this.requestQueue = [];

        try {
            const response = await fetch('/api/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ requests })
            });

            const results = await response.json();
            this.handleBatchedResults(results);
        } catch (error) {
            console.error('Batch request failed:', error);
        }
    }

    setupPrefetching() {
        // Prefetch likely next pages based on user behavior
        const links = document.querySelectorAll('a[href^="/"]');
        const linkObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const link = entry.target;
                    this.prefetchPage(link.href);
                }
            });
        });

        links.forEach(link => linkObserver.observe(link));
    }

    prefetchPage(url) {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        document.head.appendChild(link);
    }

    /**
     * Memory Management
     */
    cleanupCache() {
        // Clean up cache when it gets too large
        if (this.cache.size > 50) {
            const entries = Array.from(this.cache.entries());
            const toDelete = entries.slice(0, 10); // Remove oldest 10 entries
            toDelete.forEach(([key]) => this.cache.delete(key));
        }
    }

    /**
     * Public API
     */
    getPerformanceMetrics() {
        return this.performanceMetrics;
    }

    clearCache() {
        this.cache.clear();
    }
}

// Initialize performance optimizer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.performanceOptimizer = new WebPerformanceOptimizer();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WebPerformanceOptimizer;
}
