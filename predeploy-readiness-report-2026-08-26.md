# Rapport pré-déploiement MostaPlace

**Auteur :** Manus AI  
**Date :** 26 août 2026  
**Périmètre :** audit du workspace existant, corrections ciblées, validation locale et vérification read-only des dépendances/Appwrite. Aucun déploiement public, aucune migration destructive et aucune écriture distante n’ont été effectués.

## Verdict exécutif

MostaPlace dispose d’un socle local fonctionnel et testable. Les contrôles frontend/backend, le build, les parcours E2E desktop/mobile et l’audit de dépendances sont passés après les corrections appliquées. Le backend local répond correctement, mais `/ready` retourne encore `503 Appwrite non configuré` et `/health` indique explicitement `database: memory-local`.

> **Verdict : NOT READY FOR PRODUCTION.** Le projet est **READY AFTER CONFIGURATION** pour une phase de raccordement contrôlé, mais il ne faut pas le déployer tant qu’Appwrite, les variables de production, les tests distants et les intégrations externes ne sont pas homologués.

## Résultats vérifiables

| Contrôle | Preuve observée | État |
|---|---|---|
| TypeScript frontend | `pnpm check` exit 0 | **PASS** |
| TypeScript backend | `pnpm backend:check` exit 0 | **PASS** |
| Tests backend | Vitest `14/14` | **PASS** |
| Tests frontend | Vitest `8/8` | **PASS** |
| Build | Vite production exit 0 | **PASS** |
| E2E desktop/mobile | Playwright `72/72` | **PASS** |
| Audit dépendances production | `pnpm audit --prod` : aucune vulnérabilité connue | **PASS** |
| Frontend local | HTTP `200`, TTFB observé environ `9,7 ms` | **PASS local** |
| Backend `/health` | HTTP `200`, `database: memory-local`, environ `2,1 ms` | **PASS local / persistance absente** |
| Backend `/ready` | HTTP `503`, Appwrite non configuré, environ `1,2 ms` | **BLOCKED** |
| Origine locale autorisée | HTTP `200` + CORS pour `http://localhost:5174` | **PASS local** |
| Origine inconnue | HTTP `403` `Origine non autorisée.` | **PASS sécurité locale** |

Les mesures HTTP sont des mesures ponctuelles dans le sandbox et ne constituent pas un benchmark de production. Le build final pèse environ `56 MB` dans `dist`; le plus gros bundle JavaScript est d’environ `494,5 kB` avant gzip. Une optimisation ultérieure par découpage de l’entrée principale reste recommandée, mais aucune régression fonctionnelle n’a été observée.

## Corrections appliquées

### Configuration et sécurité serveur

Le runtime Appwrite refuse désormais les valeurs vides ou placeholders tels que `PLACEHOLDER`, `SET`, `YOUR_*` ou `CHANGE_ME`. En production, l’absence d’un runtime Appwrite valide provoque un échec immédiat au démarrage au lieu d’activer silencieusement le `MemoryStore`.

La configuration CORS ignore les placeholders, utilise les origines de développement uniquement hors production, exige une liste explicite d’origines en production et répond `403` aux origines déclarées mais non autorisées. Un rate limiting mémoire a été ajouté aux endpoints IA coûteux : transcription, recherche image, assistant, recherche texte et chat. Cette protection locale doit être remplacée ou complétée par un limiteur partagé Redis/API Gateway lors d’un déploiement horizontal.

### Appwrite, annonces et Storage

Le provisioning prévu ajoute désormais `technicalNotes` à la collection `listings` et augmente la taille du champ JSON `images` pour éviter le rejet d’une annonce contenant plusieurs URLs. Les annonces approuvées conservent la lecture `any` mais accordent également `update` et `delete` au propriétaire ; elles peuvent donc être modifiées ou supprimées sans rendre l’annonce publique modifiable par tous.

Le serveur vérifie avant l’enregistrement d’un média le MIME, la taille et les permissions du fichier Appwrite. Il exige que le compte courant possède `read`, `update` et `delete` sur le fichier. La fiche publique Appwrite utilise maintenant un `getDocument` direct filtré par `status=published` et `aiDecision=approved`, au lieu d’une liste limitée à 100 annonces.

### Validation d’entrée et dépendances

Les limites d’e-mail, mot de passe, nom et prix ont été renforcées côté tRPC. L’audit `pnpm audit --prod` avait détecté une vulnérabilité élevée dans `drizzle-orm@0.44.7`; le paquet a été mis à jour vers `0.45.2`, version corrigée selon l’avis de sécurité [1]. Aucun avis connu ne subsiste après la mise à jour.

## État Appwrite et intégrations externes

