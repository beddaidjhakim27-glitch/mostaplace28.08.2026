# Rapport d’infrastructure Appwrite — MostaPlace

**Auteur :** Manus AI  
**Date :** 27 août 2026  
**Périmètre :** configuration backend locale, connectivité Appwrite read-only, suppression du fallback silencieux `memory-local` et validation de non-régression. Aucun déploiement public et aucune écriture distante Appwrite n’ont été effectués.

## Verdict

Le endpoint Appwrite Frankfurt est joignable depuis l’environnement d’exécution. Le diagnostic réseau a résolu DNS et TLS/HTTPS vers `fra.cloud.appwrite.io`, puis a reçu des réponses HTTP Appwrite. L’endpoint a répondu `401` sans authentification et la requête projet a également répondu `401`; cela indique une connectivité réseau fonctionnelle, mais ne fournit pas une preuve de clé serveur, de schéma Database ou de permissions.

Le fallback mémoire est maintenant **désactivé pour le profil backend local configuré**. `backend-local/.env` contient `PERSISTENCE_MODE=appwrite` et `REQUIRE_APPWRITE=true`. Au démarrage, le backend charge réellement `backend-local/.env`, constate l’absence de `APPWRITE_API_KEY` et s’arrête avec :

```text
Persistance Appwrite obligatoire : vérifiez APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID et APPWRITE_API_KEY. Le fallback memory-local est désactivé.
```

> **État actuel : BLOCKED jusqu’à injection sécurisée de `APPWRITE_API_KEY`.** Le site ne masque plus cette absence derrière `memory-local`.

## Configuration vérifiée

| Élément | Valeur/état non sensible | Résultat |
|---|---|---|
| Endpoint serveur | `https://fra.cloud.appwrite.io/v1` | Cohérent avec le projet Frankfurt |
| Project ID | `6a8b71c8002bdee73678` | Présent et cohérent avec les journaux précédents |
| Bucket public frontend | `listing-media` | Présent dans la configuration publique |
| Database ID attendue | `mostaplace` | Présente dans le backend local |
| Clé API serveur | Absente de l’environnement actuel | **BLOCKED** |
| Mode de persistance | `appwrite` | Actif |
| Fallback mémoire | Interdit par `REQUIRE_APPWRITE=true` | Actifement bloqué |
| Google Client ID/Secret | Non présents dans le frontend | Correct : ils doivent rester dans Appwrite/Google Cloud |

## Modifications appliquées

| Fichier | Modification |
|---|---|
| `backend-local/src/env.ts` | Nouveau chargeur déterministe de `backend-local/.env` via `dotenv`, exécuté avant la construction du runtime Appwrite |
| `backend-local/src/appwrite.ts` | Chargement du module d’environnement avant la lecture de `process.env` |
| `backend-local/src/server.ts` | Ajout de `PERSISTENCE_MODE`, `REQUIRE_APPWRITE`, démarrage fail-closed et diagnostic explicite de `/health`, `/api/health` et `/ready` |
| `backend-local/.env` | Activation de `PERSISTENCE_MODE=appwrite` et `REQUIRE_APPWRITE=true`; aucune clé secrète ajoutée |
| `backend-local/.env.example` | Modèle synchronisé avec le mode Appwrite obligatoire et l’endpoint Frankfurt |
| `tools/appwrite-network-diagnostic.mjs` | Nouveau diagnostic DNS/HTTPS/HTTP read-only, sans secret |
| `package.json` | Nouvelle commande `pnpm appwrite:network-diagnostic` |
| `docs/environment-production-template.md` | Structure finale publique/privée et règles Google OAuth/Appwrite |

## Commande de diagnostic réseau

Depuis :

```bash
cd /home/ubuntu/mostaplace-work/app/frontend_test_copy
pnpm appwrite:network-diagnostic
```

Le script vérifie uniquement DNS, HTTPS, endpoint Appwrite et réponse du projet. Il affiche `apiKeyPresent=true/false`, jamais la valeur de la clé. La sortie observée dans l’environnement actuel est un verdict `PASS_NETWORK_BLOCKED_AUTH_OR_PROJECT`, avec DNS fonctionnel et réponses Appwrite `401`.

Sur une machine locale, une vérification minimale équivalente est :

```bash
curl -i --max-time 15 https://fra.cloud.appwrite.io/v1/health
curl -i --max-time 15 \
  -H "X-Appwrite-Project: 6a8b71c8002bdee73678" \
  https://fra.cloud.appwrite.io/v1/account
```

Une réponse `401` ou `403` depuis Appwrite est différente d’un timeout ou d’une erreur DNS : elle prouve que la machine atteint Appwrite, mais pas qu’elle est autorisée à accéder à la ressource.

## Variables frontend publiques

À placer dans `client/.env.local` en test ou dans les variables publiques du build frontend :

