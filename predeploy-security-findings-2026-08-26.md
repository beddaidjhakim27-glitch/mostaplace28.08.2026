# Constats sécurité et readiness — audit pré-déploiement

**Date :** 26 août 2026

## Protections déjà présentes

Le backend désactive `x-powered-by`, ajoute `nosniff`, `X-Frame-Options: DENY` et une politique de referer restrictive. Les cookies de session sont HttpOnly, avec SameSite configurable et Secure en production. Les procédures protégées vérifient l’authentification, le statut bloqué et les rôles administrateur/modérateur côté serveur. Les contrôles de propriété sont présents pour les annonces, conversations, messages, favoris et profils.

Les annonces publiques sont filtrées par `status=published` et `aiDecision=approved`. Le pare-feu fraude bloque les messages Flexy/CCP/acompte avant écriture. Le webhook de paiement vérifie une signature et une fenêtre temporelle avant de toucher une transaction.

## Constats à corriger ou à vérifier

| Constat | Niveau | État |
|---|---:|---|
| `.env.qa.local` contient des secrets vides et un projet placeholder | Bloquant distant | **BLOCKED** |
| `backend-local/.env` contient un projet placeholder | Bloquant distant | **BLOCKED** |
| L’audit `pnpm appwrite:db-audit` refuse honnêtement de démarrer sans clé serveur | Bloquant distant | **BLOCKED** |
| Le fallback `MemoryStore` n’est pas une persistance de production | Critique | **À maintenir explicitement interdit en production** |
| Runtime Appwrite à durcir contre les placeholders | Critique | **À corriger** |
| CORS doit ignorer les valeurs placeholder et refuser une configuration ambiguë | Élevé | **À corriger** |
| Endpoints IA publics potentiellement coûteux sans limite dédiée | Élevé | **À vérifier/corriger localement** |
| Preuves réelles OAuth, e-mail, Storage et Database | Critique distant | **EN ATTENTE de configuration externe** |
| Paiement distant et webhook provider | Critique distant | **EN ATTENTE de configuration provider** |

## Scan statique effectué

Aucune occurrence de `dangerouslySetInnerHTML`, affectation `innerHTML`, `eval`, `new Function`, désactivation TLS ou journalisation évidente de mot de passe/token/secret n’a été trouvée dans `client` ou `backend-local`. Les références localhost sont limitées au développement, aux exemples et à la configuration locale documentée ; elles devront être exclues ou remplacées dans tout environnement de production.

## Conclusion intermédiaire

Le socle local est exploitable pour poursuivre l’audit et les tests, mais ne doit pas être déclaré prêt à déployer tant que la configuration persistante Appwrite n’est pas injectée, que `/ready` ne répond pas positivement et que les parcours distants ne sont pas vérifiés. Les corrections locales prioritaires concernent la détection de placeholders, la configuration CORS et la limitation des endpoints IA publics.
