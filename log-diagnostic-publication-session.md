# Diagnostic réel des logs — publication et session Appwrite

Date du contrôle : 26 août 2026.

## Conclusion

La cause immédiate de l’échec de publication avec image est une session Appwrite expirée ou non exploitable par le SDK Web au moment de l’appel `account.get()`. Le blocage intervient avant `storage.createFile()` et avant `ai.publish`; il ne s’agit donc pas d’un défaut de validation MIME confirmé ni d’un refus de la route de publication.

## Preuves observées

| Preuve | Observation réelle | Interprétation |
|---|---|---|
| Navigateur, soumission avec `storage-smoke.png` | Message exact : `Votre session Appwrite a expiré. Reconnectez-vous avant de gérer une image.` | Échec dans `requireCurrentAppwriteUserId()` à l’étape `account.get()`. |
| Fixture image | Le champ fichier a accepté `storage-smoke.png` et affiché son aperçu | Le champ HTML et la validation locale du format fonctionnent. |
| Bucket Appwrite | La console authentifiée montre `listing-media` réel et vide après l’échec | Aucun `createFile` n’a été confirmé ; pas de fichier orphelin créé par ce test. |
| Publication sans image | Soumission réussie, retour vers `/`, annonce `MostaPlace annonce QA` visible | La route `ai.publish` et la redirection de succès fonctionnent en mode local sans image. |
| Backend `/health` | HTTP 200, `database: memory-local` | Le backend est joignable mais n’utilise pas l’adaptateur Appwrite serveur. |
| Backend `auth.me` sans Authorization | Réponse JSON `null`, statut HTTP 200 | Sans JWT, le backend ne peut pas reconnaître l’utilisateur. |
| Logs backend | Après redémarrage avec journal sûr : méthode, chemin, statut et durée sont enregistrés ; aucun secret n’est journalisé | L’observabilité est maintenant disponible pour le prochain retest. |

## Cause technique

`PublishPage` traite d’abord les images. `uploadAppwriteImage()` appelle `requireCurrentAppwriteUserId()`, qui appelle `account.get()`. Si le cookie/session Appwrite n’est plus utilisable ou si le JWT local est périmé, cette fonction échoue volontairement et empêche la création du fichier et de l’annonce. L’ancienne interface laissait l’utilisateur sur le formulaire ; le message pouvait donner l’impression que le bouton ne faisait rien.

Une cause aggravante a été identifiée dans la persistance JWT : le décodage Base64URL ne complétait pas toujours le padding, ce qui pouvait appliquer une durée de secours de 15 minutes au lieu de l’expiration réelle. Le cache périmé pouvait aussi rester présent après une nouvelle tentative.

## Correctifs appliqués

Le frontend purge maintenant le JWT avant une nouvelle session Appwrite, gère correctement le padding Base64URL et efface le cache quand `createJWT()` ou `account.get()` échoue. `PublishPage` attend la vérification de session, redirige vers `/connexion?next=/publier` lorsqu’une session n’est plus valide, affiche l’erreur dans le formulaire et redirige vers `/` uniquement après succès de `ai.publish`. `AuthPage` respecte le paramètre `next` après reconnexion. `startLogin` conserve la route protégée de manière sûre.

Le backend dispose maintenant d’un journal HTTP non sensible. Il n’enregistre ni Authorization, ni cookie, ni corps de requête, ni secret. Il a été redémarré avec le binaire TSX existant après que `pnpm start` a été bloqué par la politique d’installation des scripts esbuild.

## Storage

Le bucket réel `listing-media` est activé. La console Appwrite certifie `Users` avec Create uniquement, sans Read/Update/Delete global. File Security, Encryption, Antivirus et Image transformations sont activés. Le bucket reste vide après le test image échoué. L’upload propriétaire et l’isolation A/B ne sont pas encore déclarés PASS tant qu’un retest avec une session fraîche n’a pas créé puis contrôlé un fichier.

## Blocage secondaire

`APPWRITE_API_KEY` serveur n’est pas disponible dans l’environnement backend. Le backend reste donc en `memory-local`; les annonces, messages, favoris, modération et commandes ne sont pas encore démontrés comme persistants dans Appwrite Database. Cette absence n’explique pas l’échec immédiat de `account.get()` côté navigateur, mais elle empêche la validation distante complète.

## Validation automatisée après correction

La compilation TypeScript frontend et backend passe. Les tests frontend passent à 8/8 et les tests backend à 6/6. Le test réel image reste en attente d’une reconnexion QA fraîche, puis doit confirmer successivement `createFile`, les permissions propriétaires, la publication, la visibilité après promotion et le nettoyage/rollback.

## Verdict

**Cause immédiate : session Appwrite expirée/non exploitable lors de `account.get()` avant l’upload.**

**Correction logicielle : appliquée et compilée.**

**Upload Storage réel avec session fraîche : EN ATTENTE.**

**Persistance Appwrite Database serveur : BLOQUÉE par l’absence de `APPWRITE_API_KEY`.**

**Production : NOT READY.**
