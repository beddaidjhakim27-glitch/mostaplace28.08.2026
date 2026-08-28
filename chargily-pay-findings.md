# Chargily Pay v2 — éléments vérifiés

Source webhook : https://dev.chargily.com/pay-v2/webhooks

Chargily envoie un POST HTTPS JSON. Le payload contient notamment `id`, `type`, `data`, `created_at` et `updated_at`. Un paiement réussi utilise l’événement `checkout.paid` et le statut `data.status = paid`. L’en-tête de signature s’appelle `signature`. La signature est un HMAC-SHA256 du payload brut avec la clé secrète API. La documentation demande de répondre HTTP 200 après traitement. L’URL webhook peut être enregistrée dans le dashboard développeur ou fournie lors de la création d’un checkout. Pour tester localement, un endpoint public temporaire est nécessaire.

Source checkout : https://dev.chargily.com/pay-v2/the-full-guide/create-a-checkout

La création de checkout utilise POST `https://pay.chargily.net/test/api/v2/checkouts` en mode test, avec `Authorization: Bearer <API_SECRET>` et `Content-Type: application/json`. L’exemple documenté utilise `items` avec un identifiant `price`, `quantity`, et `success_url`. La réponse contient `id`, `amount`, `currency` (`dzd`), `status` (`pending`), `success_url`, `checkout_url`, ainsi que les dates et informations de frais. Le client est redirigé vers `checkout_url`; la confirmation doit ensuite être traitée par webhook.

Implication pour MostaPlace : l’adaptateur doit mapper `checkout.id` vers `providerReference`, conserver la référence interne dans `metadata` lorsque le fournisseur le permet, vérifier `event.type`, `data.status`, montant et devise, puis rendre l’opération idempotente sur l’identifiant d’événement et la référence de checkout.
