## Contrôle visuel intermédiaire — 27 août 2026

L’accueil servi par le frontend affiche bien la bannière voiture en première position, immédiatement sous le header. La rangée de catégories apparaît directement sous cette bannière, avec les grandes icônes conservées.

Le logo et l’icône MostaPlace AI sont séparés dans la ligne supérieure et aucun chevauchement visuel n’est constaté dans le viewport desktop contrôlé. Le contrôle de défilement n’a pas déplacé le viewport dans cette session navigateur ; le test E2E géométrique vérifie l’ordre des trois blocs dans le DOM et dans leur position calculée.

## Contrôle bannière supérieure après recadrage — 27 août 2026

La bannière supérieure de l’accueil a été contrôlée après le défilement automatique et le rechargement visuel. Le visuel voiture est légèrement recadré et agrandi, les petites flèches latérales ne sont plus visibles, le CTA « Découvrir les véhicules » reste présent et les catégories demeurent sous la bannière. La bannière inférieure n’a pas été modifiée dans cette itération. Les points de navigation restent disponibles lorsque plusieurs visuels sont fournis.

Le contrôle navigateur a porté sur la page d’accueil temporaire et n’a soumis aucune action métier.

## Logo rond et micro-animation — contrôle visuel

Le logo rond officiel est maintenant visible dans l’en-tête d’accueil, avec une taille lisible et sans suppression des assets horizontaux. La bannière supérieure conserve le visuel voiture, le CTA et les catégories sous-jacentes. Deux overlays de roues RGBA sont chargés uniquement lorsque la bannière active est la bannière voiture ; leur rotation est lente, discrète et désactivée avec `prefers-reduced-motion`.

Le contrôle navigateur n’a déclenché aucune action métier et n’a pas touché à Appwrite.

## Nouveau visuel de bannière supérieure — 27 août 2026

Le nouvel asset `mostaplace-car-banner-new.webp` est servi en HTTP 200 par le frontend en WebP 1821×864. Après le chargement complet, la bannière supérieure affiche correctement le nouveau visuel haute qualité avec le logo, le motif IA, le drapeau algérien, la ville et la voiture orange. Un premier contrôle montrait une zone vide pendant le chargement initial ; le second contrôle a confirmé le rendu final correct. La bannière inférieure n’a pas été modifiée.
