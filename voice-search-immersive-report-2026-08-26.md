# Rapport Tech Lead — Recherche vocale immersive MostaPlace

**Date :** 26 août 2026  
**Périmètre :** interface locale, backend local et préparation Appwrite read-only. Aucun déploiement public et aucune donnée Appwrite distante créée.

## Verdict

La nouvelle expérience de recherche vocale immersive est **intégrée et validée localement pour son interface, son contrat tRPC et ses règles de recherche**. Le verdict fonctionnel est **PASS local pour l’UI et les contrats**, avec deux éléments explicitement **EN ATTENTE** : la transcription audio réelle avec un fournisseur IA configuré et la requête Appwrite réelle après provisioning de la base.

> Il n’est pas techniquement honnête de promettre une « zéro latence » absolue. L’implémentation évite toutefois les bibliothèques d’animation lourdes, limite les animations à `transform`/`opacity`, et charge le module vocal uniquement après l’action utilisateur.

## Fonctionnalités livrées

| Domaine | Implémentation | État réel |
|---|---|---|
| Bouton vocal dans la barre | Commande `Lancer la recherche vocale` dans la barre existante | **PASS local** |
| Envol visuel | Overlay plein écran, flou, assombrissement, bouton centré avec `top:50%`, `left:50%`, `translate3d(-50%,-50%,0)` | **PASS visuel** |
| Aura d’écoute | Aura légère autour du micro, désactivée ou réduite avec `prefers-reduced-motion` | **PASS code/UI** |
| Silence | Analyse d’énergie via `AudioContext`/`AnalyserNode`, arrêt automatique après silence prolongé | **Implémenté, audio réel EN ATTENTE** |
| Langues | Sélecteurs Français, Darija algérienne et Anglais | **PASS UI** |
| Capture audio | `MediaRecorder`, conversion contrôlée en Data URL, arrêt des pistes et nettoyage du contexte audio | **Implémenté** |
| Contrat de recherche | Alias structurés `{ article, min_price, max_price }` en plus du contrat interne existant | **PASS tests backend** |
| Conversion Darija | `mlayen/mlyoun = 10 000 DZD`, `alf = 1 000 DZD`, formes arabes prises en charge | **PASS tests backend** |
| Comptage rapide | Helper serveur et helper client avec `Query.select(["$id"])` et `limit(1)` | **Implémenté, Appwrite réel EN ATTENTE** |
| Visibilité publique | Résultats limités aux annonces `status=published` et `aiDecision=approved` | **PASS code existant + contrôle backend** |
| Chargement différé | `VoiceSearchOverlay` et `HomeAIWidget` ne sont montés qu’à l’ouverture | **PASS build** |

La capture s’appuie sur l’API native `MediaRecorder`, conçue pour enregistrer les données audio produites par le navigateur [1]. Le code ne demande pas d’accès micro avant l’action utilisateur et arrête les pistes dès la fermeture ou la fin de l’enregistrement.

## Contrat de recherche

Le parseur conserve les champs internes `query`, `minPrice` et `maxPrice` afin de ne pas casser les pages existantes. Le routeur tRPC renvoie simultanément les alias demandés par la spécification :

```json
{
  "article": "telephone",
  "min_price": null,
  "max_price": 30000
}
```

La phrase Darija latine `Choufli telephone b 30 alf` produit `max_price = 30000`. La phrase arabe `شوفلي تلفون ب 30 ألف` produit également `max_price = 30000`. La forme automobile `tomobil fiha sbigha, raccord et m9yoss` produit des notes techniques séparées, destinées à être confirmées par le vendeur.

Le message d’annonce vocale est affiché après le retour visuel du bouton : `Kayen X articles li y9edrou ye3jbouk sur le store.` Le total provient du backend tRPC en mode local et du total Appwrite lorsque le runtime Appwrite sera effectivement provisionné.

## Optimisation Appwrite

