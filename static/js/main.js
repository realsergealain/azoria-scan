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


/* ────────────────────────────────────────────
   6. AzoriaUI — Native Micro-Interactions Engine
   (Web Audio Synthesizer, Confetti, Haptics & Counters)
──────────────────────────────────────────── */
window.AzoriaUI = {
  // Web Audio Synthesizer (No MP3 download needed, instant & crystal clear)
  audioCtx: null,

  getAudioContext() {
    if (!this.audioCtx) {
      const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
      if (AudioCtxClass) {
        this.audioCtx = new AudioCtxClass();
      }
    }
    if (this.audioCtx && this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
    return this.audioCtx;
  },

  playChime(type = 'success') {
    try {
      const ctx = this.getAudioContext();
      if (!ctx) return;

      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'order' || type === 'celebration' || type === 'product_created') {
        // Joyful ascending melody (Chime)
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
          const chordOsc = ctx.createOscillator();
          const chordGain = ctx.createGain();
          chordOsc.type = 'triangle';
          chordOsc.frequency.setValueAtTime(freq, now + i * 0.08);
          chordGain.gain.setValueAtTime(0.15, now + i * 0.08);
          chordGain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.6);
          chordOsc.connect(chordGain);
          chordGain.connect(ctx.destination);
          chordOsc.start(now + i * 0.08);
          chordOsc.stop(now + i * 0.08 + 0.6);
        });
      } else if (type === 'pop' || type === 'copy') {
        // Crisp bubble pop sound for copying links / clicks
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.exponentialRampToValueAtTime(1400, now + 0.06);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
        osc.start(now);
        osc.stop(now + 0.09);
      } else if (type === 'cart' || type === 'add') {
        // Crisp pop chime
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.15);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
        osc.start(now);
        osc.stop(now + 0.25);
      } else {
        // Standard success chime
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, now); // D5
        osc.frequency.setValueAtTime(880, now + 0.1); // A5
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        osc.start(now);
        osc.stop(now + 0.35);
      }
    } catch (e) {
      // Audio autoplay policy fallback
    }
  },

  // Pop sound shortcut
  playPop() {
    this.playChime('pop');
    this.vibrate([10]);
  },

  // Success sound shortcut
  playSuccess() {
    this.playChime('celebration');
    this.vibrate([20, 30, 20]);
  },

  // Android Material Toast / Snackbar Feedback
  showToast(message, type = 'success') {
    let container = document.getElementById('azoria-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'azoria-toast-container';
      container.className = 'fixed bottom-6 left-1/2 -translate-x-1/2 z-[9999] flex flex-col items-center gap-2 pointer-events-none px-4 w-full max-w-sm';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto flex items-center gap-3 px-4 py-3 bg-slate-900/95 dark:bg-white/95 text-white dark:text-slate-900 text-xs font-bold rounded-2xl shadow-2xl backdrop-blur-md transform transition-all duration-300 translate-y-8 opacity-0 border border-white/10 dark:border-slate-800/10';
    
    const icon = type === 'success' ? '✓' : 'ℹ';
    toast.innerHTML = `<span class="flex items-center justify-center w-5 h-5 rounded-full bg-brand-500 text-white text-[10px] font-black shrink-0">${icon}</span><span>${message}</span>`;
    
    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-8', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
    });

    // Auto dismiss
    setTimeout(() => {
      toast.classList.add('opacity-0', 'scale-95');
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  },

  // Copy to clipboard with instant pop sound and Android toast
  copyToClipboard(text, message = 'Lien copié dans le presse-papier !') {
    this.playPop();
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => {
        this.showToast(message);
      }).catch(() => {
        this.fallbackCopy(text, message);
      });
    } else {
      this.fallbackCopy(text, message);
    }
  },

  fallbackCopy(text, message) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
      this.showToast(message);
    } catch (err) {
      alert("Lien : " + text);
    }
    document.body.removeChild(textArea);
  },

  // Haptic feedback (Mobile vibration)
  vibrate(pattern = [15]) {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      try {
        navigator.vibrate(pattern);
      } catch (e) {}
    }
  },

  // Confetti Explosion
  celebrate() {
    this.playChime('celebration');
    this.vibrate([20, 40, 20]);

    if (typeof confetti === 'function') {
      confetti({
        particleCount: 90,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#7C3AED', '#3B82F6', '#10B981', '#F59E0B', '#EC4899'],
        disableForReducedMotion: true
      });
      // Second burst
      setTimeout(() => {
        confetti({
          particleCount: 60,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors: ['#7C3AED', '#3B82F6', '#F59E0B']
        });
        confetti({
          particleCount: 60,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
          colors: ['#10B981', '#7C3AED', '#EC4899']
        });
      }, 250);
    }
  },

  // Numerical counter animation
  animateCounters() {
    const counters = document.querySelectorAll('[data-counter]:not([data-counter-animated])');
    counters.forEach(el => {
      el.setAttribute('data-counter-animated', 'true');
      const targetStr = el.getAttribute('data-counter');
      const target = parseInt(targetStr.replace(/\D/g, ''), 10);
      if (isNaN(target) || target <= 0) return;

      const duration = 1000;
      const start = 0;
      const startTime = performance.now();
      const hasFCFA = targetStr.includes('FCFA');

      function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease-out cubic
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (target - start) * easeProgress);

        const formatted = current.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
        el.textContent = hasFCFA ? `${formatted} FCFA` : formatted;

        if (progress < 1) {
          requestAnimationFrame(update);
        } else {
          el.textContent = targetStr;
        }
      }
      requestAnimationFrame(update);
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  AzoriaUI.animateCounters();
});
document.addEventListener('htmx:afterSwap', () => {
  AzoriaUI.animateCounters();
});
document.addEventListener('htmx:afterSettle', () => {
  AzoriaUI.animateCounters();
});

// Unlock Audio Context on user interaction
['click', 'touchstart', 'keydown'].forEach(evtType => {
  document.addEventListener(evtType, function unlock() {
    if (window.AzoriaUI) {
      window.AzoriaUI.getAudioContext();
    }
  }, { once: true, passive: true });
});


