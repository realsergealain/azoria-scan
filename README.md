Voici un **cahier des charges / prompt complet** que tu peux donner à une IA pour développer **Azoria**. Je l'ai volontairement conçu comme un **MVP professionnel mais réalisable**, sans ajouter inutilement des dizaines de fonctionnalités.

---

# PROMPT COMPLET — PROJET AZORIA

## 1. Présentation du projet

Je veux créer une plateforme SaaS appelée **Azoria**.

Azoria est une plateforme de **social commerce** qui permet à n'importe quel vendeur de créer facilement sa propre boutique en ligne depuis son téléphone ou son ordinateur.

Le vendeur peut :

1. créer sa boutique ;
2. ajouter ses produits ;
3. ajouter des photos, un prix et une description ;
4. utiliser une intelligence artificielle pour générer ou améliorer le titre et la description ;
5. partager sa boutique grâce à un lien personnalisé ;
6. générer un QR Code pour sa boutique ou un produit ;
7. recevoir et gérer les commandes ;
8. proposer le paiement à la livraison ;
9. gérer la livraison locale ou l'expédition vers une autre ville.

L'objectif principal est de permettre aux vendeurs qui utilisent **TikTok, WhatsApp, Facebook, Instagram et les QR Codes** de transformer facilement leurs visiteurs en commandes.

Azoria doit être :

* simple ;
* rapide ;
* professionnel ;
* mobile-first ;
* facile à utiliser même pour une personne peu expérimentée avec la technologie ;
* adapté en priorité au marché ivoirien, tout en restant extensible à d'autres pays.

---

# 2. Problème que résout Azoria

Beaucoup de vendeurs prennent encore leurs commandes manuellement via WhatsApp ou les commentaires sur les réseaux sociaux.

Le processus ressemble souvent à ceci :

```text
Client voit un produit
        ↓
Écrit au vendeur sur WhatsApp
        ↓
Le vendeur demande :
Nom ?
Téléphone ?
Ville ?
Adresse ?
Produit ?
Couleur ?
Taille ?
Quantité ?
        ↓
Le vendeur enregistre manuellement la commande
```

Ce processus devient difficile lorsque le vendeur reçoit beaucoup de messages.

Azoria simplifie le processus :

```text
TikTok / WhatsApp / Facebook / Instagram
                    ↓
              Lien ou QR Code
                    ↓
             Boutique Azoria
                    ↓
              Choix du produit
                    ↓
             Informations client
                    ↓
           Choix de la livraison
                    ↓
         Confirmation de commande
                    ↓
             Paiement à la livraison
```

---

# 3. Utilisateurs

L'application possède principalement trois types d'utilisateurs.

## A. Visiteur / client

Un client peut visiter une boutique publique sans nécessairement créer de compte.

Il peut :

* voir la boutique ;
* rechercher un produit ;
* consulter un produit ;
* choisir une variante ;
* ajouter au panier ;
* modifier les quantités ;
* passer une commande ;
* renseigner ses informations ;
* choisir une ville ;
* choisir un mode de livraison disponible ;
* choisir éventuellement une compagnie de transport ;
* recevoir une confirmation.

---

## B. Vendeur

Le vendeur possède un compte Azoria et peut créer et gérer sa boutique.

Il peut :

* créer sa boutique ;
* modifier les informations de la boutique ;
* ajouter son logo ;
* ajouter une image de couverture ;
* créer ses produits ;
* gérer les commandes ;
* gérer les livraisons ;
* générer des liens ;
* générer des QR Codes ;
* utiliser Azoria AI ;
* consulter des statistiques simples.

---

## C. Administrateur

L'administrateur gère la plateforme.

Il peut :

* voir les utilisateurs ;
* voir les boutiques ;
* gérer les catégories ;
* gérer les villes ;
* gérer les compagnies de transport ;
* modérer ou désactiver une boutique ;
* consulter les statistiques globales ;
* gérer les paramètres de la plateforme.

Pour le back-office, utiliser **Django Admin** autant que possible afin d'éviter de développer inutilement une deuxième interface d'administration complète.

---

# 4. Onboarding vendeur

Après inscription, le vendeur doit pouvoir créer sa boutique en quelques étapes.

### Étape 1

```text
Bienvenue sur Azoria 👋

Quel est le nom de votre boutique ?

[ __________________ ]

Continuer
```

### Étape 2

```text
Que vendez-vous ?

[ Mode ]
[ Beauté ]
[ Électronique ]
[ Maison ]
[ Alimentation ]
[ Autre ]
```

