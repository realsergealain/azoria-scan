/**
 * Azoria — Interactive UI Scripts
 * Navbar scroll-aware, smooth scroll, reveal animations, store simulator
 */

/* ────────────────────────────────────────────
   1. Navbar — Scroll-aware glassmorphism
──────────────────────────────────────────── */
(function initNavbar() {
  const header = document.querySelector('header.nav-header');
  if (!header) return;

  const SCROLL_THRESHOLD = 20;

  function updateNavbarState() {
    if (window.scrollY > SCROLL_THRESHOLD) {
      header.classList.add('scrolled');
      const navPill = header.querySelector('nav');
      if (navPill) navPill.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
      const navPill = header.querySelector('nav');
      if (navPill) navPill.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', updateNavbarState, { passive: true });
  updateNavbarState(); // Run immediately on load
})();


/* ────────────────────────────────────────────
   2. Smooth Scroll — with navbar offset
──────────────────────────────────────────── */
(function initSmoothScroll() {
  const NAVBAR_HEIGHT = 80; // px — approximate fixed navbar height

  document.addEventListener('click', function (e) {
    const anchor = e.target.closest('a[href^="#"]');
    if (!anchor) return;

    const href = anchor.getAttribute('href');
    if (!href || href === '#') return;

    const target = document.querySelector(href);
    if (!target) return;

    e.preventDefault();

    const targetTop = target.getBoundingClientRect().top + window.pageYOffset - NAVBAR_HEIGHT;
    window.scrollTo({
      top: Math.max(0, targetTop),
      behavior: 'smooth',
    });
  });
})();


/* ────────────────────────────────────────────
   3. Reveal on Scroll — IntersectionObserver
──────────────────────────────────────────── */
(function initRevealOnScroll() {
  const elements = document.querySelectorAll('.reveal-on-scroll');
  if (!elements.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target); // Only reveal once
        }
      });
    },
    {
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px',
    }
  );

  elements.forEach((el) => observer.observe(el));
})();


/* ────────────────────────────────────────────
   4. Lucide Icons — Initialize on DOMContentLoaded
──────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
});

// Refresh icons after Alpine.js initializes (for dynamically rendered elements)
document.addEventListener('alpine:initialized', () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
});


/* ────────────────────────────────────────────
   5. Alpine.js — Live Store Simulator Component
──────────────────────────────────────────── */
function storeSimulator() {
  return {
    storeName: 'Maison Kente',
    category: 'Mode & Habillement',
    productName: 'Robe Saharienne Wax',
    productPrice: '18 500',
    copied: false,
    aiGenerated: false,
    aiTitle: '',
    aiDesc: '',

    /**
     * Generate a URL-safe slug from the store name.
     */
    get storeSlug() {
      return (
        this.storeName
          .toLowerCase()
          .trim()
          .normalize('NFD')
          .replace(/[\u0300-\u036f]/g, '')
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-+|-+$/g, '') || 'ma-boutique'
      );
    },

    /**
     * Full public URL of the store.
     */
    get fullUrl() {
      return `https://azoria.link/${this.storeSlug}`;
    },

    /**
     * Copy the store URL to the clipboard.
     */
    copyLink() {
      if (!navigator.clipboard) return;
      navigator.clipboard.writeText(this.fullUrl).then(() => {
        this.copied = true;
        setTimeout(() => {
          this.copied = false;
        }, 2500);
      });
    },

    /**
     * Simulate an AI-generated product description.
     */
    generateAI() {
      this.aiGenerated = false;
      const name = this.productName || 'votre produit';
      const cat  = this.category  || 'Mode';

      // Simulate a brief loading delay for realism
      setTimeout(() => {
        this.aiGenerated = true;
        this.aiTitle = `✨ ${name} — Élégance & Coupe Premium`;
        this.aiDesc  = `Sublimez votre style avec notre ${name}. Confection artisanale de haute qualité, tissu respirant et coupe ajustée idéale pour toutes vos sorties chic. Catégorie : ${cat}. Disponible en plusieurs tailles avec livraison rapide à Abidjan et partout en Côte d'Ivoire.`;

        // Re-init lucide icons for the newly rendered content
        if (window.lucide) {
          window.lucide.createIcons();
        }
      }, 600);
    },
  };
}
