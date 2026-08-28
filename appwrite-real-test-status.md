Audit Appwrite réel — 26 août 2026

URL testée : https://cloud.appwrite.io/console/project-6a8b71c8002bdee73678

Résultat : la console a répondu « 404 Page not found ». Aucun accès authentifié au projet, aucun utilisateur, aucune session, aucun e-mail, aucun fournisseur Google, aucune permission et aucun événement n’a donc pu être vérifié dans Appwrite. Ce résultat ne constitue pas un PASS. Le code local et les tests locaux doivent être rapportés séparément des tests distants.


La console racine est accessible avec la session My Browser. Le projet `mostaplace` est visible, en région Frankfurt, avec l’identifiant affiché `6a8b71c8002bdee73678`. Deux plateformes Web sont configurées : `localhost` (mise à jour il y a 2 jours) et une plateforme `5173-...us4.manus.computer` (mise à jour il y a 1 jour). La page Auth affiche 5 utilisateurs et les onglets Users, Teams, Security, Templates et Settings. Aucun test d’inscription, e-mail, réinitialisation ou OAuth n’a encore été exécuté ; seules la visibilité de la console et la configuration générale ont été confirmées.


La page Auth > Settings est accessible. Les méthodes Email/Password, Phone, Magic URL, Email OTP, Anonymous, Team Invites et JWT sont listées. Tous les providers OAuth affichés sont marqués `disabled`, notamment Google. Aucun changement n’a été effectué. Une activation Google serait une modification de configuration externe nécessitant les identifiants OAuth Google et les URLs de redirection ; elle ne doit pas être improvisée. Le projet reste donc non validé pour Google OAuth réel à ce stade.


La page Auth > Users confirme 5 utilisateurs dans le projet. Les données personnelles n’ont pas été copiées ni exposées. Aucun compte n’est identifiable depuis l’interface comme compte de test dédié ; il est donc impossible de choisir un compte de test sûr pour vérifier la réception d’e-mails sans risquer d’utiliser une adresse réelle.

Validation locale frontend effectuée le 26 août 2026 : `pnpm check` réussi (TypeScript, exit 0) ; `pnpm test` réussi (2 fichiers, 6 tests) ; `pnpm build` réussi (Vite production) ; `pnpm exec playwright test --project=chromium` réussi (14/14). La suite complète initiale avait 14/14 desktop réussis mais 14/14 mobile en échec au lancement avec `Target page, context or browser has been closed` et un message DBus/UPower. Diagnostic isolé : l’émulation iPhone fonctionne avec une configuration minimale. Correction appliquée uniquement à `playwright.config.ts` : suppression de l’héritage global Desktop, déclaration explicite de `browserName: chromium` et des paramètres de lancement dans chaque projet. Revalidation complète réussie : 28/28 scénarios E2E (desktop + mobile) en 39,5 s.

Les E2E couvrent l’accueil, recherche, catégorie Immobilier, publication, Location, Emploi, Boutiques, connexion, Google OAuth affiché côté interface, SMS absent par défaut, confirmation de mot de passe, MostaPlace AI, pages légales/publiques, protection Mes annonces, 404 et champs d’upload. Cela valide le comportement frontend simulé/local, mais ne constitue pas encore un test réel de réception d’e-mail ni un login Appwrite distant. Une revalidation supplémentaire contre une instance Vite preview propre sur le port 4180 a confirmé 14/14 tests mobile réussis en 21,2 s ; le correctif de configuration est donc reproductible et indépendant des serveurs résiduels.

Test QA réel — soumission depuis l’hôte Appwrite autorisé `5173-...us4.manus.computer` : l’interface MonstaPlace affiche `Compte créé. Consultez votre boîte e-mail pour confirmer votre adresse.` Ce message frontend confirme que la création et l’appel de vérification ont franchi le code applicatif, mais la confirmation de l’utilisateur dans Appwrite et la réception réelle de l’e-mail restent à vérifier séparément.

Vérification console immédiatement après la soumission : Appwrite affiche l’utilisateur `MostaPlace QA` avec l’adresse QA, un identifiant utilisateur généré et le statut `Unverified`, rejoint il y a quelques secondes. L’appel frontend `createVerification` n’a pas remonté d’erreur et l’interface a affiché le message de confirmation d’envoi. Cela prouve que le compte existe et que l’API Appwrite a accepté la demande de vérification ; cela ne prouve pas encore que le message est arrivé dans Gmail. Le test est volontairement arrêté ici, sans accès à la boîte.

