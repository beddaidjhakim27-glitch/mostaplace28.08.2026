# Rapport d’intégration — refonte Auth MostaPlace

**Date :** 27 août 2026  
**Projet :** `/home/ubuntu/mostaplace-work/app/frontend_test_copy`  
**Périmètre :** refonte de `/connexion` et `/inscription`, identité graphique MostaPlace, conservation des parcours d’authentification existants, validation locale.

## Résultat exécutif

La nouvelle page d’inscription est intégrée dans l’application React/Vite existante, et non dans une page parallèle. La route `/inscription` ouvre directement le parcours « Créer un compte ». La route `/connexion` conserve le parcours de connexion, le bouton Google, le mot de passe oublié, les messages d’erreur/succès et les chemins de vérification/récupération déjà présents.

Le rendu validé reprend une composition sombre premium à deux panneaux sur desktop : présentation MostaPlace à gauche, formulaire à droite. Sur mobile, le formulaire passe en priorité en haut puis le panneau de présentation s’empile dessous. Les champs demandés sont présents : nom complet, e-mail, mot de passe, confirmation, contrôle afficher/masquer et case obligatoire d’acceptation des conditions.

Le logo graphique MostaPlace utilise désormais un symbole M/sac vectoriel et un wordmark MOSTA blanc / PLACE orange sur les surfaces sombres. Une variante horizontale sombre, conservant le même symbole, est utilisée sur les headers clairs pour empêcher la disparition de MOSTA sur fond blanc.

## Statuts de validation

| Contrôle | Statut réel | Preuve ou limite |
|---|---:|---|
| TypeScript frontend | **PASS** | `pnpm check` terminé sans erreur après les derniers changements. |
| Tests unitaires | **PASS** | 10 tests passés dans 2 fichiers Vitest. |
| Build Vite | **PASS** | `pnpm build` terminé avec génération de `dist/public`. |
| Contrôle TypeScript backend | **PASS** | `pnpm backend:check` terminé sans erreur. |
| E2E desktop Chromium | **PASS** | Suite complète exécutée avec succès. |
| E2E mobile Chromium | **PASS** | Suite complète exécutée avec succès. |
| Total E2E | **PASS** | 78 tests passés, incluant les nouveaux tests de la refonte Auth. |
| `/inscription` direct | **PASS** | Route, titre, placeholders et case conditions vérifiés. |
| Conditions obligatoires | **PASS** | Soumission locale bloquée et alerte affichée sans appel de création de compte. |
| Afficher/masquer les mots de passe | **PASS** | Les deux contrôles basculent correctement entre `password` et `text`. |
| Contrôle mot de passe différent | **PASS** | Message « Les mots de passe ne correspondent pas. » vérifié. |
| Vérification visuelle desktop | **PASS** | Header sombre, logo, deux panneaux et formulaire visibles dans le navigateur temporaire. |
| Vérification visuelle mobile | **PASS** | Parcours E2E mobile passé ; aucun décalage bloquant détecté. |
| Création réelle de compte Appwrite après cette refonte | **EN ATTENTE** | Aucun compte réel n’a été créé ou modifié pendant cette validation UI. |
| Google OAuth réel | **BLOCKED / non homologué** | Le code conserve le flux existant, mais un PASS exige encore un parcours Google réel complet avec configuration Appwrite/Google valide. |
| Persistance Database/Storage distante | **EN ATTENTE** | Le profil Appwrite fail-closed reste inchangé ; aucune provision distante n’a été lancée. |
| Déploiement public | **NON EXÉCUTÉ** | Netlify et Appwrite restent volontairement en pause conformément à la consigne. |

## Fichiers modifiés ou ajoutés

| Fichier | Modification |
|---|---|
| `client/src/pages/AuthPage.tsx` | Layout Auth intégré, mode inscription via `/inscription`, champs, validations, show/hide, termes, Google, récupération et callbacks conservés. |
| `client/src/pages/auth-page.css` | Nouveau thème sombre, panneau promotionnel, carte formulaire, états de contrôle et responsive mobile. Scope ajouté au shell d’authentification. |
| `client/src/components/BrandLogo.tsx` | Ajout de `tone="dark" | "light"` pour sélectionner le logo adapté à la surface. |
| `client/src/components/MarketplaceShell.tsx` | `/inscription` ajouté au shell Auth ; header global utilise la variante de logo lisible sur fond clair. |
| `client/src/pages/HomePage.tsx` | La barre supérieure claire utilise la variante de logo contrastée ; sidebar et footer conservent la version adaptée au fond sombre. |
| `client/src/pages/template-home.css` | Dimensionnement contextualisé du logo dans sidebar, barre supérieure et footer. |
| `client/public/mostaplace-logo-dark.svg` | Nouvelle variante horizontale sombre avec le même symbole M/sac et wordmark contrasté. |
| `e2e/critical-paths.spec.ts` | Ajout des scénarios `/inscription`, conditions obligatoires et bascule des deux mots de passe. |
| `auth-design-visual-evidence.md` | Trace de la vérification visuelle effectuée dans le navigateur temporaire. |

## Méthode E2E et limites de sécurité

La suite E2E a été exécutée avec les variables de processus `PERSISTENCE_MODE=memory REQUIRE_APPWRITE=false`. Ce mode était **temporaire et strictement limité aux tests UI locaux** ; il n’a pas modifié `backend-local/.env`, n’a pas neutralisé le profil Appwrite fail-closed et ne constitue pas une preuve de persistance distante.

Aucun secret, mot de passe, JWT, cookie, clé API ou Client Secret n’a été affiché, demandé ou écrit dans ce rapport. Aucun déploiement public, provisioning de base, création de bucket ou modification de données Appwrite n’a été réalisé.

> Verdict de cette livraison UI : **PASS pour la refonte et les validations locales ; MostaPlace reste READY AFTER CONFIGURATION, pas READY FOR PRODUCTION**, tant que Google OAuth réel et la persistance Appwrite distante ne sont pas homologués séparément.