### Étape 3

```text
Votre boutique est prête 🎉

https://azoria.../nom-boutique

[ Ajouter mon premier produit ]
```

Le processus doit être extrêmement simple.

---

# 5. Gestion de la boutique

Chaque boutique possède :

```text
Nom
Slug unique
Description
Logo
Image de couverture
Téléphone de contact
WhatsApp
Ville
Adresse
Statut actif/inactif
Date de création
```

Chaque boutique possède une URL publique unique.

Exemple :

```text
azoria/.../ma-boutique
```

Le système doit utiliser un slug unique et propre.

---

# 6. Gestion des produits

Le vendeur peut créer un produit.

Champs principaux :

```text
Nom
Slug
Description
Prix
Prix promotionnel facultatif
Quantité en stock
Catégorie
Photos
Statut publié/brouillon
```

Le vendeur peut :

* créer un produit ;
* modifier un produit ;
* supprimer un produit ;
* publier ou dépublier un produit ;
* gérer le stock.

---

# 7. Variantes de produits

Un produit peut avoir des options.

Exemple :

```text
Robe

Couleur :
- Rouge
- Noir
- Bleu

Taille :
- S
- M
- L
- XL
```

Le client doit sélectionner les options avant d'ajouter le produit au panier lorsque cela est nécessaire.

Une variante peut avoir :

```text
Prix différent
Stock différent
SKU facultatif
```

La structure doit rester flexible.

---

# 8. Images produits

Le vendeur doit pouvoir ajouter plusieurs images.

Fonctionnalités :

* téléversement ;
* suppression ;
* réorganisation ;
* image principale.

Les images doivent être optimisées et stockées dans une solution adaptée à la production.

Ne pas stocker les fichiers de production directement dans le dépôt Git.

---

# 9. Azoria AI

Azoria possède une fonctionnalité IA simple.

Le vendeur ajoute :

```text
Nom du produit ou informations
Prix
Catégorie
Caractéristiques
```

Puis clique sur :

```text
✨ Générer avec Azoria AI
```

L'IA peut générer :

* un titre accrocheur ;
* une description professionnelle ;
* une description courte ;
* des points clés de vente.

Exemple de sortie structurée :

```json
{
  "title": "Robe longue élégante pour femme",
  "description": "Description complète du produit...",
  "short_description": "Description courte...",
  "selling_points": [
    "Confortable",
    "Disponible en plusieurs tailles"
  ]
}
```

L'utilisateur doit toujours pouvoir :

* modifier le résultat ;
* régénérer le résultat ;
* refuser le résultat.

L'IA ne doit pas automatiquement publier ou modifier un produit sans validation du vendeur.

---

# 10. Boutique publique

La boutique publique doit être conçue principalement pour les téléphones.

Elle doit être :

* rapide ;
* responsive ;
* simple ;
* claire ;
* avec peu de JavaScript inutile.

Elle affiche :

```text
Logo
Nom de la boutique
Description
Produits
Catégories
Recherche
Panier
```

Structure possible :

```text
┌──────────────────────────┐
│ ← Logo   MA BOUTIQUE     │
├──────────────────────────┤
│ 🔎 Rechercher            │
├──────────────────────────┤
│ Catégories               │
├──────────────────────────┤
│ [Produit] [Produit]      │
│ [Produit] [Produit]      │
│ [Produit] [Produit]      │
├──────────────────────────┤
│ 🛒 Panier                │
└──────────────────────────┘
```

---

# 11. Page produit

Chaque produit possède une page.

Le client voit :

* photos ;
* nom ;
* prix ;
* ancien prix si promotion ;
* description ;
* caractéristiques ;
* disponibilité ;
* variantes ;
* quantité.

Actions :

```text
[-] 1 [+]

[ Ajouter au panier ]

ou

[ Commander maintenant ]
```

---

# 12. Panier

Le client peut :

* ajouter un produit ;
* modifier la quantité ;
* supprimer un produit ;
* voir le sous-total.

Le panier doit fonctionner correctement pour un visiteur non connecté.

La solution technique peut utiliser une session ou un mécanisme approprié.

---

# 13. Checkout / commande

Le processus de commande doit être extrêmement court.

Le client renseigne :

```text
Nom complet
Téléphone
Ville
Commune ou zone
Adresse ou point de livraison
```

Puis :

```text
Mode de livraison
```

Enfin :

```text
Paiement à la livraison
```

