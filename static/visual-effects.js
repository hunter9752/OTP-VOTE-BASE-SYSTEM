// ========================================
// ADVANCED VISUAL EFFECTS & INTERACTIONS
// ========================================

// ========== Particle System ==========
function createParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    document.body.appendChild(particlesContainer);

    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
        particlesContainer.appendChild(particle);
    }
}

// ========== Morphing Blobs ==========
function createBlobs() {
    const blobContainer = document.createElement('div');
    blobContainer.style.position = 'fixed';
    blobContainer.style.top = '0';
    blobContainer.style.left = '0';
    blobContainer.style.width = '100%';
    blobContainer.style.height = '100%';
    blobContainer.style.pointerEvents = 'none';
    blobContainer.style.zIndex = '-1';
    blobContainer.style.overflow = 'hidden';

    for (let i = 1; i <= 3; i++) {
        const blob = document.createElement('div');
        blob.className = `blob blob-${i}`;
        blobContainer.appendChild(blob);
    }

    document.body.appendChild(blobContainer);
}

// ========== Mouse Follow Effect ==========
function initMouseFollowEffect() {
    const cards = document.querySelectorAll('.candidate-card label, .feature-card, .result-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
        });
    });
}

// ========== Parallax Scroll Effect ==========
function initParallaxEffect() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.parallax || 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// ========== Intersection Observer for Animations ==========
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Add stagger effect for children
                const children = entry.target.querySelectorAll('.stagger-child');
                children.forEach((child, index) => {
                    setTimeout(() => {
                        child.classList.add('animate-in');
                    }, index * 100);
                });
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// ========== Magnetic Button Effect ==========
function initMagneticButtons() {
    const buttons = document.querySelectorAll('.btn, .magnetic');
    
    buttons.forEach(button => {
        button.addEventListener('mousemove', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            button.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translate(0, 0)';
        });
    });
}

// ========== Cursor Trail Effect ==========
function initCursorTrail() {
    const trail = [];
    const trailLength = 20;
    
    for (let i = 0; i < trailLength; i++) {
        const dot = document.createElement('div');
        dot.className = 'cursor-trail-dot';
        dot.style.cssText = `
            position: fixed;
            width: 8px;
            height: 8px;
            background: rgba(99, 102, 241, ${1 - i / trailLength});
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease;
        `;
        document.body.appendChild(dot);
        trail.push(dot);
    }
    
    let mouseX = 0, mouseY = 0;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    function animateTrail() {
        let x = mouseX;
        let y = mouseY;
        
        trail.forEach((dot, index) => {
            const nextDot = trail[index + 1] || trail[0];
            
            dot.style.left = x - 4 + 'px';
            dot.style.top = y - 4 + 'px';
            
            x += (parseInt(nextDot.style.left) - x) * 0.3;
            y += (parseInt(nextDot.style.top) - y) * 0.3;
        });
        
        requestAnimationFrame(animateTrail);
    }
    
    animateTrail();
}

// ========== Glitch Effect on Hover ==========
function initGlitchEffect() {
    const glitchElements = document.querySelectorAll('.glitch-on-hover');
    
    glitchElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.classList.add('glitch');
            element.setAttribute('data-text', element.textContent);
            
            setTimeout(() => {
                element.classList.remove('glitch');
            }, 500);
        });
    });
}

// ========== Confetti Burst ==========
function triggerConfetti(x = 0.5, y = 0.5) {
    if (typeof confetti !== 'undefined') {
        const count = 200;
        const defaults = {
            origin: { x, y },
            zIndex: 9999
        };

        function fire(particleRatio, opts) {
            confetti(Object.assign({}, defaults, opts, {
                particleCount: Math.floor(count * particleRatio)
            }));
        }

        fire(0.25, {
            spread: 26,
            startVelocity: 55,
        });

        fire(0.2, {
            spread: 60,
        });

        fire(0.35, {
            spread: 100,
            decay: 0.91,
            scalar: 0.8
        });

        fire(0.1, {
            spread: 120,
            startVelocity: 25,
            decay: 0.92,
            scalar: 1.2
        });

        fire(0.1, {
            spread: 120,
            startVelocity: 45,
        });
    }
}

// ========== Number Counter Animation ==========
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// ========== Spotlight Effect ==========
function initSpotlightEffect() {
    const spotlightElements = document.querySelectorAll('.spotlight');
    
    spotlightElements.forEach(element => {
        element.addEventListener('mousemove', (e) => {
            const rect = element.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            element.style.setProperty('--spotlight-x', x + 'px');
            element.style.setProperty('--spotlight-y', y + 'px');
        });
    });
}

// ========== Initialize All Effects ==========
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎨 Initializing Visual Effects...');
    
    createParticles();
    createBlobs();
    initMouseFollowEffect();
    initParallaxEffect();
    initScrollAnimations();
    initMagneticButtons();
    initCursorTrail();
    initGlitchEffect();
    initSpotlightEffect();
    
    console.log('✨ Visual Effects Loaded!');
});

// Export functions for use in other scripts
window.visualEffects = {
    triggerConfetti,
    animateCounter
};
