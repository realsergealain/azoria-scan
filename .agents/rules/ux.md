---
trigger: always_on
---

## 🎨 17. EXCELLENCE UI/UX & DESIGN SYSTEM (TAILWIND + ALPINE)
- **Cohérence Visuelle :** Ne jamais utiliser de valeurs arbitraires (ex: `w-[42px]` ou `text-[#1a2b3c]`). Utiliser strictement l'échelle utilitaire de Tailwind. Définir une palette de couleurs SaaS claire dans `tailwind.config.js` (couleurs `primary`, `background`, `surface`, `danger`) et s'y tenir.
- **Feedback Immédiat (Micro-interactions) :** L'utilisateur ne doit jamais se demander si son clic a fonctionné.
  - Désactiver visuellement les boutons (opacité, curseur) et afficher un icône de chargement (spinner) lors de toute soumission de formulaire (via les classes `htmx-request`).
  - Utiliser des *Skeleton Loaders* (écrans de chargement grisés) plutôt qu'une page vide pendant que les données chargent.
  - Renvoyer des notifications *Toasts* élégantes (gérées via Alpine.js) pour confirmer chaque succès ou expliquer chaque erreur.
- **Ergonomie Mobile-First (Touch) :**
  - Les zones de clic (boutons, icônes, liens) doivent avoir une taille minimale de `44x44px` pour être facilement tapables au doigt.
  - Sur mobile, remplacer les fenêtres modales classiques par des "Bottom Sheets" (tiroirs qui glissent depuis le bas de l'écran) pour une navigation à une main naturelle.
- **Animations & Fluidité :** 
  - Toute apparition/disparition d'élément dynamique (menus déroulants, modals, alertes) DOIT utiliser les directives `x-transition` d'Alpine.js. 
  - Ajouter systématiquement `transition-all duration-200 ease-in-out` sur les états `:hover` et `:focus` des boutons et des cartes (cards).
- **États Vides (Empty States) :** Ne jamais laisser un écran vide si l'utilisateur n'a pas de données (ex: 0 produit, 0 commande). Toujours concevoir un "Empty State" professionnel avec une icône douce, un texte explicatif clair et un bouton d'action principal (CTA) pour le guider (ex: "Créer mon premier produit").
- **Typographie & Hiérarchie :** Utiliser des contrastes de gris (ex: `text-gray-900` pour les titres, `text-gray-500` pour les sous-titres). Ne jamais tout mettre en noir pur ou en gras. L'interface doit respirer (utiliser généreusement le padding/margin).