Après confirmation utilisateur « lien ouvert », la console Appwrite a été rechargée puis la fiche détaillée du compte a été ouverte. Le statut distant reste `unverified` et le bouton `Verify account` est encore proposé. Résultat : réception de l’e-mail = PASS ; ouverture du lien = déclarée par l’utilisateur ; changement effectif à `Verified` = FAIL/EN ATTENTE, car Appwrite n’a pas enregistré la vérification. Le bouton administratif n’a pas été utilisé afin de ne pas masquer un défaut du parcours e-mail. Le lien fourni a ensuite été relancé sur l’hôte autorisé ; le frontend a retiré le secret de l’URL après traitement, mais Appwrite a répondu 401. Le message utilisateur est incorrectement classé comme erreur SMS par `appwriteErrorMessage` lorsque le code 401 provient d’une autre opération.


La page Auth > Security est accessible. Valeurs visibles : limite de sessions actives par utilisateur à 10, durée de session à 365 jours, longueur minimale de mot de passe à 8. Les exigences de caractères et les politiques avancées (historique, dictionnaire, données personnelles) sont présentées mais leur état exact n’est pas entièrement lisible dans l’extraction ; aucun réglage n’a été modifié. Pour une marketplace publique, ces paramètres devront être revus avant production, mais toute modification distante doit être validée avec le propriétaire du projet et testée sur un compte dédié.


Dans Auth > Security, les facteurs MFA visibles sont TOTP, e-mail et téléphone cochés, tandis que le canal Custom ne l’est pas. Les politiques “Deny free emails” et “Deny aliased emails” apparaissent désactivées sur l’écran observé. Le MFA n’est pas forcément imposé aux utilisateurs ; il s’agit de facteurs disponibles. Le téléphone reste donc préparé mais non obligatoire côté inscription, conformément à la décision produit. Aucune modification n’a été effectuée dans Appwrite.


Audit Storage Appwrite : la première URL directe basée uniquement sur l’ID (`project-6a8b...`) renvoie une page 404 de console ; l’URL correcte utilise le slug de région `project-fra-6a8b71c8002bdee73678`. Avec cette URL, la page Storage est accessible et affiche 4 buckets dans le projet, sans exposer leurs noms ni modifier leur contenu. La persistance Appwrite Storage est donc présente côté console, mais les permissions, limites de taille/MIME et associations utilisateur doivent encore être vérifiées bucket par bucket ou via une clé serveur dédiée.


Audit Databases Appwrite : l’interface affiche un compteur `6` près de la section Databases, mais le panneau de contenu indique simultanément “Create your first database” et ne rend aucune base dans la liste. Cette divergence est un point bloquant à clarifier : elle peut provenir d’un chargement incomplet de la console, d’un mauvais contexte de projet ou de ressources non visibles. La présence réelle des collections `listings`, `orders`, `ratings`, `comments`, `media` et `transactions` n’est donc pas confirmée par l’interface seule ; aucune ressource n’a été modifiée.

Nouvelle vérification Storage : le compteur `4` reste présent, mais aucune ligne/carte de bucket n’est rendue, aussi bien en vue table qu’en vue grille. La console affiche donc un état incohérent similaire à celui des Databases. Le changement de vue n’a pas résolu l’anomalie et aucune ressource n’a été touchée.

Référence Storage Appwrite : la documentation officielle indique qu’un bucket sans permissions n’autorise aucun accès par défaut ; les permissions bucket s’appliquent à tous les fichiers, tandis que les permissions fichier nécessitent l’activation de File Security. Les restrictions de taille et d’extensions se configurent au niveau bucket, avec jusqu’à 100 extensions. Sources : https://appwrite.io/docs/products/storage/buckets, https://appwrite.io/docs/products/storage/permissions, https://appwrite.io/docs/advanced/security/permissions.

