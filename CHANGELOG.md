<!-- Ajoute ton changelog ici je rajouterai le tag -->

# Version 1.1

- UI Overhaul (Ameliorations, plus joli a regarder (fin j'espere), plus d'options)
- Le bouton load ouvre maintenant un menu qui permet de selectionner quel fichier on veut ouvrir
- Update a la derniere version de Snake Engine 2 (passage de la version 2.7.1.1 a la version 2.9.9.1) avec : Nouveau system de ui (Beaucoup plus facile de travailler avec), plus optimisé. Plusieurs Bug fixes. Utilisation facilitée de SE2. Changement au niveau du Renderer qui utilise graphics.py. Les &engine ne sont plus stockés individuellement dans chaque game_objects, l'engine est accessible avec la fonction `get_engine`. Une nouvelle fonctionalité permet de limiter le nombre de FPS pour le rendering
- FlappyBirdUI a ete entierement recode pour utiliser le nouveau systeme de UI
- Ajout de la fonction `get_save_files` qui renvoie une liste de noms de fichiers json depuis BASE_PATH avec leur extensions
- Changement de la fonction `load_birds` qui maintenant prend en argement une string `file_name` qui contient le nom du fichier et son extension a etre chargé
- la variable `scale` de FBEnvironments n'existe plus, comme maintenant une variable time_scale existe dans SnakeEngine2 qui est un facteur de delta_time, la vrai valeur de delta_time est accessible avec get_engine().real_delta_time
- Il existe maintenant 2 sliders : celui du haut permet de changer la vitesse a la quelle les objets bougent. L'autre controle time_scale

# Version 1.0

- ajout rectangle de couleur autour des oiseaux (la couleur est déterminée par les "poids" du cerveau de l'oiseau)
- implémentation du bouton save (avec `FsManager.py`), sauvegarde les cerveaux des oiseaux dans un fichier format `heures-minutes-secondes-jours-mois-années.json` dans le dossier `saved-brains`.
- Création de la fonction `load_birds` mais pas mise dans le bouton load, la fonction `load_birds` regarde si il existe un fichier `load_me.json` dans `saved-brains`.