```dotenv
VITE_BACKEND_URL=http://localhost:3000
VITE_RENDER_BACKEND_URL=
VITE_APP_URL=http://localhost:5173
VITE_APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
VITE_APPWRITE_PROJECT_ID=6a8b71c8002bdee73678
VITE_APPWRITE_BUCKET_ID=listing-media
VITE_APPWRITE_DATABASE_ID=mostaplace
VITE_APPWRITE_LISTINGS_COLLECTION_ID=listings
VITE_APPWRITE_NOTIFICATIONS_COLLECTION_ID=notifications
VITE_AUTH_PROVIDER=appwrite
VITE_AUTH_SMS_ENABLED=false
```

Ces variables sont publiques ou nécessaires au bundle Web. Elles ne doivent jamais contenir de clé API serveur, de secret Google, de JWT ou de secret webhook.

## Variables backend privées

À injecter dans `backend-local/.env` uniquement pour le test local, ou dans le gestionnaire de secrets du service backend en production :

```dotenv
NODE_ENV=production
PORT=3000
HOST=0.0.0.0
CORS_ORIGINS=https://frontend.example.com
PERSISTENCE_MODE=appwrite
REQUIRE_APPWRITE=true

APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=6a8b71c8002bdee73678
APPWRITE_API_KEY=<injectée hors chat et hors frontend>
APPWRITE_DATABASE_ID=mostaplace
APPWRITE_BUCKET_ID=listing-media
APPWRITE_USERS_COLLECTION_ID=users
APPWRITE_LISTINGS_COLLECTION_ID=listings
APPWRITE_FAVORITES_COLLECTION_ID=favorites
APPWRITE_CONVERSATIONS_COLLECTION_ID=conversations
APPWRITE_MESSAGES_COLLECTION_ID=messages
APPWRITE_NOTIFICATIONS_COLLECTION_ID=notifications
APPWRITE_BANNERS_COLLECTION_ID=banners
APPWRITE_MEDIA_COLLECTION_ID=media
APPWRITE_COMMENTS_COLLECTION_ID=comments
APPWRITE_AUDIT_LOGS_COLLECTION_ID=audit_logs
APPWRITE_ORDERS_COLLECTION_ID=orders
APPWRITE_RATINGS_COLLECTION_ID=ratings
APPWRITE_TRANSACTIONS_COLLECTION_ID=transactions
APPWRITE_REPORTS_COLLECTION_ID=reports
APPWRITE_RENTALS_COLLECTION_ID=rentals
APPWRITE_JOB_SEEKERS_COLLECTION_ID=job_seekers
APPWRITE_VIRTUAL_SHOPS_COLLECTION_ID=virtual_shops
```

## Google OAuth : emplacement correct des identifiants

Aucune clé Google ne doit être ajoutée au `.env` frontend. Le **Client ID** et le **Client Secret** Google sont enregistrés dans le provider Google du projet Appwrite. Le frontend utilise `createOAuth2Session` et ne doit jamais connaître le Client Secret.

L’URI Appwrite précédemment observée pour Google est :

```text
https://fra.cloud.appwrite.io/v1/account/sessions/oauth2/callback/google/6a8b71c8002bdee73678
```

Google Cloud doit autoriser exactement l’URI générée par Appwrite et les origines réellement utilisées. L’ajout d’un secret Google dans `VITE_*` serait une erreur critique de sécurité.

## Validation après corrections

| Contrôle | Résultat |
|---|---:|
| `pnpm backend:check` | **PASS** |
| `pnpm backend:test` | **PASS — 14/14** |
| `pnpm check` | **PASS** |
| `pnpm test` | **PASS — 8/8** |
| `pnpm build` | **PASS** |
| `pnpm test:e2e` | **PASS — 72/72 desktop/mobile** |
| Démarrage avec Appwrite forcé sans clé | **PASS du garde-fou — arrêt explicite** |
| `/ready` avec Appwrite non injecté | **BLOCKED attendu** |
| Base Appwrite distante | **NON VALIDÉE** |
| Google OAuth complet | **BLOCKED** |

Les E2E restent une validation frontend locale : ils ne prouvent pas la persistance Database Appwrite. Pour obtenir `/ready=200`, une preuve `List/Get Documents` et l’isolation Storage A/B, il faut injecter la vraie clé serveur via un canal sécurisé, sans la communiquer dans le chat.

## Conclusion opérationnelle

La cause du `503` n’était pas une mauvaise orthographe de `https://fra.cloud.appwrite.io/v1` ni un mauvais Project ID. La cause immédiate était l’absence de clé API serveur et, auparavant, le fait que le backend ne chargeait pas explicitement son fichier `.env`. Cette seconde cause est corrigée. La première reste volontairement visible et bloquante.

Le backend mémoire n’est plus autorisé dans le profil de test réel. Dès qu’une clé Appwrite valide sera injectée dans l’environnement backend, le démarrage pourra établir le runtime Appwrite, puis `/ready` vérifiera réellement l’accès à la collection `listings`. Tant que cette injection n’a pas eu lieu, aucun état de persistance distante ne doit être déclaré PASS.