La commande read-only `pnpm appwrite:db-audit` a été exécutée. Elle s’est arrêtée avec `APPWRITE_API_KEY est requis. Audit en lecture seule annulé sans clé serveur.` Cette sortie est conforme au comportement attendu : aucun document, attribut ou permission n’a été inventé.

Les fichiers QA observés contiennent des entrées vides ou placeholders pour la clé API et les comptes A/B. Le backend local reste donc en `memory-local`. Les journaux Appwrite précédents montrent une base et des tables visibles dans la console, mais aucune preuve API actuelle de documents et de schémas métier complets. La Database, la persistance des annonces, la messagerie, les commentaires, les commandes et les avis restent **BLOCKED/EN ATTENTE**.

Les journaux antérieurs montrent également des blocages Google OAuth de type `400 invalid_request`, `409 user_already_exists` et un problème possible de cookie/session cross-site. Aucun nouveau parcours complet `Google → callback → session MostaPlace` n’a été homologué dans cette campagne. Google OAuth reste **BLOCKED**, même si du code frontend et une configuration Appwrite ont déjà été préparés.

L’e-mail QA a déjà fait l’objet de preuves historiques de réception, mais la chaîne complète ne peut pas être déclarée homologuée depuis un environnement sans secrets QA actifs. Storage dispose d’un bucket configuré côté console historique, mais l’upload propriétaire et l’isolation A/B réels ne sont pas PASS sans probe authentifié. Le paiement reste non homologué sans fournisseur, URLs de retour et webhook de production.

## Fichiers créés ou modifiés pendant cet audit

| Fichier | Nature du changement |
|---|---|
| `backend-local/src/appwrite.ts` | Refus des placeholders, vérification de propriété média, permissions propriétaire, lecture directe d’annonce |
| `backend-local/src/server.ts` | CORS fail-closed, 403 origine, rate limiting IA, garde de démarrage production |
| `backend-local/src/setupAppwrite.ts` | `technicalNotes` et taille d’images alignées sur l’adaptateur |
| `backend-local/src/router.ts` | Lecture publique directe, validations d’entrée renforcées |
| `backend-local/tests/marketplace.integration.test.ts` | Couverture contrat vocal/Darija et intégration marketplace |
| `package.json` et `pnpm-lock.yaml` | `drizzle-orm` mis à jour de `0.44.7` à `0.45.2` |
| `predeploy-inventory-2026-08-26.md` | Inventaire réel du workspace |
| `predeploy-security-findings-2026-08-26.md` | Constats de sécurité et readiness |
| `predeploy-readiness-report-2026-08-26.md` | Présent rapport |

## Blocages critiques avant déploiement

| Priorité | Action nécessaire | État |
|---:|---|---|
| 1 | Injecter de manière sécurisée un vrai runtime Appwrite côté serveur et renseigner les identifiants de collections | **BLOCKED** |
| 2 | Exécuter le provisioning sur une base Appwrite de staging après sauvegarde et vérifier les attributs/indexes/permissions | **EN ATTENTE** |
| 3 | Obtenir une preuve `List/Get Documents` anonymisée et un test de persistance annonce/média | **EN ATTENTE** |
| 4 | Exécuter l’isolation Storage A/B réelle avec deux sessions dédiées | **EN ATTENTE** |
| 5 | Finaliser Google Branding/Audience, vérifier les Authorized Origins/Redirect URIs et repasser le parcours réel | **BLOCKED** |
| 6 | Configurer l’URL backend frontend de production, CORS HTTPS et cookies `Secure`/`SameSite` selon l’architecture | **EN ATTENTE** |
| 7 | Homologuer paiement, webhook signé, e-mails, modération persistante et commandes/avis | **EN ATTENTE** |
| 8 | Remplacer ou valider le contenu juridique par le responsable légal | **EN ATTENTE** |

Les avertissements non bloquants relevés lors de l’installation sont la branche Recharts 2 dépréciée et un peer dependency de `@builder.io/vite-plugin-jsx-loc` prévu pour Vite 4/5 alors que le projet utilise Vite 7. Aucun de ces avertissements n’a cassé les contrôles actuels, mais ils doivent être traités avant une maintenance longue durée.

## Références

[1]: https://github.com/advisories/GHSA-gpj5-g38j-94v9 "GitHub Advisory — drizzle-orm SQL injection via improperly escaped SQL identifiers"

[2]: https://appwrite.io/docs/products/databases "Appwrite Databases documentation"

[3]: https://appwrite.io/docs/products/storage/permissions "Appwrite Storage permissions documentation"

[4]: https://appwrite.io/docs/products/auth/oauth2 "Appwrite OAuth2 documentation"