Google OAuth — vérification approfondie : la fiche Appwrite contient déjà un Client ID et un Client Secret enregistrés (le secret n’a pas été copié ni exposé). Le provider reste explicitement `disabled`. L’URI de callback générée par Appwrite est `https://fra.cloud.appwrite.io/v1/account/sessions/oauth2/callback/google/6a8b71c8002bdee73678`. La configuration avancée propose les prompts `None`, `Consent` et `Select account`. La fiche a été fermée avec Annuler ; aucun changement n’a été enregistré. D’après la documentation officielle Appwrite, il faut activer le provider puis autoriser exactement cette URI dans Google Cloud, avec les scopes de base `openid`, `userinfo.email` et `userinfo.profile` si demandés. Le frontend appelle déjà `createOAuth2Session` avec succès/échec redirigés vers l’origine de l’application, mais le test ne peut pas aboutir tant que Google reste désactivé.

Sources officielles OAuth conservées pour référence : Appwrite décrit la configuration Google à l’URL https://appwrite.io/integrations/oauth-google (Client ID/Client Secret Google Cloud, scopes `openid`, `userinfo.email`, `userinfo.profile`, puis URI callback Appwrite) ; la documentation générale OAuth2 est disponible à https://appwrite.io/docs/products/auth/oauth2 et confirme que l’URI de redirection doit être copiée depuis la fiche provider Appwrite vers Google Cloud. Le billet Appwrite https://appwrite.io/blog/post/appwrite-oauth confirme également que le provider doit être activé, configuré avec les identifiants Google et que le callback doit être autorisé côté fournisseur.


Validation backend locale : `pnpm backend:check` réussi (TypeScript, exit 0) et `pnpm backend:test` réussi (1 fichier, 5 tests). Le contrat local Express/tRPC reste donc cohérent après les changements de configuration Playwright. Les tests n’impliquent pas encore une base Appwrite distante ni l’envoi d’e-mails réels.

Constat session QA : après inscription Appwrite, les pages protégées affichaient encore « Connectez-vous », car `AuthPage.submitAppwrite()` ne relançait pas la requête tRPC `auth.me` après création de la session Appwrite. Correction locale minimale appliquée : `await auth.refetch()` après connexion Appwrite et après inscription Appwrite. Validation post-correction : `pnpm check`, tests unitaires et `pnpm build` réussis. Cette correction n’a modifié aucune API Appwrite ni donnée distante.

Accès serveur distant : aucune variable `APPWRITE_API_KEY` n’est présente dans `.env.local`, `backend-local/.env` ou l’environnement shell de cette copie QA. Il est donc impossible d’interroger directement l’API Admin Appwrite pour confirmer les identifiants de buckets, permissions et collections ; la console reste la seule source distante disponible dans cette session. Aucune clé n’a été inventée ou demandée automatiquement.

Plateformes Appwrite vérifiées : `localhost` et `5173-ih0mglu78hmyze6v7hj5m-8e2b6483.us4.manus.computer` sont les deux plateformes Web visibles, pour un total de 2. L’URL QA `4190-...` utilisée au premier essai n’était pas autorisée ; l’hôte `5173-...` l’était. L’instance corrigée `4191-...` n’est pas encore ajoutée à Appwrite, ce qui explique qu’elle ne soit pas adaptée à un nouveau test distant de session tant qu’aucune plateforme n’est ajoutée.

Databases — nouvelle vérification : après navigation directe dans la console, le compteur `6` est toujours affiché, tandis que la liste reste vide avec `Create your first database`, sans pagination ni ligne sélectionnable. La cause exacte ne peut pas être confirmée depuis l’interface seule : il s’agit au minimum d’une incohérence de rendu/chargement ou d’un compteur non synchronisé avec le contexte courant. La vérification API Admin est bloquée par l’absence de clé serveur ; aucune base n’a été créée, supprimée ou recréée.


Audit des variables d’environnement : `.env.local` frontend contient les noms `VITE_APPWRITE_ENDPOINT`, `VITE_APPWRITE_PROJECT_ID` et `VITE_APPWRITE_BUCKET_ID`. Le modèle `backend-local/.env.example` prévoit bien `APPWRITE_API_KEY`, les identifiants de base/collections, bucket, ainsi que les collections métier. Aucun nom de variable Appwrite/Brevo/Chargily/SMTP/DATABASE n’est exposé dans l’environnement du shell utilisé pour l’audit. La clé serveur Appwrite et les identifiants de collections ne sont donc pas disponibles ici pour effectuer un test distant authentifié ; ils ne doivent pas être demandés ou écrits en clair dans le rapport.

