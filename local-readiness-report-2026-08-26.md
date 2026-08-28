# Rapport de préparation locale — MostaPlace

**Auteur : Manus AI**  
**Date : 26 août 2026**  
**Périmètre :** validation locale uniquement, sans déploiement public, sans provisioning ni modification Appwrite.

## Conclusion exécutive

Votre clarification est confirmée : la base métier et le backend n’ont pas encore été téléversés ou provisionnés sur Appwrite. L’état distant observé est donc **normal pour cette étape** : Appwrite contient des ressources de base visibles dans la console, mais aucune preuve exploitable de documents métier ou de schémas complets ne peut être présentée. Le backend local fonctionne volontairement en mode `memory-local`; une annonce créée pendant les tests locaux ne doit pas être interprétée comme une écriture Database Appwrite.

La validation locale a néanmoins été renforcée. Après correction des tests qui attendaient à tort une publication anonyme et après suppression de l’attente JWT inutile pour les visiteurs, le frontend passe **70/70 scénarios E2E desktop et mobile**. Le backend passe désormais **10/10 tests d’intégration métier**, en incluant deux comptes distincts, la propriété des annonces, les favoris, la messagerie, les signalements/modération et les préconditions explicites des fonctions qui nécessitent Appwrite.

## Résultats vérifiables

| Domaine | État | Preuve concrète | Limite à retenir |
|---|---|---|---|
| TypeScript frontend | **PASS** | `pnpm check` termine avec le code 0 | Ne prouve pas la persistance distante |
| Tests unitaires frontend | **PASS** | 2 fichiers, 8 tests réussis | Couverture ciblée, pas un test Appwrite |
| Build frontend | **PASS** | `pnpm build`, Vite termine avec succès | Ne prouve pas la configuration de production |
| E2E frontend desktop/mobile | **PASS** | `pnpm test:e2e` : 70 scénarios réussis | Parcours locaux sans compte QA distant |
| TypeScript backend | **PASS** | `pnpm backend:check` termine avec le code 0 | Backend en fallback local |
| Intégration métier backend | **PASS** | `pnpm backend:test` : 2 fichiers, 10 tests réussis | Les tests utilisent `MemoryStore` |
| Backend actif | **PASS local** | `GET http://127.0.0.1:3000/health` → `ok: true`, `database: memory-local` | Database Appwrite serveur non raccordée |
| Frontend actif | **PASS local** | Serveur Vite actif sur le port 5174, réponse HTTP 200 | L’URL localhost dépend de l’environnement qui exécute le serveur |
| Sessions QA A/B distantes | **BLOCKED** | `pnpm qa:sessions` s’arrête avant appel réseau : variables QA absentes ou vides | Le fichier existe, mais ses cinq valeurs sont encore des placeholders/valeurs vides |
| Database Appwrite | **NOT CONFIGURED** | Console : une base `mostaplace` et des tables visibles, mais `listings` et `users` affichent `You have no columns yet`; aucun document métier visible | Provisioning à effectuer plus tard, après les tests locaux |
| Preuve Get/List Documents Appwrite | **BLOCKED** | La clé API serveur n’est pas disponible dans `backend-local/.env` | Aucun JSON de document n’a été inventé |
| Storage Appwrite réel | **EN ATTENTE** | Le bucket `listing-media` existe dans la console et sa sécurité a été contrôlée historiquement | Aucun upload A/B complet n’est certifié dans cette campagne locale |
| Google OAuth réel | **FAIL / NON VALIDÉ** | La configuration a été préparée, mais le dernier parcours réel revenait avec `oauth=failed` | Ne pas déclarer Google fonctionnel avant un retour avec session active |
| SMS | **NOT CONFIGURED** | Fonctionnalité volontairement désactivée | Conforme à la priorité actuelle |

## Corrections appliquées pendant cette étape

Dans `client/src/main.tsx`, le client ne tente plus `account.createJWT()` lorsqu’aucun JWT Appwrite persistant n’existe. Les routes publiques ne restent donc pas bloquées par un appel distant inutile pour un visiteur anonyme. Lorsqu’une session Appwrite est réellement créée et persistée, le JWT est toujours relu et envoyé au backend.