Le serveur utilise maintenant une sélection légère des champs pour les recherches, et le client expose `countPublicAppwriteListings()` avec filtres de catégorie, wilaya et prix. Les requêtes utilisent `Query.select()` pour limiter les attributs transférés, conformément au mécanisme de sélection d’attributs documenté par Appwrite [2].

La requête distante garde systématiquement les deux conditions de sécurité `status=published` et `aiDecision=approved`. Les annonces en attente ou rejetées ne doivent donc pas apparaître dans le comptage ni dans les résultats publics. La base Appwrite de MostaPlace n’étant pas encore provisionnée par décision utilisateur, aucune preuve de comptage distant n’est déclarée.

## Preuve visuelle

L’accueil temporairement exposé a été vérifié en lecture seule. Le bouton vocal est visible dans la barre de recherche. Après activation, l’écran affiche l’overlay `Recherche vocale immersive`, le titre `Parlez naturellement à MostaPlace`, un arrière-plan assombri et flouté, le bouton micro central, ainsi que les options `FR`, `DZ` et `EN`.

Dans cette vérification, la permission microphone n’a pas été accordée. L’interface a correctement affiché un état de repli avec l’icône muette et le message invitant à recommencer, sans simuler une capture ni envoyer un faux audio. La preuve détaillée est jointe dans `voice-search-visual-evidence.md`.

## Fichiers créés ou modifiés

| Fichier | Rôle |
|---|---|
| `client/src/components/VoiceSearchOverlay.tsx` | Nouveau composant lazy de capture vocale, silence et overlay immersif |
| `client/src/pages/HomePage.tsx` | Bouton vocal dans la barre, montage lazy, résultat et message de comptage |
| `client/src/pages/template-home.css` | Centrage, flou, aura, transitions GPU et responsive mobile |
| `client/src/lib/appwrite.ts` | Helper read-only `countPublicAppwriteListings()` avec sélection `$id` |
| `backend-local/src/appwrite.ts` | Sélections légères, filtres approuvés et comptage Appwrite serveur |
| `backend-local/src/router.ts` | Alias structurés et raccordement du total filtré |
| `backend-local/tests/marketplace.integration.test.ts` | Tests des montants latins/arabe et du contrat vocal |
| `e2e/critical-paths.spec.ts` | Test UI de l’ouverture et fermeture de l’overlay vocal |
| `voice-search-visual-evidence.md` | Constats visuels anonymisés de la vérification navigateur |

Aucun package d’animation ou dépendance lourde n’a été installé. Le build produit un chunk dédié `VoiceSearchOverlay` d’environ **4,45 kB**, soit environ **1,98 kB gzip**, ce qui confirme le découpage du module vocal dans un fichier séparé.

## Validation technique

| Contrôle | Résultat |
|---|---:|
| `pnpm check` | **PASS** |
| `pnpm backend:check` | **PASS** |
| `pnpm backend:test` | **PASS — 14/14 tests** |
| `pnpm test` | **PASS — 8/8 tests** |
| `pnpm build` | **PASS** |
| `pnpm test:e2e` | **PASS — 72/72 desktop/mobile** |
| Vérification visuelle overlay | **PASS local** |
| Permission microphone réelle | **EN ATTENTE** |
| Transcription Darija par fournisseur IA | **EN ATTENTE — fournisseur non configuré** |
| Comptage réel Database Appwrite | **EN ATTENTE — base non provisionnée** |

## Reprise ultérieure obligatoire

Après configuration sécurisée du fournisseur IA côté backend, il faudra tester un enregistrement réel en Darija algérienne, vérifier le texte retourné, contrôler les montants extraits et confirmer que la recherche finale respecte les annonces approuvées. Il faudra ensuite provisionner Appwrite, exécuter la requête de comptage read-only et vérifier que les attributs sélectionnés correspondent bien au schéma distant.

La fonctionnalité est donc prête pour une **validation locale humaine du rendu**, mais elle ne doit pas encore être présentée comme une recherche vocale IA distante entièrement opérationnelle.

## Références

[1]: https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder "MDN — MediaRecorder API"

[2]: https://appwrite.io/docs/products/databases/queries "Appwrite — Query and database query documentation"