Audit Storage côté code : le frontend limite les images à JPEG/PNG/WebP/AVIF et 10 Mo, redimensionne à 2400 px maximum et tente une conversion WebP qualité 0,84 si le résultat est plus léger. Le backend revalide le MIME et la taille via `storage.getFile`, génère un chemin logique `uploads/users/{userId}/{resourceType}/{resourceId-or-userId}/{fileId}`, enregistre la relation dans `media`, et supprime/remplace les fichiers au niveau serveur. Le bucket provisionné par script est `listing-media`, lecture publique au niveau bucket, limite 10 Mo et extensions jpg/jpeg/png/webp/avif. Point à vérifier en production dans la console : File Security, permissions d’écriture/création et possibilité d’accès public aux avatars ; le code ne permet pas de confirmer ces réglages distants sans API Admin.

Netlify — lecture via le connecteur autorisé : aucun projet Netlify n’a été retourné (`get-projects` = liste vide). Le déploiement frontend Netlify n’est donc pas vérifiable comme existant dans cette session ; aucun déploiement ni changement de variables n’a été effectué. La prochaine étape de mise en ligne nécessitera le rattachement explicite du site Netlify et la configuration de `VITE_BACKEND_URL`, sans exposer de clé serveur au frontend.


Audit SMTP Appwrite : l’onglet Settings > SMTP indique que le serveur SMTP personnalisé est une fonctionnalité réservée à un plan payant, avec un bouton d’upgrade, et qu’aucun formulaire SMTP actif n’est disponible sur le plan actuel. Les e-mails Appwrite peuvent donc dépendre du service intégré/limites du plan ; la réception réelle d’un e-mail de vérification ou de récupération doit être testée avec une adresse dédiée, mais ne peut pas être homologuée depuis ce compte sans destinataire de test accessible.

67	Reprise récupération QA — après confirmation explicite : le formulaire frontend a déclenché la demande de récupération pour l’adresse QA et a affiché « Si cette adresse existe, un lien Appwrite de récupération a été envoyé. » Aucun accès à Gmail n’a été effectué. La réception de ce nouvel e-mail est EN ATTENTE de confirmation utilisateur avant ouverture du lien ou modification du mot de passe.

68	Le probe Appwrite séparant la création de session de `account.get()` a confirmé que les identifiants QA sont acceptés et qu’une session est créée côté service. Le refus suivant concerne la persistance du cookie dans le navigateur de preview intersite. Le frontend affiche désormais un diagnostic spécifique à cette situation.

69	Validation locale après correction : `pnpm check` réussi et 6 tests unitaires réussis.

70	Après correction de `PasswordRecoveryPage`, un nouvel envoi de récupération a été déclenché pour le compte QA autorisé. L’interface affiche à nouveau le message neutre « Si cette adresse existe, un lien Appwrite de récupération a été envoyé. » La réception de ce nouvel e-mail est EN ATTENTE de confirmation utilisateur. Aucun secret de lien n’a été copié ou enregistré.

71	Le correctif local est validé par TypeScript, 6 tests unitaires et le build frontend. Le composant lit désormais `window.location.search` directement et nettoie l’URL seulement après réinitialisation réussie.

72	Dernier renouvellement QA : après confirmation explicite, le frontend a déclenché une nouvelle demande de récupération pour le compte QA et a affiché le message neutre d’envoi accepté. La réception et l’ouverture du nouveau lien restent EN ATTENTE. Aucun secret n’a été lu, copié ou enregistré.

73	Résultat du dernier parcours de récupération : Appwrite a refusé la requête au moment de la réinitialisation. La rotation n’est pas validée ; aucun mot de passe n’a été forcé ni modifié administrativement.

74	Correctif frontend appliqué : `completeAppwritePasswordRecovery` intercepte désormais les erreurs Appwrite et distingue un lien invalide/expiré/déjà utilisé d’un refus générique. Le formulaire conseille de demander un nouveau lien sans modifier l’URL. Validation locale post-correctif : TypeScript PASS et 6 tests unitaires PASS.

75	Le probe direct a confirmé auparavant que l’ancien mot de passe est refusé, mais le nouveau mot de passe connu du test l’est aussi. La valeur effectivement saisie par l’utilisateur n’étant pas connue du probe et Appwrite ayant refusé la requête, le test de rotation reste FAIL/EN ATTENTE, sans conclure à un défaut de cryptographie ou de stockage du mot de passe.

