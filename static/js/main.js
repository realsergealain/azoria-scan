/**
 * Azoria - Interactive UI Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons if available
    if (window.lucide) {
        window.lucide.createIcons();
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || !href.startsWith('#')) return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

/**
 * Alpine.js component for the live interactive Store Simulator
 */
function storeSimulator() {
    return {
        storeName: 'Maison Kente',
        category: 'Mode & Habillement',
        productName: 'Robe Saharienne Wax',
        productPrice: '18 500',
        copied: false,
        activeTab: 'preview',
        aiGenerated: false,
        aiTitle: '',
        aiDesc: '',

        get storeSlug() {
            return this.storeName
                .toLowerCase()
                .trim()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/^-+|-+$/g, '') || 'ma-boutique';
        },

        get fullUrl() {
            return `https://azoria.link/${this.storeSlug}`;
        },

        copyLink() {
            navigator.clipboard.writeText(this.fullUrl).then(() => {
                this.copied = true;
                setTimeout(() => {
                    this.copied = false;
                }, 2500);
            });
        },

        generateAI() {
            this.aiGenerated = true;
            this.aiTitle = `✨ ${this.productName} — Élégance & Coupe Premium`;
            this.aiDesc = `Sublimez votre style avec notre ${this.productName}. Confection artisanale haute qualité, tissu respirant et coupe ajustée idéale pour toutes vos sorties chic. Disponible en plusieurs tailles avec livraison rapide à Abidjan et partout en Côte d'Ivoire.`;
        }
    };
}
