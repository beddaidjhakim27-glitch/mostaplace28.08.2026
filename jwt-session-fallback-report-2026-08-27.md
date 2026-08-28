# Correctif session Appwrite — repli JWT local

**Date :** 27 août 2026  
**Périmètre :** OAuth, e-mail/password, restauration de session, `client.setJWT`, localStorage et déconnexion. Aucun token réel n’a été enregistré dans ce rapport et aucun compte Appwrite n’a été modifié.

## Correctif appliqué

Le frontend conserve désormais deux représentations locales du même JWT :

1. `mostaplace.appwrite.jwt` contient le JWT avec son `expiresAt` calculé depuis le claim `exp`.
2. `appwrite_jwt` contient l’alias brut demandé pour compatibilité avec le navigateur et le code existant.

Le client Appwrite reçoit immédiatement le jeton avec `client.setJWT(token)` lorsque la valeur est restaurée ou créée. Les deux clés sont supprimées lorsqu’elles sont expirées, invalides ou lors de la déconnexion.

Le helper `getAppwriteUserWithJwtFallback()` est utilisé par les parcours d’inscription, de connexion e-mail, OAuth Google, téléphone et restauration de session. Il essaie d’abord `account.get()` avec un JWT local éventuellement restauré, crée ensuite un nouveau JWT via `account.createJWT()` après une session réussie, puis réessaie `account.get()` si nécessaire.

## Limite technique importante

Le JWT n’est pas une méthode permettant de créer une session Appwrite à partir de rien. `account.createJWT()` exige qu’Appwrite reconnaisse déjà une session valide, généralement via le cookie Appwrite ou un JWT déjà valide. Si le navigateur bloque totalement le cookie cross-site et qu’aucun JWT existant n’est présent, le repli ne peut pas s’auto-initialiser après OAuth. Dans ce cas, le problème résiduel est la politique de cookie/origine, pas le stockage local.

> Le stockage local réduit la dépendance au cookie après obtention d’un JWT, mais il ne contourne pas l’authentification Appwrite elle-même.

Le mécanisme est donc un **repli local contrôlé**, pas une preuve que Google OAuth est désormais PASS.

## Sécurité

`localStorage` est lisible par le JavaScript de l’origine. Il est donc moins résistant à une XSS qu’un cookie HttpOnly. Le repli est adapté au test local demandé, mais en production il faut privilégier une origine HTTPS cohérente, un domaine personnalisé commun ou une architecture backend qui conserve la session côté serveur. Le JWT est limité par son expiration Appwrite et supprimé à la déconnexion.

## Fichiers modifiés

| Fichier | Modification |
|---|---|
| `client/src/lib/appwrite-auth.ts` | Helper de restauration/création JWT raccordé à OAuth, e-mail/password, téléphone et session courante |
| `client/src/lib/appwrite.ts` | Alias `appwrite_jwt`, expiration, `client.setJWT`, nettoyage des deux clés |
| `client/src/lib/appwrite-upload.test.ts` | Tests de stockage/restauration/expiration du JWT et tests Storage existants conservés |

Le fichier `client/src/main.tsx` possédait déjà la restauration avant le premier appel tRPC et l’injection `Authorization: Bearer`; cette logique n’a pas été dupliquée.

## Validation locale

| Contrôle | Résultat |
|---|---:|
| TypeScript frontend | **PASS** |
| Tests frontend | **PASS — 10/10** |
| Build Vite | **PASS** |
| TypeScript backend | **PASS** |
| Session OAuth réelle avec Google | **NON VALIDÉE / BLOCKED** |
| Cookie cross-site Appwrite/localhost | **NON RÉSOLU PAR CODE SEUL** |
| Persistance Database Appwrite | **NON VALIDÉE** |

Aucun JWT réel n’a été affiché, copié ou inclus dans les pièces jointes.egl