Le client voit un récapitulatif clair :

```text
Produits       15 000 FCFA
Livraison       2 000 FCFA

TOTAL          17 000 FCFA
```

Puis :

```text
[ Confirmer la commande ]
```

---

# 14. Livraison locale

Le vendeur peut définir ses zones de livraison.

Exemple :

```text
Cocody       2 000 FCFA
Yopougon     2 000 FCFA
Abobo        2 500 FCFA
Marcory      2 000 FCFA
```

Le système calcule automatiquement les frais selon la zone sélectionnée.

---

# 15. Expédition vers une autre ville

Pour les clients situés dans une autre ville :

```text
Ville :
[ Man ▼ ]

Mode d'expédition :
[ Compagnie de transport ▼ ]
```

L'administrateur peut gérer une liste de compagnies de transport.

Le vendeur peut également choisir les compagnies qu'il accepte.

Exemple :

```text
Compagnie A
Compagnie B
Compagnie C
```

Une commande expédiée peut avoir différents statuts :

```text
Nouvelle
Confirmée
En préparation
Expédiée
Arrivée
Livrée
Annulée
```

La structure doit permettre d'ajouter plus tard des informations telles que :

```text
Référence d'expédition
Agence de départ
Agence d'arrivée
Date d'expédition
```

---

# 16. Gestion des commandes

Le vendeur possède un écran simple.

```text
COMMANDES

[ Nouvelles ] [ En cours ] [ Expédiées ] [ Livrées ]

#AZ-00124

Client : Jean
Total : 17 000 FCFA

Statut :
Nouvelle

[ Voir ]
```

Le vendeur peut :

* consulter une commande ;
* confirmer ;
* annuler ;
* modifier le statut ;
* voir les produits commandés ;
* voir les informations du client ;
* voir le mode de livraison.

---

# 17. QR Codes

Azoria permet de générer :

### QR Code de boutique

```text
QR → Boutique complète
```

### QR Code de produit

```text
QR → Produit spécifique
```

### QR Code de campagne

Le vendeur peut créer une campagne :

```text
Nom :
Live TikTok Août 2026
```

Azoria génère un lien et un QR Code.

Plus tard, cela permettra de savoir quelle campagne a généré des visites et éventuellement des commandes.

Le QR Code doit pouvoir être téléchargé dans un format adapté au partage ou à l'impression.

---

# 18. Partage

Le vendeur peut partager :

* sa boutique ;
* un produit ;
* une campagne.

Plateformes ciblées :

```text
WhatsApp
TikTok
Facebook
Instagram
Copier le lien
QR Code
```

---

# 19. Dashboard vendeur

Le dashboard doit rester simple.

Exemple :

```text
Bonjour 👋

Aujourd'hui

Commandes : 8

À préparer : 3

Expédiées : 2

Livrées : 3

-----------------

Commandes récentes

#AZ-101
#AZ-102
#AZ-103
```

Ne pas surcharger le dashboard avec trop de graphiques dans le MVP.

---

# 20. Notifications

Le système doit être conçu pour supporter des notifications.

Exemples :

```text
Nouvelle commande
Commande confirmée
Commande expédiée
Commande livrée
```

Pour le MVP, commencer par des notifications dans l'application et prévoir une architecture permettant d'ajouter plus tard :

* email ;
* SMS ;
* WhatsApp, selon les intégrations disponibles et autorisées.

---

# 21. Recherche

Le client peut rechercher :

```text
Nom du produit
Catégorie
```

La recherche doit fonctionner rapidement et être adaptée à une boutique avec un catalogue raisonnable.

Ne pas introduire Elasticsearch ou une infrastructure complexe dans le MVP sans besoin réel.

---

# 22. Catégories

Une catégorie contient :

```text
Nom
Slug
Description facultative
Image facultative
Statut
```

Exemples :

```text
Mode
Beauté
Électronique
Maison
Alimentation
Sport
Autre
```

---

# 23. Architecture Django

Utiliser une architecture Django modulaire.

```text
azoria/
│
├── config/
│   ├── settings/
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── stores/
│   ├── catalog/
│   ├── carts/
│   ├── orders/
│   ├── shipping/
│   ├── qr_codes/
│   ├── ai/
│   └── core/
│
├── templates/
├── static/
├── media/
├── tests/
│
├── manage.py
└── pyproject.toml
```

Ne pas créer une architecture excessivement complexe avec des dizaines d'applications inutiles.

---

# 24. Stack technique

Utiliser :

