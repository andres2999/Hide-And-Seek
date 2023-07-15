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

    - generate_clusters() : Fonction qui génère des clusters de cases noires 

    - step() : Fonction permettant de prendre une action en entrée et de l'appliquer à l'environnement

    - compute_visibility_state() : Fonction qui renvoie le nombre de cases noires entre l'agent et le joueur

    - get_observation() : Fonction permettant d'observer l'état de l'environnement

    - get_observation_space() : Fonction qui permet de définir l'espace d'observation pour le modèle

    - calculate_reward() : Fonction permettant à l'environnement de récompenser ou pénaliser l'agent en fonction de l'action qui a été éxécuté selon les modalités suivantes : 
        * si l'agent fonce dans le mur, c'est-à-dire, qu'il touche une case noire alors le jeu s'arrête > pénalité
        * si l'agent entre en collision avec le joueur alors le jeu s'arrête > pénalité
        * plus le nombre de cases noires entre l'agent et le joueur augmente, moins l'IA est pénalisée
        * s'il y a au moins 3 cases noire entre l'agent et le joueur alors le jeu s'arrête > récompense

    - render() : Fonction qui permet de visualiser l’environnement

L'ensemble de définissions de la classe d'environnement JumboMana est contenue dans le fichier utils.py dans lequel vous pourrez visualiser plus en détails chacunes des fonctions précédemment énumérées. Les fichiers main.py et test.py permettent respectivement d'entrainer et de tester le modèle. Le fichier grid_gen.py permet de générer différents environnements de jeu et de les sauvegarder dans le fichier grid.pkl. Ces derniers sont ensuite utilisés lors de la phase d'entrainement du modèle. 

Fonctionnement de l'architecture du modèle et du jeu : 
  1) le modèle défini une position aléatoire du joueur dans l'environnement
  2) Le modèle défini ensuite la position de l'agent en fonction de celle du joueur, de sorte qu'il soit proche de lui
  3) Le modèle visualise l'état de l'environnement
  4) Le modèle décide de l'action à réaliser
  5) L'environnement prend en compte l'action ce qui génère une nouvelle observation de l'environnement et donc un nouvel état
  6) Les 3 dernières étapes sont réitérés jusqu'à ce que le modèle atteigne son objectif qui est de maximiser la somme de ses récompenses

Plusieurs stratégies ont étés utilisées lors de la phase d'entrainement pour améliorer les performances du modèle qui au départ avait beaucoup de mal à converger. Parmi les pistes envisagées et testées : 
  * Une première piste à consister à réaliser la phase d'entrainement sur des maps générés aléatoirement
  * Une deuxième piste à consister à modifier les positions de départ de l'agent et du joueur
  * Une troisième piste à consister à augmenter les montants des pénalités
  * Une quatrième piste à consister à complexifier les pénalités du modèle en introduisant notamment une pénalité sur l'angle formé par le triangle agent-joueur-case noire avec pour sommet de l'angle la case noire, de sorte que plus l'angle est proche de 180° moins l'agent est pénalisé 
  * Une cinquième piste à consister à modifier certains paramètres du modèle et notamment le timesteps

Parmi les difficultés que j'ai rencontré, l'une d'elle est que j'avais des observations (spaces.Box) de formats dictionnaires de plusieurs dimensions (un space pour la position du joueur, un autre pour la position de l'agent, un space pour la grille, et un autre pour la visibility_state) et cela a fortement perturbé au départ l'entrainement de mon modèle en générant des erreurs de TYPE et de DIMENSION. Pour solutionner ce problème, j'ai décidé d'utiliser des observations où l'on a qu'une seule space contenant les 4 informations précédentes. 

Le modèle final utilise un ensemble de maps spécifiques pour sa phase d'entrainement qui est préalablement généré et enregistré, ainsi qu'un gain décroissant des pénalités en fonction du nombre de cases noires entre l'agent et la joueur. Afin de permettre une meilleure visualisation des performances du modèle, j'ai choisi de fixé le "sucess" à 3 cases noires entre l'agent et le joueur. Pour déterminer le nombre de cases noires entre l'agent et le joueur, j'ai utilisé l'algorithme de Bresenham qui permet de tracer un segment entre les 2 positions et qui calcul le nombre de cases noires chevauchant cette droite. La principale métrique utilisée pour l'estimation de la performance du modèle est le reward_mean qui correspond à la récompense moyenne du modèle, de sorte que plus la récompense moyenne augmente plus le modèle performe. Bien que ce modèle ne soit pas le plus complexe, il reste néanmoins performant dans sa capacité à apprendre à se dissimuler d'un joueur. 

Les pistes à explorer pour l'amélioration du modèle pourrait être de l'entrainer davantage sur de nouveaux map plus complexes, une compléxification des règles de récompenses et pénalités, un finetunning des hyperparamètres du modèle ou encore une sélection beaucoup plus spécifiques des maps d'entrainements. 


### 2. Étapes à suivre pour reproduire les résultats

La reproduction des résultats nécessite en premier lieu l'installation des packages Python suivants : Numpy, Gym, Time, Random, Bresenham, Stable_baselines3. Une fois les packages installées, téléchargez l'ensemble des fichiers du répertoire courant. Une fois les téléchargements réalisés, il ne vous reste plus qu'à lancer le fichier test.py qui génèra les résultats du modèle que j'ai développé. 

Si vous désirez relancer l'entrainement du modèle sur de nouvelles maps, il vous suffit de de modifier dans l'étape d'initialisation de la classe d'environnement JumboMana les paramètres suivants : 
  - self.grid_size = 12 # taille de la grille
  - self.num_clusters = 5 # nombre de clusters de cases noires
  - self.cluster_size = 10 # taille des clusters de cases noires

Une fois les nouvelles caractéristiques des maps définies, il faudra exécuter grid_gen.py qui génèrera un ensemble de nouveaux maps qui seront enregistrés dans le fichier grid.pkl, à partir desquels l'étape d'entrainement pourra s'effectuer. Il ne vous restera plus qu'à exécuter les fichiers main.py (phase d'entrainement), puis le fichier test.py (phase de test). 