76	Comparaison avec la spécification `pasted_content_4.txt` : le frontend Appwrite crée bien les comptes, sessions, vérifications et récupérations via le SDK Web. Le backend accepte un JWT Appwrite via `Authorization: Bearer` dans `context.ts`, mais ses procédures legacy `auth.login`, `auth.register`, `auth.logout` et `forgotPassword` restent basées sur `MemoryStore`; elles ne doivent pas être utilisées lorsque `VITE_AUTH_PROVIDER=appwrite`.

77	Cause racine supplémentaire corrigée : `client/src/main.tsx` envoyait auparavant le contenu de `sessionStorage.manus-cookie` comme un Bearer token si `createJWT()` échouait. Ce cookie est un identifiant de session local et n’est pas un JWT Appwrite ; le backend le rejetait avec `general_unauthorized_scope`. Le fallback a été supprimé. Désormais, le frontend transmet uniquement un JWT Appwrite valide ou aucun en-tête Authorization, conformément à la spécification.

78	Validation post-correction : TypeScript PASS, 6 tests unitaires PASS et build frontend PASS. Les tests distants de rotation du mot de passe restent NON VALIDATED/FAIL tant qu’un lien Appwrite frais n’est pas consommé avec succès.

79	Après suppression du fallback `manus-cookie`, un nouvel envoi de récupération a été déclenché pour le compte QA. L’interface affiche le message neutre d’envoi accepté. La réception, l’ouverture du nouveau lien et la réinitialisation restent EN ATTENTE de confirmation utilisateur. Aucun secret du lien n’a été capturé.

80	Validation directe Appwrite après réinitialisation confirmée : ancien mot de passe refusé avec `401 user_invalid_credentials` = PASS ; nouveau mot de passe temporaire QA accepté et session créée = PASS.

81	Cycle HTTP réel avec cookie Appwrite : création de session `201`, récupération du compte `200`, `emailVerification: true`, déconnexion `204`, nouvelle connexion `201`, récupération du compte `200`, `emailVerification: true`. La session et la reconnexion sont PASS. Le probe supprime ensuite la session finale pour ne pas laisser de session QA active.

82	Le test Node initial qui appelait `account.get()` sans cookie a échoué avec `general_unauthorized_scope`; il s’agissait d’une limite de persistance cookie du runtime Node, pas d’un échec du compte. Le probe HTTP avec conservation explicite de `Set-Cookie` a validé le parcours réel.

83	État publication après inscription réussie : la page `/publier` affiche l’avatar QA et le bouton `Se déconnecter`, ce qui prouve que l’interface reçoit un utilisateur authentifié. Les champs observés sont remplis (`maquillage`, prix `20000`, wilaya `Alger`, catégorie sélectionnée, description et une image). Aucune nouvelle soumission n’a été lancée automatiquement afin de ne pas créer une annonce de test sans validation explicite. Le journal backend local ne contient encore aucun appel de publication : le point exact reste à reproduire avec une soumission contrôlée ou à instrumenter côté frontend.

84	Après confirmation explicite, une soumission a été tentée depuis `/publier`. Le formulaire est resté affiché et le backend local n’a reçu aucun appel visible. La navigation brute vers `GET /v1/storage/buckets/listing-media/files` a répondu `404 storage_bucket_not_found`, mais cette requête ne portait pas l’en-tête `X-Appwrite-Project` du SDK : ce 404 n’est donc pas une preuve d’absence du bucket. La console Appwrite authentifiée confirme un seul bucket réel `listing-media`, dont la liste de fichiers affiche `Create your first file`. Aucun bucket ni fichier n’a été supprimé ou modifié.

85	La fiche Settings du bucket réel expose les rubriques Permissions, File security, Encryption, Antivirus, Compression, Image transformations, Maximum file size et Allowed file extension. Les valeurs détaillées des permissions ne sont pas encore homologuées par un probe authentifié avec en-tête projet/API ; le statut Storage reste donc non validé malgré la présence du bucket.

86	Lecture visuelle complémentaire de la fiche Settings : les interrupteurs File security, Encryption et Antivirus sont visibles, mais leur état ne doit pas être conclu à partir de la capture seule. Aucune modification n’a été effectuée ; une inspection DOM/console ou un probe authentifié est requis pour certifier On/Off.

