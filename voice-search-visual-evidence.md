# Preuve visuelle — recherche vocale immersive

**URL vérifiée :** frontend local exposé temporairement `https://5174-ih0mglu78hmyze6v7hj5m-8e2b6483.us4.manus.computer/`.

Le 26 août 2026, l’accueil affiche bien un bouton `Lancer la recherche vocale` dans la barre de recherche. Après activation, le navigateur montre un overlay `Recherche vocale immersive` avec le titre `Parlez naturellement à MostaPlace`, un fond de page assombri et flouté, une commande micro dorée centrée, les choix `FR`, `DZ`, `EN`, et un bouton de fermeture `Fermer la recherche vocale`.

La permission microphone n’a pas été accordée pendant cette vérification en lecture seule ; l’interface a affiché le repli explicite `Appuyez sur le microphone pour recommencer.` au lieu de simuler une écoute. La capture audio réelle reste donc à tester avec une permission navigateur et un fournisseur de transcription configuré.
Après rechargement, le bouton central respecte visuellement le centrage écran : il apparaît au centre horizontal/vertical de la zone, avec l’aura latérale et l’arrière-plan flouté. Dans le navigateur de vérification, le microphone a été refusé ou indisponible : l’état affiché est `Arrêter l’écoute` puis l’icône muette et le message de repli, sans envoi d’audio. Les commandes FR/DZ/EN restent accessibles avant l’état d’erreur.
