// Responsive Enhancement Script for Hackversity
// Enhanced mobile navigation and touch interactions

(function() {
    'use strict';
    
    // Responsive utilities
    const ResponsiveUtils = {
        // Viewport detection
        isMobile: () => window.innerWidth <= 768,
        isTablet: () => window.innerWidth > 768 && window.innerWidth <= 992,
        isDesktop: () => window.innerWidth > 992,
        
        // Touch device detection
        isTouchDevice: () => {
            return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        },
        
        // Screen orientation
        isLandscape: () => window.innerWidth > window.innerHeight,
        isPortrait: () => window.innerWidth <= window.innerHeight,
        
        // Viewport size updates
        updateViewportClass: function() {
            const body = document.body;
            body.classList.remove('mobile', 'tablet', 'desktop', 'touch', 'landscape', 'portrait');
            
            if (this.isMobile()) body.classList.add('mobile');
            else if (this.isTablet()) body.classList.add('tablet');
            else if (this.isDesktop()) body.classList.add('desktop');
            
            if (this.isTouchDevice()) body.classList.add('touch');
            
            if (this.isLandscape()) body.classList.add('landscape');
            else body.classList.add('portrait');
        }
    };
    
    // Mobile Navigation Enhancement
    const MobileNav = {
        init: function() {
            this.setupTouchInteractions();
            this.handleNavOverflow();
            this.improveScrolling();
        },
        
        setupTouchInteractions: function() {
            // Improve touch interactions for nav links
            const navLinks = document.querySelectorAll('.nav-links a');
            navLinks.forEach(link => {
                // Add touch feedback
                link.addEventListener('touchstart', function() {
                    this.style.transform = 'scale(0.95)';
                });
                
                link.addEventListener('touchend', function() {
                    this.style.transform = 'scale(1)';
                });
            });
        },
        
        handleNavOverflow: function() {
            // Handle navigation overflow on very small screens
            const navContainer = document.querySelector('.nav-container');
            const navLinks = document.querySelector('.nav-links');
            
            if (!navContainer || !navLinks) return;
            
            const checkOverflow = () => {
                if (ResponsiveUtils.isMobile() && window.innerWidth < 480) {
                    // Very small screens - stack navigation items
                    navContainer.style.flexDirection = 'column';
                    navContainer.style.alignItems = 'center';
                    navLinks.style.justifyContent = 'center';
                } else {
                    // Reset to normal layout
                    navContainer.style.flexDirection = '';
                    navContainer.style.alignItems = '';
                    navLinks.style.justifyContent = '';
                }
            };
            
            checkOverflow();
            window.addEventListener('resize', checkOverflow);
        },
        
        improveScrolling: function() {
            // Improve scrolling behavior on mobile
            if (ResponsiveUtils.isTouchDevice()) {
                document.body.style.webkitOverflowScrolling = 'touch';
                
                // Prevent scroll bouncing on iOS
                document.addEventListener('touchmove', function(e) {
                    if (e.target.closest('.messages-container') || 
                        e.target.closest('.sidebar')) {
                        return; // Allow scrolling in these containers
                    }
                    
                    const target = e.target;
                    const isScrollable = target.scrollHeight > target.clientHeight;
                    if (!isScrollable) {
                        e.preventDefault();
                    }
                }, { passive: false });
            }
        }
    };
    
    // Chat Interface Enhancements
    const ChatEnhancements = {
        init: function() {
            this.optimizeMessageDisplay();
            this.improveInputExperience();
            this.handleKeyboardResize();
        },
        
        optimizeMessageDisplay: function() {
            const messagesContainer = document.querySelector('.messages-container');
            if (!messagesContainer) return;
            
            // Optimize scrolling performance
            let scrollTimeout;
            messagesContainer.addEventListener('scroll', function() {
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(() => {
                    // Lazy load or optimize visible messages if needed
                }, 100);
            });
            
            // Auto-resize chat area based on content
            const resizeObserver = new ResizeObserver(entries => {
                if (ResponsiveUtils.isMobile()) {
                    // Adjust chat height on mobile
                    const viewport = window.visualViewport || window;
                    const availableHeight = viewport.height - 150; // Account for nav and input
                    messagesContainer.style.maxHeight = `${availableHeight}px`;
                }
            });
            
            resizeObserver.observe(messagesContainer);
        },
        
        improveInputExperience: function() {
            const inputField = document.querySelector('.input-field');
            const inputArea = document.querySelector('.input-area');
            
            if (!inputField || !inputArea) return;
            
            // Auto-resize textarea on mobile
            inputField.addEventListener('input', function() {
                if (ResponsiveUtils.isMobile()) {
                    this.style.height = 'auto';
                    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
                }
            });
            
            // Improve focus behavior on mobile
            if (ResponsiveUtils.isTouchDevice()) {
                inputField.addEventListener('focus', function() {
                    setTimeout(() => {
                        this.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'nearest' 
                        });
                    }, 300); // Wait for virtual keyboard
                });
            }
        },
        
        handleKeyboardResize: function() {
            // Handle virtual keyboard on mobile
            if (!ResponsiveUtils.isTouchDevice()) return;
            
            const viewport = window.visualViewport;
            if (!viewport) return;
            
            const chatContainer = document.querySelector('.chat-container');
            const inputArea = document.querySelector('.input-area');
            
            viewport.addEventListener('resize', () => {
                const keyboardHeight = window.innerHeight - viewport.height;
                
                if (keyboardHeight > 0 && ResponsiveUtils.isMobile()) {
                    // Virtual keyboard is open
                    if (inputArea) {
                        inputArea.style.position = 'fixed';
                        inputArea.style.bottom = '0';
                        inputArea.style.zIndex = '1001';
                    }
                    
                    if (chatContainer) {
                        chatContainer.style.paddingBottom = `${keyboardHeight + 80}px`;
                    }
                } else {
                    // Virtual keyboard is closed
                    if (inputArea) {
                        inputArea.style.position = '';
                        inputArea.style.bottom = '';
                        inputArea.style.zIndex = '';
                    }
                    
                    if (chatContainer) {
                        chatContainer.style.paddingBottom = '';
                    }
                }
            });
        }
    };
    
    // Form Enhancements
    const FormEnhancements = {
        init: function() {
            this.preventZoomOnInput();
            this.improveFormValidation();
            this.enhanceSelectElements();
        },
        
        preventZoomOnInput: function() {
            // Prevent zoom on input focus for iOS
            if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
                const inputs = document.querySelectorAll('input, textarea, select');
                inputs.forEach(input => {
                    if (!input.style.fontSize) {
                        input.style.fontSize = '16px';
                    }
                });
            }
        },
        
        improveFormValidation: function() {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                // Better error display on mobile
                form.addEventListener('invalid', function(e) {
                    if (ResponsiveUtils.isMobile()) {
                        e.preventDefault();
                        const firstInvalid = form.querySelector(':invalid');
                        if (firstInvalid) {
                            firstInvalid.focus();
                            firstInvalid.scrollIntoView({ 
                                behavior: 'smooth', 
                                block: 'center' 
                            });
                        }
                    }
                }, true);
            });
        },
        
        enhanceSelectElements: function() {
            // Improve select elements on mobile
            const selects = document.querySelectorAll('select');
            selects.forEach(select => {
                if (ResponsiveUtils.isTouchDevice()) {
                    select.style.appearance = 'none';
                    select.style.webkitAppearance = 'none';
                    // Add custom dropdown arrow if needed
                }
            });
        }
    };
    
    // Performance Optimizations
    const PerformanceOptimizations = {
        init: function() {
            this.optimizeImages();
            this.lazyLoadContent();
            this.throttleScrollEvents();
        },
        
        optimizeImages: function() {
            // Add loading="lazy" to images
            const images = document.querySelectorAll('img:not([loading])');
            images.forEach(img => {
                img.loading = 'lazy';
            });
        },
        
        lazyLoadContent: function() {
            // Lazy load non-critical content on mobile
            if (ResponsiveUtils.isMobile() && 'IntersectionObserver' in window) {
                const lazyElements = document.querySelectorAll('.lazy-load');
                const imageObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('loaded');
                            imageObserver.unobserve(entry.target);
                        }
                    });
                });
                
                lazyElements.forEach(el => imageObserver.observe(el));
            }
        },
        
        throttleScrollEvents: function() {
            // Throttle scroll events for better performance
            let ticking = false;
            
            function updateScrollEffects() {
                // Add scroll-based effects here
                ticking = false;
            }
            
            document.addEventListener('scroll', function() {
                if (!ticking) {
                    requestAnimationFrame(updateScrollEffects);
                    ticking = true;
                }
            });
        }
    };
    
    // Initialize everything when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        ResponsiveUtils.updateViewportClass();
        MobileNav.init();
        ChatEnhancements.init();
        FormEnhancements.init();
        PerformanceOptimizations.init();
        
        // Update viewport class on resize and orientation change
        window.addEventListener('resize', ResponsiveUtils.updateViewportClass);
        window.addEventListener('orientationchange', function() {
            setTimeout(ResponsiveUtils.updateViewportClass, 100);
        });
        
        // Add swipe gestures for mobile navigation
        if (ResponsiveUtils.isTouchDevice()) {
            let startX, startY, distX, distY;
            const threshold = 150;
            const restraint = 100;
            
            document.addEventListener('touchstart', function(e) {
                startX = e.changedTouches[0].pageX;
                startY = e.changedTouches[0].pageY;
            });
            
            document.addEventListener('touchend', function(e) {
                distX = e.changedTouches[0].pageX - startX;
                distY = e.changedTouches[0].pageY - startY;
                
                if (Math.abs(distX) >= threshold && Math.abs(distY) <= restraint) {
                    // Horizontal swipe detected - could be used for sidebar navigation
                    if (distX > 0) {
                        // Swipe right
                        document.body.dispatchEvent(new CustomEvent('swipeRight'));
                    } else {
                        // Swipe left
                        document.body.dispatchEvent(new CustomEvent('swipeLeft'));
                    }
                }
            });
        }
        
        console.log('✅ Responsive enhancements initialized');
    });
    
})();