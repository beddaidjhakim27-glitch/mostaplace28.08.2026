# MostaPlace

MostaPlace est une marketplace React 19 + Vite avec un backend Express/tRPC local et une intégration Appwrite optionnelle selon l’environnement.

## Prérequis

Le projet nécessite Node.js 20 ou supérieur et pnpm. Les dépendances doivent être installées à la racine du projet.

## Installation locale

```bash
cd /home/ubuntu/mostaplace-work/app/frontend_test_copy
pnpm install
pnpm --dir backend-local install --ignore-scripts
```

Créer ensuite la configuration frontend à partir du modèle :

```bash
cp .env.example .env.local
```

Le frontend utilise par défaut `http://127.0.0.1:3000` comme backend local en mode développement. Le fichier `backend-local/.env.example` contient la configuration du serveur local. Le mode mémoire est utilisable sans secret pour les tests de raccordement ; les données sont perdues au redémarrage.

## Lancement local

Démarrer le backend dans un terminal :

```bash
pnpm backend:dev
```

Démarrer le frontend dans un second terminal :

```bash
pnpm dev
```

Ouvrir ensuite `http://localhost:5173`. Le contrôle de santé du backend est disponible sur `http://127.0.0.1:3000/health`.

## Tests locaux

Exécuter les contrôles statiques, unitaires et le build :

```bash
pnpm check
pnpm backend:check
pnpm test
pnpm backend:test
pnpm build
```

Exécuter les parcours E2E desktop et mobile :

```bash
pnpm test:e2e
```

La suite E2E démarre automatiquement les serveurs nécessaires lorsque le port de test est libre. Si un ancien serveur Vite occupe le port `4173`, l’arrêter avant de relancer les E2E afin d’éviter de tester un bundle obsolète.

## Configuration Appwrite

Les valeurs publiques frontend sont définies par les variables `VITE_*` dans `.env.local`. Le modèle utilise l’endpoint régional du projet MostaPlace et le bucket logique `listing-media`. Les clés serveur Appwrite ne doivent jamais être préfixées par `VITE_`, placées dans Netlify ou incluses dans le bundle navigateur.

Les validations authentifiées Appwrite utilisent un fichier local séparé, non versionné :

```text
.env.qa.local
```

Ce fichier peut contenir les comptes QA A/B et, uniquement côté terminal ou backend, la clé API Appwrite nécessaire à l’audit Database. Ne jamais copier ses valeurs dans le chat, les logs ou un commit.

Les probes disponibles sont :

```bash
pnpm qa:sessions
pnpm storage:isolation-ab
pnpm appwrite:db-audit
```

Ces commandes refusent de démarrer lorsque les variables requises sont absentes. Elles ne simulent aucun résultat PASS.

## Architecture de déploiement prévue

Netlify sert le frontend compilé. Render héberge le backend Express/tRPC. Le frontend appelle `${VITE_BACKEND_URL}/api/trpc`. La clé `APPWRITE_API_KEY` reste strictement côté backend Render et ne doit jamais apparaître dans une variable `VITE_*`.

Aucun déploiement public ne doit être effectué tant que les validations Appwrite Storage A/B, Database, Google OAuth et les parcours persistants de marketplace ne sont pas réellement terminés.

## Statut local actuel

La dernière régression locale validée comprend TypeScript frontend et backend, 8 tests unitaires frontend, 6 tests backend, 28 tests E2E desktop/mobile et le build Vite. Les validations Appwrite authentifiées restent distinctes et peuvent être classées `BLOCKED` si `.env.qa.local` n’est pas configuré.