```text
Python
Django
PostgreSQL
Django Templates
HTMX
Alpine.js
Tailwind CSS
```

Outils de qualité :

```text
Ruff
pytest
pytest-django
pre-commit
```

Ajouter seulement lorsque nécessaire :

```text
Redis
Celery
```

Pour les images en production :

```text
S3-compatible storage
```

Utiliser :

```text
Git
GitHub Actions
Docker
```

Docker peut être utilisé pour faciliter le développement et le déploiement, mais ne doit pas compliquer inutilement le projet.

---

# 25. Authentification

Utiliser un **Custom User Model Django dès le début**.

Le modèle utilisateur doit être extensible.

Champs possibles :

```text
id
email
phone
first_name
last_name
is_active
is_staff
created_at
updated_at
```

Utiliser l'email comme identifiant principal, avec possibilité d'ajouter plus tard une authentification par téléphone.

Ne pas modifier le modèle utilisateur après avoir déjà construit toutes les migrations.

---

# 26. Identifiants

Utiliser des identifiants non séquentiels exposés publiquement.

Par exemple :

```text
UUID
```

ou une autre stratégie cohérente décidée dès le début.

Les commandes peuvent également avoir un numéro lisible par l'utilisateur, par exemple :

```text
AZ-2026-000123
```

Ne pas confondre :

```text
ID interne
```

et :

```text
Numéro public de commande
```

---

# 27. Sécurité

L'application doit respecter les bonnes pratiques Django.

Inclure :

* protection CSRF ;
* validation côté serveur ;
* permissions ;
* contrôle d'accès aux boutiques ;
* contrôle d'accès aux commandes ;
* protection contre les accès à des ressources appartenant à un autre vendeur ;
* validation des fichiers uploadés ;
* secrets uniquement dans les variables d'environnement ;
* aucune clé API dans le frontend ou dans Git ;
* `.env` ignoré par Git.

Chaque vendeur doit uniquement pouvoir modifier :

```text
ses boutiques
ses produits
ses commandes
ses paramètres
```

---

# 28. Performance

L'application doit être optimisée pour les téléphones et les connexions variables.

Principes :

* pages légères ;
* images optimisées ;
* pagination ;
* index de base de données sur les champs fréquemment recherchés ;
* éviter le problème N+1 ;
* utiliser `select_related` et `prefetch_related` lorsque nécessaire ;
* éviter les requêtes inutiles ;
* utiliser du cache uniquement lorsqu'il apporte un réel bénéfice.

---

# 29. Base de données — principales entités

```text
User
│
└── Store
      │
      ├── Product
      │     ├── ProductImage
      │     └── ProductVariant
      │
      ├── ShippingZone
      │
      ├── Campaign
      │     └── QRCode
      │
      └── Order
             │
             ├── OrderItem
             └── Shipment
```

Entités globales :

```text
Category
City
TransportCompany
```

---

# 30. Relations principales

```text
User
  └── possède une ou plusieurs Store

Store
  └── possède plusieurs Product

Product
  └── possède plusieurs ProductImage

Product
  └── possède plusieurs ProductVariant

Store
  └── reçoit plusieurs Order

Order
  └── possède plusieurs OrderItem

OrderItem
  └── représente une copie des informations du produit au moment de la commande

Order
  └── peut posséder une Shipment

Store
  └── possède plusieurs Campaign

Campaign
  └── peut posséder un QR Code
```

Important : les données d'une commande doivent conserver un historique. Si le vendeur modifie ensuite le prix ou le nom d'un produit, une ancienne commande ne doit pas changer rétroactivement.

---

# 31. Règles métier importantes

### Stock

Le stock ne doit pas devenir négatif.

La logique de création de commande doit être protégée contre les problèmes de concurrence lorsque plusieurs clients commandent simultanément.

Utiliser des transactions de base de données et des mécanismes de verrouillage adaptés lorsque nécessaire.

### Prix

Le prix affiché dans une commande doit être enregistré au moment de la commande.

Ne pas recalculer le prix historique à partir du produit actuel.

### Commande

Une commande doit conserver :

```text
nom du client
téléphone
adresse
ville
produits
prix au moment de l'achat
frais de livraison
total
mode de livraison
statut
```

---

# 32. API

Ne pas créer une API REST complète pour toutes les fonctionnalités si elle n'est pas nécessaire.

L'application principale peut utiliser Django Templates + HTMX.

Prévoir toutefois une architecture qui permettra d'ajouter plus tard une API pour :

