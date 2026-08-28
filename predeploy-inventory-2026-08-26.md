# Inventaire pré-déploiement MostaPlace

**Date :** 26 août 2026

## Architecture observée

Le projet contient un frontend React/Vite dans `client`, un backend Express/tRPC autonome dans `backend-local`, un adaptateur Appwrite, un `MemoryStore` local et des tests Vitest/Playwright. Les ports actifs au moment de l’inventaire sont `3000` pour le backend et `5174` pour le frontend.

Les pages principales présentes sont : accueil, authentification, profil, publication, annonces personnelles, détail d’annonce, favoris, messages, commandes, modération, assistant IA, boutiques virtuelles, locations, emploi, informations publiques et récupération de mot de passe.

Les domaines backend identifiés sont : authentification, annonces, recherche, assistant IA, upload média, profil, favoris, conversations, messages, notifications, commentaires, signalements, modération, journal d’audit, commandes, évaluations, boutiques, locations, emploi, paiement Chargily et santé serveur.

## Scripts vérifiés

Le projet fournit des scripts distincts pour le développement frontend/backend, le build, les contrôles TypeScript, les tests Vitest, les E2E Playwright, les probes Storage, l’audit Database Appwrite, les sessions QA et le provisioning Appwrite. Aucun script de déploiement public n’a été lancé.

## État non sensible des environnements

Le fichier `.env.qa.local` existe mais ses cinq secrets QA attendus sont vides dans l’environnement observé : e-mails/mots de passe A/B et clé API Appwrite. Le projet ID qui y figure est également un placeholder. Le backend `.env` contient des identifiants de collections et des paramètres de configuration, mais le projet ID et plusieurs paramètres opérationnels sont des placeholders ; aucune clé Appwrite serveur exploitable n’est disponible.

Conclusion : l’audit distant Appwrite, la persistance Database/Storage, l’isolation A/B réelle, le paiement distant et les scénarios OAuth dépendant d’une configuration externe ne peuvent pas être déclarés PASS à partir de cet environnement.

## Risques immédiats à examiner

1. Vérifier le fallback `MemoryStore` et empêcher qu’il soit confondu avec une persistance de production.
2. Vérifier CORS, absence de rate limiting, validation des entrées et contrôles de propriété sur toutes les procédures.
3. Vérifier que les URLs `localhost` et les placeholders ne puissent pas être utilisées comme configuration de production.
4. Vérifier que les fichiers médias et les annonces non approuvées restent inaccessibles publiquement.
5. Vérifier que les flux OAuth/e-mail/Storage restent clairement séparés entre tests locaux et opérations distantes.
