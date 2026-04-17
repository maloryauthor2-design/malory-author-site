/**
 * animations.js — Scroll-triggered reveal animations
 *
 * Add this to every page with:
 *   <script src="animations.js" defer></script>
 *
 * Works by selecting key elements and adding a .reveal class,
 * then using IntersectionObserver to add .visible when they
 * scroll into view. The CSS in style.css handles the actual
 * fade + slide transition.
 *
 * Automatically disabled if the user has prefers-reduced-motion set.
 */

document.addEventListener('DOMContentLoaded', () => {

    // Respect the user's OS motion preference — bail out entirely if set
    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (motionQuery.matches) return;

    // Elements to animate. Excludes header/hero (already above fold).
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
        '.publisher-strip'
    ].join(', ');

    const elements = document.querySelectorAll(ANIMATED_SELECTORS);
    if (!elements.length) return;

    // Add the reveal class to prime them for animation
    elements.forEach(el => el.classList.add('reveal'));

    // Use a single shared observer for memory efficiency
    const observer = new IntersectionObserver((entries) => {

        // Sort triggering entries top-to-bottom so stagger feels natural
        const visible = entries
            .filter(e => e.isIntersecting)
            .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

        visible.forEach((entry, i) => {
            // Stagger each element in the batch by 80ms, capped at 400ms total
            const delay = Math.min(i * 80, 400);
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, delay);
            // Only animate once — unobserve after triggering
            observer.unobserve(entry.target);
        });

    }, {
        threshold: 0.07,
        rootMargin: '0px 0px -30px 0px'
    });

    elements.forEach(el => observer.observe(el));

    // Listen for runtime changes to motion preference
    motionQuery.addEventListener('change', (e) => {
        if (e.matches) {
            // User just enabled reduced motion — show everything immediately
            document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
                el.classList.add('visible');
                observer.unobserve(el);
            });
        }
    });
});

/**
 * Starfield — Subtle drifting stars on the dark background.
 * Uses a fixed canvas behind all content. Respects reduced motion.
 * Automatically pauses when the tab is hidden for performance.
 */
(function() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const canvas = document.createElement('canvas');
    canvas.id = 'starfield';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.prepend(canvas);

    const ctx = canvas.getContext('2d');
    let w, h, stars, raf;
    const STAR_COUNT = 80;
    const MAX_SPEED = 0.15;

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }

    function createStars() {
        stars = [];
        for (let i = 0; i < STAR_COUNT; i++) {
            stars.push({
                x: Math.random() * w,
                y: Math.random() * h,
                r: Math.random() * 1.2 + 0.3,
                dx: (Math.random() - 0.5) * MAX_SPEED,
                dy: (Math.random() - 0.5) * MAX_SPEED,
                alpha: Math.random() * 0.6 + 0.2
            });
        }
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);
        for (const s of stars) {
            s.x += s.dx;
            s.y += s.dy;
            if (s.x < 0) s.x = w;
            if (s.x > w) s.x = 0;
            if (s.y < 0) s.y = h;
            if (s.y > h) s.y = 0;

            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(212, 175, 55, ' + s.alpha + ')';
            ctx.fill();
        }
        raf = requestAnimationFrame(draw);
    }

    function start() {
        resize();
        createStars();
        draw();
    }

    // Pause when tab is hidden
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            cancelAnimationFrame(raf);
        } else {
            draw();
        }
    });

    window.addEventListener('resize', () => {
        resize();
        // Don't recreate stars on resize, just update canvas dimensions
    });

    // Respect runtime motion changes
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
        if (e.matches) {
            cancelAnimationFrame(raf);
            canvas.remove();
        }
    });

    start();
})();