* application mobile ;
* intégrations externes ;
* partenaires logistiques.

Django REST Framework peut être ajouté lorsque ce besoin devient concret.

---

# 33. Qualité du code

Le code doit respecter les principes suivants :

* code lisible ;
* fonctions courtes lorsque possible ;
* logique métier séparée des vues ;
* éviter les vues de plusieurs centaines de lignes ;
* utiliser des services ou des fonctions métier lorsque cela apporte de la clarté ;
* utiliser les transactions pour les opérations critiques ;
* type hints Python lorsque pertinents ;
* tests pour les fonctionnalités critiques.

Ne pas appliquer des design patterns simplement parce qu'ils sont populaires.

La simplicité et la maintenabilité sont prioritaires.

---

# 34. Tests prioritaires

Créer des tests pour :

```text
Création d'utilisateur
Création de boutique
Permissions vendeur
Création de produit
Gestion du panier
Création de commande
Calcul du total
Calcul des frais de livraison
Protection du stock
Permissions sur les commandes
```

Les tests doivent être ajoutés progressivement avec chaque fonctionnalité importante.

---

# 35. Interface utilisateur

L'interface doit être :

```text
Mobile First
Simple
Moderne
Rapide
Accessible
```

Le vendeur doit pouvoir effectuer les principales actions avec son téléphone.

Navigation vendeur :

```text
Accueil
Produits
Commandes
Boutique
Profil
```

Utiliser une navigation adaptée aux écrans mobiles.

---

# 36. Priorités de développement

## PHASE 1 — Fondation

```text
✓ Projet Django
✓ PostgreSQL
✓ Custom User
✓ Authentification
✓ Configuration
✓ Tests
```

## PHASE 2 — Boutiques

```text
✓ Création de boutique
✓ Modification
✓ Slug
✓ Boutique publique
```

## PHASE 3 — Catalogue

```text
✓ Catégories
✓ Produits
✓ Images
✓ Stock
✓ Variantes
```

## PHASE 4 — Vente

```text
✓ Panier
✓ Checkout
✓ Client invité
✓ Commande
✓ Paiement à la livraison
```

## PHASE 5 — Livraison

```text
✓ Villes
✓ Zones
✓ Frais
✓ Compagnies de transport
✓ Expédition
```

## PHASE 6 — Acquisition

```text
✓ Lien boutique
✓ Lien produit
✓ QR Code
✓ Campagnes
```

## PHASE 7 — IA

```text
✓ Génération de titre
✓ Génération de description
✓ Amélioration de texte
```

## PHASE 8 — Optimisation

```text
✓ Notifications
✓ Statistiques
✓ Cache
✓ Tâches asynchrones si nécessaire
✓ Optimisation images
```

---

# INSTRUCTION FINALE POUR L'IA QUI VA CODER

> Construis Azoria progressivement. Ne génère pas tout le projet en une seule fois. Commence par analyser l'architecture existante et respecte les conventions de Django. Avant d'ajouter une nouvelle fonctionnalité, vérifie les modèles et migrations existants afin d'éviter les duplications.
>
> Utilise un Custom User Model dès le début. Utilise PostgreSQL. Construis une application mobile-first avec Django Templates, HTMX, Alpine.js et Tailwind CSS.
>
> Privilégie les fonctionnalités réellement nécessaires au MVP. N'ajoute pas Redis, Celery, Docker, Django REST Framework ou d'autres infrastructures complexes sans justification technique.
>
> Pour chaque fonctionnalité importante :
>
> 1. créer ou modifier les modèles ;
> 2. créer les migrations ;
> 3. définir les contraintes et index nécessaires ;
> 4. implémenter la logique métier ;
> 5. appliquer les permissions ;
> 6. créer les vues et interfaces ;
> 7. ajouter les tests critiques ;
> 8. vérifier que la fonctionnalité n'introduit pas de régression.
>
> Le code doit être simple, maintenable, sécurisé et professionnel. Ne pas inventer de fonctionnalités non demandées. Ne pas modifier ou supprimer des fonctionnalités existantes sans vérifier leur impact.

---

## La vision d'Azoria en une phrase

> **Azoria permet à n'importe quel vendeur de créer facilement une boutique en ligne, partager ses produits grâce à un lien ou un QR Code, recevoir des commandes et gérer la livraison, directement depuis son téléphone.**

Je te conseille de donner ce document à l'IA comme **spécification de référence**, puis de lui demander de développer **une phase à la fois**, en commençant par la Phase 1.
