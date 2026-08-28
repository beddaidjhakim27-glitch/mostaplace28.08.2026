# Rapport Tech Lead — Assistant IA et pare-feu Darija de MostaPlace

**Date :** 26 août 2026  
**Périmètre :** validation locale, sans déploiement public, sans écriture distante Appwrite et sans fournisseur IA externe actif pendant les tests.  
**Verdict de cette itération :** **READY AFTER CONFIGURATION**. Le code est intégré et validé localement ; la vision, la transcription vocale et la persistance Appwrite restent à valider après configuration sécurisée.

## 1. Décision d’architecture

L’IA est désormais appelée uniquement côté backend. Le frontend ne reçoit jamais de clé, de jeton ou de secret. Le service `backend-local/src/ai.ts` accepte un fournisseur compatible avec l’API OpenAI via des variables serveur, produit des sorties structurées et applique d’abord les règles déterministes locales. Une requête LLM ne peut donc pas annuler une règle de sécurité locale.

Le pare-feu adopte une stratégie **fail closed** pour les annonces contenant des images ou nécessitant une analyse externe : sans fournisseur IA configuré, l’annonce devient `pending` et reste invisible du public. Les seuls contenus approuvés localement par les tests utilisent explicitement `AI_LOCAL_RULES_APPROVE=true` dans la suite Vitest ; cette variable de test ne doit pas être activée en environnement utilisateur ou de production.

## 2. Règles algériennes codées

| Règle | Comportement déterministe | Preuve locale |
|---|---|---|
| `1 mlyoun/mlayen` | `10 000 DZD` | PASS dans l’intégration backend |
| `1 alf` | `1 000 DZD` | PASS dans l’intégration backend |
| `3 mlayen` | `30 000 DZD` | PASS dans la recherche Darija |
| `150 mlyoun` | `1 500 000 DZD` | PASS dans la recherche Darija |
| `30 alf` | `30 000 DZD` | PASS dans la recherche Darija |
| `sbigha`, `raccord`, `صبغة`, `راكور` | note technique de peinture/retouche à confirmer | PASS |
| `m9yoss`, `مقيوس` | note technique de carrosserie légèrement touchée à confirmer | PASS |
| `Flexy`, `Versili CCP`, `acompte avant de voir` | blocage, score de suspicion `90 %`, notification rouge acheteur | PASS dans l’intégration backend |

> La conversion est volontairement codée comme règle métier locale. Elle ne dépend pas de l’interprétation variable d’un modèle linguistique.

Les expressions de fraude sont vérifiées avant l’écriture d’un message. Le message bloqué n’est pas stocké. Une notification privée est ajoutée à l’acheteur avec l’instruction de ne transmettre ni Flexy, ni CCP, ni acompte avant vérification. La création de commande exige également une annonce déjà approuvée par le pare-feu lorsque la persistance Appwrite est active.

## 3. Parcours fonctionnels intégrés

L’écran `/assistant` permet maintenant la recherche conversationnelle texte, la sélection Français/Anglais/Darija algérienne, la recherche par image, la préparation d’un brouillon d’annonce à partir d’une image, et l’enregistrement vocal lorsque le navigateur autorise `MediaRecorder`. La transcription est envoyée au backend sous forme de données audio contrôlées ; si le fournisseur de transcription n’est pas configuré, l’interface affiche une indisponibilité explicite au lieu de simuler une transcription.

Les résultats de recherche renvoient les annonces approuvées, le prix, la wilaya, l’identifiant public et le nom public du vendeur, ainsi qu’un lien interne vers la fiche et la messagerie. Les filtres `minPrice` et `maxPrice` sont transmis au backend Appwrite avec les requêtes numériques correspondantes lorsque la base distante sera provisionnée.

Le brouillon d’annonce peut préremplir le titre, la description, la catégorie, une estimation de prix et les caractéristiques techniques. L’utilisateur doit encore relire et confirmer les informations. La publication et toute modification significative repassent par le pare-feu. Une annonce `pending` ou `rejected` n’est ni listée publiquement ni accessible par la route directe de fiche.

## 4. Fichiers modifiés

| Fichier | Modification principale |
|---|---|
| `backend-local/src/ai.ts` | fournisseur IA serveur, sorties structurées, vision, transcription, prompt multilingue, conversions Darija, jargon automobile et détection fraude |
| `backend-local/src/router.ts` | procédures assistant, recherche enrichie vendeur, publication/modification revalidées, blocage messages, garde commandes |
| `backend-local/src/store.ts` | statuts IA, score, motifs, fournisseur, date de scan et notes techniques |
| `backend-local/src/appwrite.ts` | champs IA, notes techniques, filtres publics, bornes de prix et permissions recalculées après modification |
| `backend-local/src/setupAppwrite.ts` | attributs et index nécessaires au provisioning futur |
| `backend-local/.env.example` | variables IA non secrètes et activation explicite |
| `client/src/pages/AssistantPage.tsx` | expérience multimodale texte/image/voix et résultats vendeur |
| `client/src/pages/PublishPage.tsx` | brouillon IA, notes techniques, décision du pare-feu et conservation des contrôles vendeur |
| `client/src/pages/MessagesPage.tsx` | affichage rouge du blocage et des alertes acheteur |
| `client/src/pages/HomePage.tsx` | affichage direct des résultats structurés IA |
| `backend-local/tests/marketplace.integration.test.ts` | tests de conversion, jargon, fraude, notifications et visibilité |

## 5. Preuves de validation locale

| Contrôle | Résultat réel |
|---|---:|
| `pnpm check` | **PASS** |
| `pnpm backend:check` | **PASS** |
| `pnpm backend:test` | **PASS — 13/13 tests** |
| `pnpm test` | **PASS — 8/8 tests** |
| `pnpm build` | **PASS** |
| `pnpm test:e2e` | **PASS — 70/70 scénarios desktop/mobile** |
| Appwrite Database distant | **NON CONFIGURÉ / non provisionné selon la décision utilisateur** |
| Fournisseur IA texte/vision | **NON CONFIGURÉ dans l’environnement de test** |
| Transcription Darija réelle | **EN ATTENTE de configuration et d’un fichier audio réel** |
| Analyse Vision réelle | **EN ATTENTE de configuration et d’une image réelle** |

Ces tests établissent la cohérence du code et du mode local. Ils ne prouvent pas la persistance Appwrite, la qualité réelle d’un modèle de vision ou la précision d’une transcription audio tant que les services externes ne sont pas injectés et testés séparément.

## 6. Configuration nécessaire avant activation réelle

Le fichier `backend-local/.env.example` documente `AI_ENABLED`, `AI_API_BASE_URL`, `AI_API_KEY`, `AI_MODEL`, `AI_TRANSCRIBE_MODEL` et `AI_TIMEOUT_MS`. La clé doit rester exclusivement côté serveur et être injectée par le mécanisme sécurisé de l’environnement d’exécution. Le fournisseur doit être activé seulement après un test contrôlé texte, vision et audio.

Le provisioning Appwrite devra ensuite ajouter les attributs IA et l’index prévus par `setupAppwrite.ts`, puis être vérifié par une campagne read-only : création d’une annonce de test, lecture du document, vérification de la décision IA, vérification des permissions, test d’isolation et suppression des médias rejetés. Aucune de ces étapes distantes n’a été exécutée dans cette itération.

## Références

[1]: https://appwrite.io/docs/products/databases "Appwrite — Databases documentation"

[2]: https://platform.openai.com/docs/guides/structured-outputs "OpenAI — Structured Outputs documentation"

[3]: https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder "MDN — MediaRecorder API"