Dans `e2e/critical-paths.spec.ts`, les assertions de publication ont été réalignées sur la règle de sécurité effective : un visiteur est redirigé vers `/connexion` et ne voit pas le formulaire de publication. Les tests ne contournent pas l’authentification et ne rendent pas la publication anonyme possible.

Dans `backend-local/tests/marketplace.integration.test.ts`, une campagne d’intégration locale a été ajoutée. Elle vérifie la liaison vendeur-annonce, le refus des modifications croisées, les favoris, le refus de contact de sa propre annonce, la création idempotente d’une conversation, l’envoi de messages, le compteur de messages non lus, les droits de modération et l’archivage d’une annonce signalée. Elle vérifie aussi que les commentaires, commandes et avis vérifiés renvoient une précondition explicite tant que Database Appwrite n’est pas raccordée.

## Ce que prouve réellement cette campagne

> **Le code local est testable et cohérent ; la persistance distante n’est pas encore activée.**

Les résultats locaux valident le comportement applicatif, les garde-fous de propriété et les rôles en mémoire. Ils ne certifient pas encore la création de documents dans les tables Appwrite, les permissions de collections, l’isolation Storage entre deux comptes, les notifications persistantes, les commandes ou les avis vérifiés en environnement distant.

La console Appwrite a bien affiché une base TablesDB réelle nommée `mostaplace` et six tables : `conversations`, `favorites`, `messages`, `listings`, `users` et `notifications`. Le nombre `6` affiché sur la page des bases correspond au sélecteur d’éléments par page ; la console indiquait `Total: 1`. Dans les tables `listings`, `users` et `notifications`, l’interface affichait uniquement les colonnes système et le message `You have no columns yet`. Il n’existe donc actuellement aucune preuve visuelle de documents métier ou de colonnes complètes.

## Reprise après votre téléversement Appwrite

Quand vous déciderez de raccorder la base et le backend, la reprise devra rester séquentielle et en lecture contrôlée. Il faudra d’abord injecter les variables dans l’environnement sécurisé, sans les transmettre dans le chat, puis vérifier uniquement `SET/ABSENT` et les permissions du fichier. Ensuite, la campagne pourra exécuter `pnpm qa:sessions`, `pnpm appwrite:db-audit` et, si les sessions QA A/B sont réellement valides, `pnpm storage:isolation-ab`.

L’audit Database devra alors fournir pour chaque collection l’identifiant, les attributs, les index, les permissions, le total et un échantillon anonymisé obtenu par un vrai `List/Get Documents`. Le provisioning éventuel devra être effectué par le script idempotent existant, après vérification de l’environnement et jamais pour masquer un échec de test. Les collections attendues devront au minimum couvrir les annonces, utilisateurs, conversations, messages, commentaires, favoris, commandes, évaluations, médias, notifications, signalements, journaux d’audit et transactions selon la configuration active du projet.

## Verdict de cette étape

| Verdict | Interprétation |
|---|---|
| **🟠 READY AFTER CONFIGURATION** | Prêt pour les tests humains locaux et pour le raccordement Appwrite ultérieur, mais pas pour déclarer la persistance distante ni la production. |
| Déploiement public | **NON EFFECTUÉ**, conformément à votre consigne |
| Action immédiate obligatoire | **Aucune** tant que vous n’avez pas choisi de téléverser/provisionner Appwrite |

## Références

[1]: `appwrite-real-test-status.md` — journal interne des vérifications Appwrite et des limites observées.

[2]: `backend-local/tests/marketplace.integration.test.ts` — campagne d’intégration locale ajoutée et exécutée.

[3]: `e2e/critical-paths.spec.ts` — assertions E2E des parcours publics et protections d’accès.

[4]: https://appwrite.io/docs/products/storage/permissions — documentation Appwrite sur les permissions Storage.

[5]: https://appwrite.io/docs/products/databases — documentation Appwrite sur les bases et collections.
