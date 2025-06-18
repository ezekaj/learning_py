/**
 * Mobile-Specific JavaScript for Python Learning Platform
 * Handles touch interactions, gestures, and mobile-specific features
 */

class MobileOptimizer {
    constructor() {
        this.isMobile = this.detectMobile();
        this.isTouch = 'ontouchstart' in window;
        this.orientation = this.getOrientation();
        
        if (this.isMobile) {
            this.init();
        }
    }

    init() {
        this.setupTouchHandlers();
        this.setupGestureHandlers();
        this.setupOrientationHandler();
        this.setupMobileNavigation();
        this.setupMobileOptimizations();
        this.setupOfflineHandling();
        this.setupPullToRefresh();
    }

    detectMobile() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        return /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent) ||
               window.innerWidth <= 768;
    }

    getOrientation() {
        return window.innerHeight > window.innerWidth ? 'portrait' : 'landscape';
    }

    /**
     * Touch Event Handlers
     */
    setupTouchHandlers() {
        // Improve touch responsiveness
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true });
        
        // Add touch feedback to buttons
        this.addTouchFeedback();
        
        // Prevent zoom on double tap for specific elements
        this.preventDoubleTabZoom();
    }

    handleTouchStart(event) {
        const target = event.target.closest('.btn, .card, .quiz-option');
        if (target) {
            target.classList.add('touch-active');
        }
    }

    handleTouchEnd(event) {
        const target = event.target.closest('.btn, .card, .quiz-option');
        if (target) {
            setTimeout(() => {
                target.classList.remove('touch-active');
            }, 150);
        }
    }

    addTouchFeedback() {
        const style = document.createElement('style');
        style.textContent = `
            .touch-active {
                transform: scale(0.98);
                opacity: 0.8;
                transition: all 0.1s ease;
            }
            
            .btn.touch-active {
                background-color: rgba(0, 0, 0, 0.1);
            }
        `;
        document.head.appendChild(style);
    }

    preventDoubleTabZoom() {
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (event) => {
            const now = new Date().getTime();
            if (now - lastTouchEnd <= 300) {
                const target = event.target.closest('.no-zoom');
                if (target) {
                    event.preventDefault();
                }
            }
            lastTouchEnd = now;
        }, false);
    }

    /**
     * Gesture Handlers
     */
    setupGestureHandlers() {
        this.setupSwipeGestures();
        this.setupPinchZoom();
    }

    setupSwipeGestures() {
        let startX, startY, startTime;
        
        document.addEventListener('touchstart', (e) => {
            const touch = e.touches[0];
            startX = touch.clientX;
            startY = touch.clientY;
            startTime = Date.now();
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            if (!startX || !startY) return;
            
            const touch = e.changedTouches[0];
            const endX = touch.clientX;
            const endY = touch.clientY;
            const endTime = Date.now();
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            const deltaTime = endTime - startTime;
            
            // Check if it's a swipe (fast movement)
            if (deltaTime < 300 && Math.abs(deltaX) > 50) {
                const direction = deltaX > 0 ? 'right' : 'left';
                this.handleSwipe(direction, e.target);
            }
            
            startX = startY = null;
        }, { passive: true });
    }

    handleSwipe(direction, target) {
        // Handle swipe on specific elements
        const swipeableElement = target.closest('.swipeable');
        if (swipeableElement) {
            const event = new CustomEvent('swipe', {
                detail: { direction, element: swipeableElement }
            });
            swipeableElement.dispatchEvent(event);
        }
        
        // Navigation swipes
        if (direction === 'right' && window.scrollX === 0) {
            this.handleBackGesture();
        }
    }

    handleBackGesture() {
        if (window.history.length > 1) {
            window.history.back();
        }
    }

    setupPinchZoom() {
        let initialDistance = 0;
        let currentScale = 1;
        
        document.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                initialDistance = this.getDistance(e.touches[0], e.touches[1]);
            }
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            if (e.touches.length === 2) {
                const currentDistance = this.getDistance(e.touches[0], e.touches[1]);
                const scale = currentDistance / initialDistance;
                
                const zoomableElement = e.target.closest('.zoomable');
                if (zoomableElement) {
                    e.preventDefault();
                    currentScale *= scale;
                    currentScale = Math.max(0.5, Math.min(3, currentScale));
                    zoomableElement.style.transform = `scale(${currentScale})`;
                }
            }
        });
    }

    getDistance(touch1, touch2) {
        const dx = touch1.clientX - touch2.clientX;
        const dy = touch1.clientY - touch2.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    /**
     * Orientation Handler
     */
    setupOrientationHandler() {
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.orientation = this.getOrientation();
                this.handleOrientationChange();
            }, 100);
        });
        
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    handleOrientationChange() {
        document.body.classList.remove('portrait', 'landscape');
        document.body.classList.add(this.orientation);
        
        // Adjust layout for orientation
        this.adjustLayoutForOrientation();
        
        // Trigger custom event
        window.dispatchEvent(new CustomEvent('orientationChanged', {
            detail: { orientation: this.orientation }
        }));
    }

    adjustLayoutForOrientation() {
        const codeEditors = document.querySelectorAll('.code-editor');
        codeEditors.forEach(editor => {
            if (this.orientation === 'landscape') {
                editor.style.height = '300px';
            } else {
                editor.style.height = '200px';
            }
        });
    }

    handleResize() {
        // Update mobile detection on resize
        this.isMobile = this.detectMobile();
        
        // Adjust viewport height for mobile browsers
        this.adjustViewportHeight();
    }

    adjustViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }

    /**
     * Mobile Navigation
     */
    setupMobileNavigation() {
        this.createMobileMenu();
        this.setupBottomNavigation();
    }

    createMobileMenu() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;
        
        // Create mobile menu toggle
        const toggleButton = document.createElement('button');
        toggleButton.className = 'mobile-menu-toggle';
        toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
        toggleButton.addEventListener('click', this.toggleMobileMenu.bind(this));
        
        // Add to navbar
        navbar.appendChild(toggleButton);
        
        // Create mobile menu overlay
        const overlay = document.createElement('div');
        overlay.className = 'mobile-menu-overlay';
        overlay.addEventListener('click', this.closeMobileMenu.bind(this));
        document.body.appendChild(overlay);
    }

    toggleMobileMenu() {
        const menu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        
        if (menu && overlay) {
            menu.classList.toggle('active');
            overlay.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        }
    }

    closeMobileMenu() {
        const menu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        
        if (menu && overlay) {
            menu.classList.remove('active');
            overlay.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    }

    setupBottomNavigation() {
        // Create bottom navigation for mobile
        const bottomNav = document.createElement('div');
        bottomNav.className = 'bottom-navigation mobile-only';
        bottomNav.innerHTML = `
            <a href="/dashboard" class="bottom-nav-item">
                <i class="fas fa-home"></i>
                <span>Home</span>
            </a>
            <a href="/lessons" class="bottom-nav-item">
                <i class="fas fa-book"></i>
                <span>Lessons</span>
            </a>
            <a href="/challenges" class="bottom-nav-item">
                <i class="fas fa-code"></i>
                <span>Code</span>
            </a>
            <a href="/progress" class="bottom-nav-item">
                <i class="fas fa-chart-line"></i>
                <span>Progress</span>
            </a>
        `;
        
        document.body.appendChild(bottomNav);
        
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .bottom-navigation {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: white;
                border-top: 1px solid #e9ecef;
                display: flex;
                justify-content: space-around;
                padding: 0.5rem 0;
                z-index: 1000;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            }
            
            .bottom-nav-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-decoration: none;
                color: #6c757d;
                padding: 0.5rem;
                min-width: 60px;
                transition: color 0.3s ease;
            }
            
            .bottom-nav-item:hover,
            .bottom-nav-item.active {
                color: #667eea;
            }
            
            .bottom-nav-item i {
                font-size: 1.2rem;
                margin-bottom: 0.25rem;
            }
            
            .bottom-nav-item span {
                font-size: 0.7rem;
            }
            
            body {
                padding-bottom: 70px;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Mobile Optimizations
     */
    setupMobileOptimizations() {
        this.optimizeScrolling();
        this.optimizeFormInputs();
        this.setupLazyLoading();
    }

    optimizeScrolling() {
        // Smooth scrolling for mobile
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Momentum scrolling for iOS
        document.body.style.webkitOverflowScrolling = 'touch';
    }

    optimizeFormInputs() {
        // Add appropriate input types for mobile keyboards
        const emailInputs = document.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.setAttribute('autocomplete', 'email');
            input.setAttribute('autocapitalize', 'none');
        });
        
        const passwordInputs = document.querySelectorAll('input[type="password"]');
        passwordInputs.forEach(input => {
            input.setAttribute('autocomplete', 'current-password');
        });
        
        // Prevent zoom on input focus
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                if (this.isMobile) {
                    input.style.fontSize = '16px';
                }
            });
        });
    }

    setupLazyLoading() {
        // Enhanced lazy loading for mobile
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px'
        });
        
        images.forEach(img => imageObserver.observe(img));
    }

    /**
     * Offline Handling
     */
    setupOfflineHandling() {
        window.addEventListener('online', this.handleOnline.bind(this));
        window.addEventListener('offline', this.handleOffline.bind(this));
        
        // Check initial state
        if (!navigator.onLine) {
            this.handleOffline();
        }
    }

    handleOnline() {
        this.showConnectionStatus('online');
        // Sync any pending data
        this.syncPendingData();
    }

    handleOffline() {
        this.showConnectionStatus('offline');
    }

    showConnectionStatus(status) {
        const existingToast = document.querySelector('.connection-toast');
        if (existingToast) {
            existingToast.remove();
        }
        
        const toast = document.createElement('div');
        toast.className = `connection-toast ${status}`;
        toast.innerHTML = `
            <i class="fas fa-${status === 'online' ? 'wifi' : 'wifi-slash'}"></i>
            <span>${status === 'online' ? 'Back online' : 'You\'re offline'}</span>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    syncPendingData() {
        // Implement data synchronization logic
        console.log('Syncing pending data...');
    }

    /**
     * Pull to Refresh
     */
    setupPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pulling = false;
        
        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                pulling = true;
            }
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            if (pulling) {
                currentY = e.touches[0].clientY;
                const pullDistance = currentY - startY;
                
                if (pullDistance > 100) {
                    this.showPullToRefreshIndicator();
                }
            }
        }, { passive: true });
        
        document.addEventListener('touchend', () => {
            if (pulling && currentY - startY > 100) {
                this.triggerRefresh();
            }
            pulling = false;
            this.hidePullToRefreshIndicator();
        }, { passive: true });
    }

    showPullToRefreshIndicator() {
        // Show pull to refresh indicator
        console.log('Show pull to refresh indicator');
    }

    hidePullToRefreshIndicator() {
        // Hide pull to refresh indicator
        console.log('Hide pull to refresh indicator');
    }

    triggerRefresh() {
        // Trigger page refresh
        window.location.reload();
    }

    /**
     * Public API
     */
    isMobileDevice() {
        return this.isMobile;
    }

    getCurrentOrientation() {
        return this.orientation;
    }

    vibrate(pattern = [100]) {
        if ('vibrate' in navigator) {
            navigator.vibrate(pattern);
        }
    }
}

// Initialize mobile optimizer
let mobileOptimizer;
document.addEventListener('DOMContentLoaded', () => {
    mobileOptimizer = new MobileOptimizer();
    
    // Make it globally available
    window.mobileOptimizer = mobileOptimizer;
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileOptimizer;
}
