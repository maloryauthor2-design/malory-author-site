/**
 * animations.js — Premium interaction engine for Malory's author website
 *
 * Features:
 *   1. Scroll-triggered reveal animations (staggered fade + slide)
 *   2. Reactive starfield background (stars scatter from cursor)
 *   3. Custom cursor with gold particle trail
 *   4. Magnetic hover on CTA buttons
 *   5. Interactive book cover spotlight (light follows cursor)
 *   6. Scroll-triggered heading text reveal with gold shimmer
 *   7. Book cover image loading shimmer placeholders
 *   8. Smooth page transitions (View Transitions API + fallback)
 *
 * All animations respect prefers-reduced-motion.
 * Touch devices get a clean, static experience.
 *
 * Usage: <script src="animations.js" defer></script>
 */

(function () {
    'use strict';

    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    let mouseX = -1000, mouseY = -1000;

    // Track mouse globally for multiple features
    if (!isTouch) {
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });
    }

    /* =========================================
       1. SCROLL-TRIGGERED REVEAL ANIMATIONS
       ========================================= */
    document.addEventListener('DOMContentLoaded', () => {
        if (motionQuery.matches) return;

        const ANIMATED_SELECTORS = [
            'main h2',
            'main h3',
            '.book-container',
            '.series-book-card',
            '.static-card',
            '.review-card',
            '.series-promo-box',
            '.continuity-box',
            '.about-container',
            '.award-callout',
            '.social-proof-subheading',
            '.guide-card',
            '.publisher-strip',
            '.review-aggregate'
        ].join(', ');

        const elements = document.querySelectorAll(ANIMATED_SELECTORS);
        if (!elements.length) return;

        elements.forEach(el => el.classList.add('reveal'));

        const observer = new IntersectionObserver((entries) => {
            const visible = entries
                .filter(e => e.isIntersecting)
                .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

            visible.forEach((entry, i) => {
                const delay = Math.min(i * 80, 400);
                setTimeout(() => entry.target.classList.add('visible'), delay);
                observer.unobserve(entry.target);
            });
        }, {
            threshold: 0.07,
            rootMargin: '0px 0px -30px 0px'
        });

        elements.forEach(el => observer.observe(el));

        motionQuery.addEventListener('change', (e) => {
            if (e.matches) {
                document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
                    el.classList.add('visible');
                    observer.unobserve(el);
                });
            }
        });
    });

    /* =========================================
       2. REACTIVE STARFIELD
       ========================================= */
    (function () {
        if (motionQuery.matches) return;

        const canvas = document.createElement('canvas');
        canvas.id = 'starfield';
        canvas.setAttribute('aria-hidden', 'true');
        document.body.prepend(canvas);

        const ctx = canvas.getContext('2d');
        let w, h, stars, raf;
        const STAR_COUNT = 80;
        const MAX_SPEED = 0.15;
        const SCATTER_RADIUS = 120;
        const SCATTER_FORCE = 0.8;

        function resize() {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
        }

        function createStars() {
            stars = [];
            for (let i = 0; i < STAR_COUNT; i++) {
                const x = Math.random() * w;
                const y = Math.random() * h;
                stars.push({
                    x, y,
                    homeX: x, homeY: y,
                    r: Math.random() * 1.2 + 0.3,
                    dx: (Math.random() - 0.5) * MAX_SPEED,
                    dy: (Math.random() - 0.5) * MAX_SPEED,
                    alpha: Math.random() * 0.6 + 0.2
                });
            }
        }

        function draw() {
            ctx.clearRect(0, 0, w, h);

            // Get cursor position in viewport (starfield is position:fixed)
            const cx = mouseX;
            const cy = mouseY;

            for (const s of stars) {
                // Normal drift
                s.homeX += s.dx;
                s.homeY += s.dy;
                if (s.homeX < 0) s.homeX = w;
                if (s.homeX > w) s.homeX = 0;
                if (s.homeY < 0) s.homeY = h;
                if (s.homeY > h) s.homeY = 0;

                // Scatter from cursor
                let targetX = s.homeX;
                let targetY = s.homeY;

                if (cx > 0 && cy > 0) {
                    const ddx = s.homeX - cx;
                    const ddy = s.homeY - cy;
                    const dist = Math.sqrt(ddx * ddx + ddy * ddy);
                    if (dist < SCATTER_RADIUS && dist > 0) {
                        const force = (1 - dist / SCATTER_RADIUS) * SCATTER_FORCE;
                        targetX = s.homeX + (ddx / dist) * force * 60;
                        targetY = s.homeY + (ddy / dist) * force * 60;
                    }
                }

                // Smooth lerp toward target
                s.x += (targetX - s.x) * 0.08;
                s.y += (targetY - s.y) * 0.08;

                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(212, 175, 55, ' + s.alpha + ')';
                ctx.fill();
            }
            raf = requestAnimationFrame(draw);
        }

        resize();
        createStars();
        draw();

        document.addEventListener('visibilitychange', () => {
            if (document.hidden) cancelAnimationFrame(raf);
            else draw();
        });

        window.addEventListener('resize', resize);

        motionQuery.addEventListener('change', (e) => {
            if (e.matches) { cancelAnimationFrame(raf); canvas.remove(); }
        });
    })();

    /* =========================================
       3. CUSTOM CURSOR WITH GOLD PARTICLE TRAIL
       ========================================= */
    (function () {
        if (motionQuery.matches || isTouch) return;

        // Inject cursor styles
        const style = document.createElement('style');
        style.textContent = `
            body { cursor: none; }
            a, button, [role="button"], .buy-button, .guide-btn, .tab-link, .static-card { cursor: none; }
            .cursor-dot {
                position: fixed;
                top: 0; left: 0;
                width: 8px; height: 8px;
                background: #d4af37;
                border-radius: 50%;
                pointer-events: none;
                z-index: 99999;
                transform: translate(-50%, -50%);
                transition: width 0.15s, height 0.15s, background 0.15s;
                mix-blend-mode: screen;
            }
            .cursor-dot.hovering {
                width: 14px; height: 14px;
                background: rgba(212, 175, 55, 0.6);
            }
            .cursor-ring {
                position: fixed;
                top: 0; left: 0;
                width: 36px; height: 36px;
                border: 1.5px solid rgba(212, 175, 55, 0.35);
                border-radius: 50%;
                pointer-events: none;
                z-index: 99998;
                transform: translate(-50%, -50%);
                transition: width 0.25s, height 0.25s, border-color 0.25s;
            }
            .cursor-ring.hovering {
                width: 50px; height: 50px;
                border-color: rgba(212, 175, 55, 0.6);
            }
        `;
        document.head.appendChild(style);

        const dot = document.createElement('div');
        dot.className = 'cursor-dot';
        const ring = document.createElement('div');
        ring.className = 'cursor-ring';
        document.body.appendChild(dot);
        document.body.appendChild(ring);

        let ringX = 0, ringY = 0;

        // Particle pool
        const particles = [];
        const MAX_PARTICLES = 30;
        const particleCanvas = document.createElement('canvas');
        particleCanvas.id = 'cursor-particles';
        particleCanvas.setAttribute('aria-hidden', 'true');
        Object.assign(particleCanvas.style, {
            position: 'fixed', top: '0', left: '0',
            width: '100%', height: '100%',
            pointerEvents: 'none', zIndex: '99997'
        });
        document.body.appendChild(particleCanvas);
        const pCtx = particleCanvas.getContext('2d');

        function resizeParticleCanvas() {
            particleCanvas.width = window.innerWidth;
            particleCanvas.height = window.innerHeight;
        }
        resizeParticleCanvas();
        window.addEventListener('resize', resizeParticleCanvas);

        let lastSpawn = 0;
        let prevMX = 0, prevMY = 0;

        function updateCursor() {
            // Dot follows exactly
            dot.style.left = mouseX + 'px';
            dot.style.top = mouseY + 'px';

            // Ring follows with smooth lag
            ringX += (mouseX - ringX) * 0.12;
            ringY += (mouseY - ringY) * 0.12;
            ring.style.left = ringX + 'px';
            ring.style.top = ringY + 'px';

            // Spawn particles on movement
            const now = performance.now();
            const speed = Math.sqrt((mouseX - prevMX) ** 2 + (mouseY - prevMY) ** 2);
            if (speed > 3 && now - lastSpawn > 40 && particles.length < MAX_PARTICLES) {
                particles.push({
                    x: mouseX, y: mouseY,
                    r: Math.random() * 2 + 1,
                    alpha: 0.6,
                    dx: (Math.random() - 0.5) * 0.5,
                    dy: (Math.random() - 0.5) * 0.5 - 0.3,
                    life: 1
                });
                lastSpawn = now;
            }
            prevMX = mouseX;
            prevMY = mouseY;

            // Draw particles
            pCtx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                p.x += p.dx;
                p.y += p.dy;
                p.life -= 0.025;
                p.alpha = p.life * 0.6;
                if (p.life <= 0) {
                    particles.splice(i, 1);
                    continue;
                }
                pCtx.beginPath();
                pCtx.arc(p.x, p.y, p.r * p.life, 0, Math.PI * 2);
                pCtx.fillStyle = `rgba(212, 175, 55, ${p.alpha})`;
                pCtx.fill();
            }

            requestAnimationFrame(updateCursor);
        }
        requestAnimationFrame(updateCursor);

        // Hover state for interactive elements
        const hoverTargets = 'a, button, [role="button"], .buy-button, .guide-btn, .tab-link, .static-card, input';
        document.addEventListener('mouseover', (e) => {
            if (e.target.closest(hoverTargets)) {
                dot.classList.add('hovering');
                ring.classList.add('hovering');
            }
        });
        document.addEventListener('mouseout', (e) => {
            if (e.target.closest(hoverTargets)) {
                dot.classList.remove('hovering');
                ring.classList.remove('hovering');
            }
        });
    })();

    /* =========================================
       4. MAGNETIC HOVER ON CTA BUTTONS
       ========================================= */
    (function () {
        if (motionQuery.matches || isTouch) return;

        document.addEventListener('DOMContentLoaded', () => {
            const magnetTargets = document.querySelectorAll('.buy-button, .guide-btn, .btn-pulse');

            magnetTargets.forEach(btn => {
                btn.addEventListener('mousemove', (e) => {
                    const rect = btn.getBoundingClientRect();
                    const bx = rect.left + rect.width / 2;
                    const by = rect.top + rect.height / 2;
                    const dx = (e.clientX - bx) * 0.2;
                    const dy = (e.clientY - by) * 0.2;
                    btn.style.transform = `translate(${dx}px, ${dy}px)`;
                });

                btn.addEventListener('mouseleave', () => {
                    btn.style.transform = '';
                    btn.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1)';
                    setTimeout(() => { btn.style.transition = ''; }, 400);
                });
            });
        });
    })();

    /* =========================================
       5. INTERACTIVE BOOK COVER SPOTLIGHT
       ========================================= */
    (function () {
        if (motionQuery.matches || isTouch) return;

        // Inject spotlight CSS
        const style = document.createElement('style');
        style.textContent = `
            .series-book-card img, .book-cover {
                position: relative;
            }
            .spotlight-wrap {
                position: relative;
                display: inline-block;
                overflow: hidden;
                border-radius: 4px;
            }
            .spotlight-wrap::after {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: radial-gradient(circle 120px at var(--spot-x, 50%) var(--spot-y, 50%),
                    rgba(255, 255, 255, 0.12) 0%,
                    rgba(255, 255, 255, 0.04) 40%,
                    transparent 70%);
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s ease;
                z-index: 2;
            }
            .spotlight-wrap:hover::after {
                opacity: 1;
            }
        `;
        document.head.appendChild(style);

        document.addEventListener('DOMContentLoaded', () => {
            // Wrap each book cover image in a spotlight container
            document.querySelectorAll('.series-book-card img, .book-cover').forEach(img => {
                // Don't wrap if already wrapped
                if (img.parentElement.classList.contains('spotlight-wrap')) return;
                const wrap = document.createElement('div');
                wrap.className = 'spotlight-wrap';
                img.parentNode.insertBefore(wrap, img);
                wrap.appendChild(img);

                wrap.addEventListener('mousemove', (e) => {
                    const rect = wrap.getBoundingClientRect();
                    const x = ((e.clientX - rect.left) / rect.width) * 100;
                    const y = ((e.clientY - rect.top) / rect.height) * 100;
                    wrap.style.setProperty('--spot-x', x + '%');
                    wrap.style.setProperty('--spot-y', y + '%');
                });
            });
        });
    })();

    /* =========================================
       6. SCROLL-TRIGGERED HEADING TEXT REVEAL
       ========================================= */
    (function () {
        if (motionQuery.matches) return;

        // Inject shimmer CSS
        const style = document.createElement('style');
        style.textContent = `
            .text-reveal-wrap {
                display: inline;
            }
            .text-reveal-char {
                display: inline-block;
                opacity: 0;
                transform: translateY(12px);
                transition: opacity 0.4s ease, transform 0.4s ease;
            }
            .text-reveal-char.shown {
                opacity: 1;
                transform: translateY(0);
            }
            /* Gold shimmer sweep */
            @keyframes shimmer-sweep {
                0%   { background-position: -200% center; }
                100% { background-position: 200% center; }
            }
            .text-shimmer {
                background: linear-gradient(
                    90deg,
                    currentColor 0%,
                    #d4af37 45%,
                    #f5e6a3 50%,
                    #d4af37 55%,
                    currentColor 100%
                );
                background-size: 200% auto;
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer-sweep 1.5s ease forwards;
                animation-delay: 0.6s;
            }
        `;
        document.head.appendChild(style);

        document.addEventListener('DOMContentLoaded', () => {
            // Only target major series headings, not every h2
            const headings = document.querySelectorAll('.series-header h2');

            headings.forEach(h => {
                const text = h.textContent;
                h.innerHTML = '';
                const words = text.split(' ');
                words.forEach((word, wi) => {
                    if (wi > 0) {
                        const space = document.createElement('span');
                        space.innerHTML = '&nbsp;';
                        space.className = 'text-reveal-char';
                        h.appendChild(space);
                    }
                    [...word].forEach(char => {
                        const span = document.createElement('span');
                        span.className = 'text-reveal-char';
                        span.textContent = char;
                        h.appendChild(span);
                    });
                });

                const revealObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const chars = h.querySelectorAll('.text-reveal-char');
                            chars.forEach((c, i) => {
                                setTimeout(() => c.classList.add('shown'), i * 30);
                            });
                            // Add shimmer after all chars revealed
                            setTimeout(() => h.classList.add('text-shimmer'), chars.length * 30 + 200);
                            revealObserver.unobserve(h);
                        }
                    });
                }, { threshold: 0.5 });

                revealObserver.observe(h);
            });
        });
    })();

    /* =========================================
       7. BOOK COVER IMAGE LOADING SHIMMER
       ========================================= */
    (function () {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes shimmer-load {
                0%   { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
            .img-shimmer {
                background: linear-gradient(90deg,
                    rgba(26, 30, 36, 1) 25%,
                    rgba(50, 54, 60, 1) 50%,
                    rgba(26, 30, 36, 1) 75%);
                background-size: 200% 100%;
                animation: shimmer-load 1.5s infinite;
                min-height: 375px;
                border-radius: 4px;
            }
            .img-shimmer.loaded {
                animation: none;
                background: none;
                min-height: auto;
            }
        `;
        document.head.appendChild(style);

        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.series-book-card img[loading="lazy"], .book-cover[loading="lazy"]').forEach(img => {
                if (img.complete) return; // Already loaded from cache
                img.classList.add('img-shimmer');
                img.addEventListener('load', () => {
                    img.classList.add('loaded');
                    setTimeout(() => img.classList.remove('img-shimmer', 'loaded'), 500);
                }, { once: true });
            });
        });
    })();

    /* =========================================
       8. SMOOTH PAGE TRANSITIONS
       ========================================= */
    (function () {
        if (motionQuery.matches) return;

        // Inject transition overlay
        const style = document.createElement('style');
        style.textContent = `
            .page-transition-overlay {
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: #0d1015;
                z-index: 100000;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease;
            }
            .page-transition-overlay.active {
                opacity: 1;
                pointer-events: all;
            }
        `;
        document.head.appendChild(style);

        const overlay = document.createElement('div');
        overlay.className = 'page-transition-overlay';
        document.body.appendChild(overlay);

        // Fade in on page arrival
        overlay.style.opacity = '1';
        overlay.style.transition = 'none';
        requestAnimationFrame(() => {
            overlay.style.transition = 'opacity 0.4s ease';
            overlay.style.opacity = '0';
        });

        // Intercept internal navigation links
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (!link) return;

            const href = link.getAttribute('href');
            // Only intercept local page links (not external, not anchors, not booklinker)
            if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('//') || link.target === '_blank') return;
            if (!href.endsWith('.html') && href !== '/') return;

            e.preventDefault();

            // Check for View Transitions API
            if (document.startViewTransition) {
                document.startViewTransition(() => {
                    window.location.href = href;
                });
            } else {
                overlay.classList.add('active');
                setTimeout(() => { window.location.href = href; }, 300);
            }
        });
    })();

})();
