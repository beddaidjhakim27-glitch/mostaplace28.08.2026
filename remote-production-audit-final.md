# Rapport final — Audit distant de production MostaPlace

**Date : 26 août 2026**  
**Compte QA : `beddaidjhakim1985@gmail.com`**  
**Projet Appwrite : `mostaplace` — ID `6a8b71c8002bdee73678`

## Synthèse exécutive

Le compte QA a été créé réellement dans Appwrite et apparaît avec le statut **Unverified**. MonstaPlace a accepté l’appel `createVerification` sans erreur, mais la réception du message dans Gmail reste volontairement **EN ATTENTE DE CONFIRMATION**. Aucun accès à Gmail n’a été effectué et aucun mot de passe n’a été demandé.

L’audit a également identifié et corrigé un défaut frontend concret : après une inscription ou une connexion Appwrite, l’état tRPC `auth.me` n’était pas systématiquement rafraîchi. Une actualisation explicite a été ajoutée après ces deux opérations. TypeScript, les tests unitaires et le build frontend réussissent après cette correction.

La validation distante complète reste bloquée par trois éléments indépendants du code local : la confirmation manuelle de l’e-mail QA, l’absence de clé API serveur Appwrite dans l’environnement d’audit pour interroger les ressources Admin, et l’absence de projet retourné par la lecture Netlify.

## Tableau des résultats

| Domaine | Statut | Résultat vérifié |
|---|---|---|
| Création compte QA | **PASS** | Utilisateur `MostaPlace QA` visible dans Appwrite, statut `Unverified`, créé quelques secondes après la soumission. |
| Génération demande de vérification | **ACCEPTÉE / réception en attente** | L’interface a affiché le succès et l’appel Appwrite n’a pas remonté d’erreur ; la boîte Gmail n’a pas été consultée. |
| Ouverture/validation e-mail | **EN ATTENTE** | À faire par le propriétaire dans la boîte de réception et les spams. |
| Connexion après vérification | **FAIL** | Appwrite retourne encore `401 general_unauthorized_scope` (`User role guests missing scopes [account]`) malgré l’activation Email/Password ; aucun contournement administratif n’a été utilisé. |
| Récupération mot de passe | **EN ATTENTE** | Dépend de la résolution du refus de session Appwrite ; aucun e-mail de récupération n’a été demandé afin de ne pas considérer le flux comme fonctionnel sans session stable. |
| Google OAuth | **BLOQUÉ — intervention requise** | Provider explicitement désactivé dans Appwrite ; Client ID et secret semblent déjà enregistrés, sans modification effectuée. |
| Storage | **PARTIELLEMENT VALIDÉ** | Compteur Appwrite `4`, mais aucune ligne/carte n’est rendue dans les vues table et grille. Les règles locales sont strictes. |
| Databases | **BLOQUÉ — anomalie console** | Compteur `6`, mais affichage simultané `Create your first database`, sans base sélectionnable. Aucune base créée/supprimée. |
| Netlify | **NON DÉPLOYÉ ou non rattaché** | La lecture Netlify a retourné une liste de projets vide. Aucun déploiement ni variable modifié. |
| Tests locaux | **PASS** | TypeScript, tests unitaires, build et 28/28 E2E déjà validés ; les E2E complets n’ont pas été relancés inutilement. |

## Google OAuth — décision nécessaire

Appwrite affiche le provider Google comme **disabled**. La fiche contient déjà des valeurs de Client ID et de Client Secret, mais le secret n’a pas été copié ni exposé. L’URI de callback générée par Appwrite est :

`https://fra.cloud.appwrite.io/v1/account/sessions/oauth2/callback/google/6a8b71c8002bdee73678`

Pour une activation correcte, il faut :

1. Dans Google Cloud Console, utiliser un client OAuth de type **Web application**.
2. Vérifier l’écran de consentement, le nom de l’application et l’e-mail de support.
3. Ajouter exactement l’URI de callback ci-dessus dans les **Authorized redirect URIs** Google.
4. Conserver les scopes de base `openid`, `userinfo.email` et `userinfo.profile` si Google les demande pour l’identité.
5. Vérifier que les domaines utilisés par l’application sont autorisés côté Appwrite : `localhost` et `5173-ih0mglu78hmyze6v7hj5m-8e2b6483.us4.manus.computer` sont actuellement visibles. L’hôte `4190-...` n’est pas autorisé et l’instance temporaire `4191-...` ne l’est pas non plus.
6. Activer Google dans Appwrite seulement après vérification du Client ID, du secret et du callback.
7. Conserver dans le frontend les URLs de succès et d’échec sur l’origine publique réelle, puis ajouter le domaine de production dans Appwrite avant le lancement.

