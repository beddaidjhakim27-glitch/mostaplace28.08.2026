# Grille d’audit — pasted_content_5.txt

## Périmètre

La spécification demande une refonte structurelle et visuelle des pages `Publication d’annonce` et `Boutique`, avec priorité mobile, sans remplacer les données réelles ni casser le backend, les API, les photos, les catégories, les profils, les favoris, la recherche et les filtres.

## Exigences Publication

1. Parcours lisible : catégorie → photos → informations → champs adaptés → aperçu → publication.
2. Sélecteur de catégories sous forme de cartes et adaptation des champs selon la catégorie.
3. Sections distinctes pour titre, description, prix, localisation, état, catégorie et sous-catégorie.
4. Zone photo multi-images avec suppression, ordre, photo principale et prévisualisation immédiate.
5. Champs intelligents au moins pour véhicules, immobilier et informatique.
6. Aperçu avant publication.
7. Bouton `Publier mon annonce`, validations lisibles et confirmation après succès.

## Exigences Boutique

1. En-tête vendeur : identité visuelle, nom, description, localisation, nombre d’annonces, informations utiles et contact.
2. Produits en cartes lisibles : image, titre, prix, localisation, état, favoris et badge éventuel.
3. Recherche et filtres : catégorie, prix, localisation, état, date, pertinence ; panneau propre sur mobile.
4. Organisation : vendeur → recherche → filtres → catégories → produits → pagination/chargement progressif.
5. Cartes légèrement arrondies, ombres discrètes, orange en accent, noir/anthracite/blanc/gris.

## Architecture demandée

Composants réutilisables à créer ou extraire si nécessaire : `CategorySelector`, `PublicationForm`, `ImageUploader`, `DynamicFields`, `ListingPreview`, `ShopHeader`, `ShopFilters`, `ProductCard`, `ProductGrid`, `EmptyState`, `LoadingState`. Éviter un composant monolithique.

## Contraintes de validation

Tester les deux pages sur desktop, tablette et mobile. Vérifier la lisibilité, les tailles d’images, les boutons tactiles, l’absence de débordement horizontal et la continuité visuelle avec le logo officiel et l’orange MostaPlace. Toute correction doit rester minimale, réutiliser les APIs existantes et ne pas simuler de données.

## Contrôle navigateur initial — 27 août 2026

La route `/publier` redirige correctement un visiteur non connecté vers `/connexion?next=/publier`, puis affiche un état de vérification de session. La page de publication n’a donc pas pu être inspectée en mode formulaire sans session QA, mais le code confirme une structure en deux colonnes avec informations, photos et état de publication.

La route `/boutiques` affiche une page longue avec hero professionnel, publication standard gratuite, catégories de boutique, plans Basique/Premium/Gold, bloc de configuration vendeur, aperçu de vitrine, règles marketplace et liste de boutiques existantes. Le rendu desktop contrôlé montre une hiérarchie cohérente, mais les textes du hero et certains contrastes paraissent faibles sur le fond sombre ; une vérification multi-breakpoints est encore requise. La page utilise des données de catégories et plans locaux, et le backend expose la création/listing de boutiques ainsi que le contrôle de paiement, mais aucune route de détail `/boutique/:id` n’apparaît dans `App.tsx` malgré les liens générés par `VirtualShopsPage`.


## Écarts vérifiés dans le code

### Publication d’annonce

La page actuelle est protégée par `useAuth` et conserve le flux réel `trpc.ai.publish`, l’upload Appwrite et la modération IA. Elle possède des sections distinctes pour les informations, les photos et la confirmation de publication. Elle permet l’ajout multiple, la suppression et la prévisualisation immédiate des photos.

Elle ne satisfait pas encore toute la séquence de la spécification : la catégorie est un `<select>` dans la section principale et non un sélecteur de cartes ; il n’existe pas de sous-catégorie ; les champs dynamiques par catégorie ne sont pas présents ; `condition` est envoyé en dur à `"bon"` ; il n’y a pas de réordonnancement ni de choix explicite de photo principale ; aucun aperçu de fiche avant publication n’est rendu ; la confirmation passe par toast/navigation ; et la page reste un formulaire à deux colonnes plutôt qu’un parcours guidé catégorie → photos → informations → champs → aperçu.

### Boutique

`VirtualShopsPage` propose un hero, des catégories, trois plans, un formulaire de création et un aperçu de vitrine. La création réelle passe par `trpc.virtualShops.create`, qui refuse de poursuivre si le paiement n’est pas activé et ne crée pas de transaction dans ce cas. Le backend persiste une boutique Appwrite avec statut `pending` et expose une liste publique des boutiques `active`.

La page ne contient pas encore l’espace professionnel complet décrit : il n’y a pas de recherche de produits de boutique, de filtres catégorie/prix/localisation/état/date/pertinence, de grille d’annonces appartenant à une boutique, de pagination de produits ni de panneau mobile `Filtrer`. Les cartes présentes sont des cartes de catégories et de plans, pas des `ProductCard` d’annonces. Les liens générés vers `/boutique/:id` ne correspondent à aucune route déclarée dans `App.tsx`, ce qui constitue un dead-end à corriger lors d’une future implémentation.

### Architecture

Les composants réutilisables demandés (`CategorySelector`, `PublicationForm`, `ImageUploader`, `DynamicFields`, `ListingPreview`, `ShopHeader`, `ShopFilters`, `ProductCard`, `ProductGrid`, `EmptyState`, `LoadingState`) n’existent pas comme fichiers dédiés. La logique principale reste concentrée dans `PublishPage.tsx` et `VirtualShopsPage.tsx`, même si la structure interne est déjà segmentée par sections et que le shell global est partagé.

### Backend et données

Les contrats backend réels existent pour `listings`, `favorites`, `banners`, `virtualShops`, `billing`, `comments`, `reports`, `messages`, `orders` et `ratings`. Les listes publiques Appwrite filtrent les statuts attendus et la publication applique la modération IA avant de rendre une annonce publique. La persistance Appwrite réelle et les schémas distants restent toutefois non homologués dans l’environnement courant ; le profil fail-closed ne doit pas être remplacé par une fausse réussite.

### Design et responsive

Le code CSS contient des breakpoints explicites pour la publication et la boutique, avec réduction des grilles jusqu’à une colonne sur mobile. L’audit automatisé a trouvé `document.scrollWidth <= viewportWidth` aux sept largeurs sur `/boutiques` et sur la route `/publier` observée en accès visiteur. La page `/publier` n’a pas pu être inspectée en mode formulaire sans session authentifiée ; ce point est donc `EN ATTENTE`, pas `PASS`.