87	Inspection DOM de la capture console authentifiée avant la mise à jour : le bucket était activé, File security et Encryption étaient activées, Antivirus était désactivé. La table Permissions montre `Users` avec Create coché et Read/Update/Delete non cochés. Après activation ciblée d’Antivirus, réactivation de File Security puis réactivation d’Encryption, Appwrite a affiché successivement `Listing media has been updated` et `Security has been updated`; la date du bucket est passée à 22:12. La capture DOM finale certifie les switches dans l’ordre : bucket activé, File security `true`, Encryption `true`, Antivirus `true`, Image transformations `true`. Les cases globales Users restent Create seul, sans Read/Update/Delete. Aucun fichier n’est présent dans le bucket après la tentative précédente.

88	Après le build du correctif, le retest navigateur sur `/publier` affiche bien l’avatar QA `H` et le bouton `Se déconnecter`, donc la session frontend/backend est active. La page de publication est rendue normalement ; les champs sont vides dans ce nouveau chargement, avec catégorie et wilaya par défaut. Le bouton doit maintenant rediriger vers `/` uniquement après succès de `ai.publish`, tandis qu’une erreur sera affichée dans le formulaire.

89	Test réel après confirmation : une annonce QA sans image a été soumise avec succès. Le navigateur a quitté `/publier` pour `/`, et la page d’accueil affiche `MostaPlace annonce QA`, `Alger`, `20 000 DA`, `Annonce disponible` dans les publications récentes/à la une. La redirection vers l’accueil et la création de l’annonce en mode backend actuel sont donc PASS pour ce scénario sans image. La persistance est celle du mode local observé ; le backend répond encore `memory-local` tant que la clé API Appwrite serveur n’est pas injectée.

90	Test réel avec image après correction du bucket : `storage-smoke.png` a été accepté par le champ fichier et son aperçu était visible. Lors de la soumission, l’application a affiché `Votre session Appwrite a expiré. Reconnectez-vous avant de gérer une image.` Aucun fichier n’a été confirmé dans le bucket et aucune seconde annonce n’a été confirmée. Le blocage actuel est donc la session Appwrite côté navigateur au moment de `account.get()`, pas une validation MIME ou une permission Storage démontrée.

91	Correctifs full-stack appliqués : `AuthPage` respecte maintenant `next=/publier` après reconnexion ; `PublishPage` redirige vers `/` après succès, protège le formulaire pendant la vérification de session, affiche l’erreur dans le formulaire et renvoie vers la connexion si le compte Appwrite a expiré ; `startLogin` conserve de façon sûre la route d’origine ; le décodage Base64URL du JWT gère le padding et le cache périmé est purgé avant chaque nouvelle session. Compilation TypeScript frontend et backend : PASS. Tests frontend : 8/8 PASS. Tests backend : 6/6 PASS. Les validations distantes Storage avec une session fraîche restent à retester.

92	Après ajout du journal HTTP sûr et redémarrage direct du backend TSX, `/health` répond 200 avec `database: memory-local`, et `GET /api/trpc/auth.me` sans Authorization répond `{"result":{"data":{"json":null}}}`. Le journal backend enregistre uniquement l’identifiant de requête, méthode, chemin, statut et durée. Cela confirme que le backend est joignable mais ne peut pas authentifier une requête sans JWT ; la clé API Appwrite serveur reste absente.

## Vérification console Database en lecture seule — 26 août 2026

La console Appwrite du projet `mostaplace` (`6a8b71c8002bdee73678`) affiche une base TablesDB réelle nommée `mostaplace`. La page Databases affiche `6` comme sélecteur d’éléments par page et indique `Total: 1` base ; le compteur 6 n’est donc pas le nombre de bases.

La navigation de la base affiche les tables `conversations`, `favorites`, `messages`, `MostaPlace listings`, `MostaPlace users` et `notifications`. En ouvrant `MostaPlace listings` en lecture seule, Appwrite affiche la table `listings`, mais le panneau Rows indique `You have no columns yet` : aucune colonne métier n’est actuellement visible dans cette table. La table `notifications` affichait le même état sans colonnes métier. Cette preuve contredit l’hypothèse d’un provisioning complet des schémas distants ; le script local `setupAppwrite.ts` n’a pas été exécuté sur ce projet, car `APPWRITE_API_KEY` est absent de l’environnement.

La commande réelle `pnpm appwrite:db-audit` a été exécutée et a renvoyé : `APPWRITE_API_KEY est requis. Audit en lecture seule annulé sans clé serveur.` Aucun document ou JSON de la base n’a été inventé. Les données de test de publication précédemment visibles étaient dans le fallback `memory-local`, pas une preuve de persistance Appwrite.