**Recommandation :** ne pas activer le provider depuis la console tant que le propriétaire n’a pas confirmé le client Google et le domaine public définitif. La configuration du frontend est déjà préparée avec `createOAuth2Session`.

Références officielles : [1] [2] [3].

## Storage — audit technique

Le frontend accepte uniquement JPEG, PNG, WebP et AVIF, avec une limite de 10 Mo. Les images sont redimensionnées à 2 400 px maximum et une conversion WebP qualité 0,84 est tentée lorsqu’elle réduit effectivement la taille. Le backend revalide le MIME et la taille via l’objet distant Appwrite avant d’enregistrer la ligne `media`.

Les chemins logiques suivent la structure utilisateur/ressource, par exemple `uploads/users/{USER_ID}/profile/{FILE_ID}` ou `uploads/users/{USER_ID}/listing/{LISTING_ID}/{FILE_ID}`. Le backend enregistre `userId`, `resourceType`, `resourceId`, `logicalPath`, `fileId`, MIME, taille et statut, et contient une procédure de remplacement/suppression ainsi qu’un nettoyage des médias orphelins.

Le script de provisioning prévoit le bucket `listing-media`, 10 Mo maximum et les extensions `jpg`, `jpeg`, `png`, `webp`, `avif`. Le bucket donne une lecture publique pour les médias destinés aux annonces. Les points qui restent impossibles à confirmer sans API Admin sont l’existence détaillée des 4 buckets, File Security, les permissions effectives d’écriture et les paramètres d’encryption/compression.

La documentation officielle Appwrite confirme que les permissions sont refusées par défaut, que les permissions bucket s’appliquent à tous les fichiers, et que les permissions au niveau fichier dépendent de File Security [4] [5].

## Databases — cause déterminable à ce stade

L’interface Appwrite reproduit l’anomalie : le compteur `6` est affiché alors que le contenu indique `Create your first database`. Il n’existe ni ligne, ni pagination, ni base sélectionnable. Le problème ne vient pas d’une action de provisioning exécutée pendant cet audit : aucune base n’a été créée, supprimée ou recréée.

La cause exacte ne peut pas être prouvée depuis le seul rendu de la console. Deux hypothèses restent ouvertes : compteur de ressources non synchronisé avec le contexte de projet, ou échec de chargement de la liste côté console. La vérification définitive nécessite une lecture authentifiée de l’API Admin avec `APPWRITE_API_KEY`, qui n’est pas présente dans la copie d’audit. Les collections attendues sont documentées localement, mais leur existence distante n’est pas déclarée validée.

## Déploiement

La lecture Netlify a retourné une liste de projets vide. Aucun site frontend n’a été créé, sélectionné ou modifié. Le projet local prévoit correctement les variables `VITE_BACKEND_URL` et `VITE_RENDER_BACKEND_URL`; la clé `APPWRITE_API_KEY` reste réservée au backend Render et ne doit jamais être exposée à Netlify ou au bundle navigateur.

## Suite immédiate

La réception de l’e-mail QA est désormais **PASS**. L’ouverture du lien a été tentée, mais le frontend ne consommait pas initialement les paramètres `userId/secret`; un gestionnaire `account.updateVerification` a été ajouté. La nouvelle tentative a néanmoins reçu un 401 et Appwrite affiche encore `unverified`. Le message d’erreur générique a été corrigé pour ne plus attribuer à tort ce 401 au SMS. La connexion reste **FAIL** tant que le projet Appwrite refuse le scope `account` aux visiteurs/session QA. Les parcours récupération, nouveau mot de passe, reconnexion et déconnexion restent **EN ATTENTE** de cette résolution.

Pour lever les deux blocages techniques distants, il faudra ensuite disposer du domaine public définitif et d’une clé API serveur Appwrite configurée uniquement dans l’environnement backend Render. Il ne faut ni mettre cette clé dans Netlify, ni la transmettre dans le frontend, ni la consigner dans un rapport.

## Références

[1]: https://appwrite.io/integrations/oauth-google "Appwrite — OAuth with Google"
[2]: https://appwrite.io/docs/products/auth/oauth2 "Appwrite — OAuth2 authentication"
[3]: https://appwrite.io/blog/post/appwrite-oauth "Appwrite — How Appwrite handles OAuth"
[4]: https://appwrite.io/docs/products/storage/buckets "Appwrite — Storage buckets"
[5]: https://appwrite.io/docs/products/storage/permissions "Appwrite — Storage permissions"
[6]: https://appwrite.io/docs/advanced/security/permissions "Appwrite — Permissions"
