# Hide-And-Seek
### Renforcement Learning

Le but de ce projet est de créer une IA de dissimulation. A partir d'une matrice 12x12, l'IA doit apprendre à se cacher d'un joueur en adoptant un comportement qui soit le plus réaliste possible. Le joueur et l'IA sont placés au hasard. L'IA est considérée comme étant caché lorsqu'elle n'est pas visible par le joueur, c'est à dire, si au moins une case noire les sépare. De même l'IA est considérée comme démasqué si le joueur peut voir l'IA, c'est-à-dire, s'il n'y a que des cases blanches entre l'IA et le joueur. 

<p align="center">
  <img src="https://github.com/andres2999/Hide-And-Seek/assets/91212621/3d982ce6-c530-4b42-b105-6a6d008ccff2" />
</p>


### 1. Architecture de l'IA

Pour répondre à la problématique posée, j'ai crée une IA qui à partir d'un environnement de jeu donné est capable de se dissimuler de la position d'un joueur donnée qui elle reste fixée durant toute la partie.


L'architecture est principalement composée d'une classe environnement (appelé JumboMana) regroupant les différentes fonctions et composantes permettant la réalisation du jeu. La première étape a consisté à définir l'environnement de jeu. Afin de créer des environnements qui soient les plus similaires possible de l'exemple donnée (ci-dessus), j'ai défini dans l'étape d'initialisation de la classe JumboMana des grilles de taille 12x12 générant aléatoirement pour chaque map différents clusters de cases noires. La création de l'environnement de jeu a nécesité l'utilisation de la librairie open source Gym afin de pouvoir tester par la suite mes algorithmes de renforcement sur l'environnement développé. L'algorithme de renforcement learning utilisé durant l'étape d'entrainement est le PPO (Proximal Policy Optimization) de la librairie stable_baselines3.

Voici ci-dessous les principales fonctions et composantes de la classe JumboMana : 

    - reset() : Fonction permettant de réinitialiser l'environnement à son état initial et renvoie l'observation de l'environnement correspondant à l'état initial

    - closest_position() : permet de définir la position aléatoire de l'agent en fonction du joueur (position proche et sans case noire entre les 2 au départ)

    - generate_clusters() : génère des clusters de cases noires 

    - step() : Fonction permettant de prendre une action en entrée et de l'appliquer à l'environnement

    - compute_visibility_state() : Fonction qui renvoie le nombre de cases noires entre l'agent et le joueur

    - get_observation() : Fonction permettant d'observer l'état de l'environnement

    - get_observation_space() : permet de définir l'espace d'observation pour le modèle

    - calculate_reward() : Fonction permettant à l'environnement de récompenser ou pénaliser l'agent en fonction de l'action qui a été éxécuté selon les modalités suivantes : 
        * si l'agent fonce dans le mur, c'est-à-dire, qu'il touche une case noire alors le jeu s'arrête > pénalité
        * si l'agent entre en collision avec le joueur alors le jeu s'arrête > pénalité
        * plus le nombre de cases noires entre l'agent et le joueur augmente, moins l'IA est pénalisée
        * s'il y a au moins 3 cases noire entre l'agent et le joueur alors le jeu s'arrête > récompense

    - render() : Fonction qui permet de visualiser l’environnement

L'ensemble de définissions de la classe d'environnement JumboMana est contenue dans le fichier utils.py dans lequel vous pourrez visualiser plus en détails chacunes des fonctions précédemment énumérées. Les fichiers main.py et test.py permettent respectivement d'entrainer et de tester le modèle. Le fichier grid_gen.py permet de générer différents environnements de jeu et de les sauvegarder dans le fichier grid.pkl. Ces derniers sont ensuite utilisés lors de la phase d'entrainement du modèle. 

Contcraitement, 



### 2. Étapes à suivre pour reproduire les résultats

La reproduction des résultats nécessite en premier lieu l'installation des packages Python suivants : Numpy, Gym, Time, Random, Bresenham, stable_baselines3. Une fois les packages installées, téléchargez l'ensemble des fichiers du répertoire courant. Une fois les téléchargements réalisés, il ne vous reste plus qu'à lancer le fichier test.py qui génèra les résultats du modèle que j'ai développé. Si vous souhaitez modifier les maps d'entrainem

Si vous désirez relancer l'entrainement du modèle sur de nouvelles maps, il vous suffit de de modifier dans l'étape d'initialisation de la classe d'environnement JumboMana les paramètres suivants : 
        - self.grid_size = 12 # taille de la grille
        - self.num_clusters = 5 # nombre de clusters de cases noires
        - self.cluster_size = 10 # taille des clusters de cases noires

Une fois les nouvelles caractéristiques des maps définies, il faudra éxécuter grid_gen.py qui génèrera un ensemble de nouveaux maps qui seront enregistrés dans le fichier grid.pkl, à partir desquels l'étape d'entrainement pourra s'effectuer. Il ne vous restera plus qu'à éxécuter les fichiers main.py (phase d'entrainement), puis le fichier test.py (phase de test). 

reward_mein : récompense moyenne (plus la récompense augmente plus le modèle performe)


Tester le test.py 