Aucun compte, document, colonne ou permission n’a été créé, supprimé ou modifié pendant cette vérification.


Nouvelle lecture console Database : la table `MostaPlace users` (`users`) existe dans la base visible, mais son onglet Rows indique également `You have no columns yet`, avec seulement les colonnes système `$id`, `$createdAt`, `$updatedAt` affichées. Aucune ligne métier n’est donc visible dans la console. Cette constatation est une preuve de l’état actuel de la ressource distante, pas un résultat simulé.


93 — Contrôle QA local : `.env.qa.local` existe avec les permissions `600`, mais `APPWRITE_QA_A_EMAIL`, `APPWRITE_QA_A_PASSWORD`, `APPWRITE_QA_B_EMAIL`, `APPWRITE_QA_B_PASSWORD` et `APPWRITE_API_KEY` sont vides ou des placeholders. `pnpm qa:sessions` s’arrête avant tout appel Appwrite avec `APPWRITE_QA_A_EMAIL and APPWRITE_QA_A_PASSWORD are required.` Aucune valeur secrète n’a été affichée ni copiée.

94 — Le backend local répond `200` sur `/health` avec `database: memory-local`; le frontend répond `200` sur le port local 5174. Les processus locaux restent actifs.


95 — Validation locale après correction du parcours visiteur : `pnpm check` PASS, `pnpm test` PASS (8/8), `pnpm build` PASS. La suite E2E complète `pnpm test:e2e` est PASS avec `70 passed` (desktop et mobile). Les anciens échecs provenaient de tests qui attendaient à tort le formulaire sécurisé de publication sans session, et d’un appel JWT Appwrite inutile qui retardait l’état visiteur de `/profil`. Les tests vérifient désormais la redirection réelle vers `/connexion` pour `/publier`; le client évite `createJWT()` lorsqu’aucun JWT Appwrite persistant n’existe, sans retirer la garde d’authentification ni autoriser une publication anonyme.

Ce PASS couvre le code et le comportement local du frontend en mode visiteur. Il ne prouve ni l’écriture dans Database Appwrite, ni l’upload dans Storage Appwrite, ni la persistance des conversations, commentaires, commandes ou avis.


96 — Campagne d’intégration backend locale ajoutée dans `backend-local/tests/marketplace.integration.test.ts` : séparation vendeur/acheteur, publication liée au vendeur, favoris, refus du contact sur sa propre annonce, conversation idempotente, messages et compteur non lus, refus d’accès croisé, signalement/modération avec archivage et refus des rôles insuffisants, ainsi que préconditions explicites pour commentaires, commandes et avis sans Appwrite. Après correction d’un type local tableau/page, `pnpm backend:check` PASS et `pnpm backend:test` PASS : 2 fichiers, 10 tests.


97 — Évolution Assistant/Pare-feu IA et règles algériennes : ajout de `backend-local/src/ai.ts` avec fournisseur OpenAI-compatible côté serveur, sorties structurées, vision, transcription audio, prompt Français/Anglais/Darija, conversion déterministe `1 mlyoun/mlayen = 10000 DZD`, `1 alf = 1000 DZD`, notes `sbigha/raccord/m9yoss`, et détection Flexy/CCP/acompte à score 90 %. Publication, modification, visibilité publique, messagerie et commandes sont protégées par la décision IA. Les messages frauduleux sont bloqués avant écriture et produisent une notification privée acheteur.

98 — Schéma Appwrite préparé mais non exécuté à distance : ajout des attributs `aiDecision`, `aiRiskScore`, `aiReasons`, `aiProvider`, `aiModel`, `aiLanguage`, `aiScannedAt`, `technicalNotes` et index `status_ai_createdAt` dans `setupAppwrite.ts`. Les annonces non approuvées ne reçoivent pas de lecture publique et les recherches filtrent `status=published` + `aiDecision=approved`.

99 — Validation locale après changements : `pnpm check` PASS, `pnpm backend:check` PASS, `pnpm backend:test` PASS — 2 fichiers, 13 tests ; `pnpm test` PASS — 2 fichiers, 8 tests ; `pnpm build` PASS ; `pnpm test:e2e` PASS — 70 scénarios desktop/mobile. Aucun appel Appwrite distant ni fournisseur IA externe n’a été utilisé par cette campagne de test.
