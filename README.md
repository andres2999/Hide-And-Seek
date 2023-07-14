# Hide-And-Seek
### Renforcement Learning

Le but de ce projet est de créer une IA de dissimulation. A partir d'une matrice 12x12, l'IA doit apprendre à se cacher d'un joueur en adoptant un comportement qui soit le plus réaliste possible. Le joueur et l'IA sont placés au hasard. L'IA est considérée comme étant caché lorsqu'elle n'est pas visible par le joueur, c'est à dire, si au moins une case noire les sépare. De même l'IA est considérée comme démasqué si le joueur peut voir l'IA, c'est-à-dire, s'il n'y a que des cases blanches entre l'IA et le joueur. 

<p align="center">
  <img src="https://github.com/andres2999/Hide-And-Seek/assets/91212621/3d982ce6-c530-4b42-b105-6a6d008ccff2" />
</p>


### Architecture

Pour répondre à la problématique posée, j'ai crée une IA qui à partir d'un environnement de jeu donné est capable de se dissimuler de la position d'un joueur donnée qui elle reste fixée durant toute la partie.


L'architecture est principalement composée d'une classe environnement (appelé JumboMana) regroupant les différentes fonctions et composantes permettant la réalisation du jeu. La première étape a consisté à définir l'environnement de jeu. Afin de créer des environnements qui soient les plus similaires possible de l'exemple donnée (ci-dessus), j'ai défini dans l'étape d'initialisation de la classe JumboMana des grilles de taille 12x12 générant aléatoirement pour chaque map différents clusters de cases noires. 

Voici ci-dessous les principales fonctions et composantes de la classe JumboMana : 

    - reset() : Fonction permettant de réinitialiser l'environnement à son état initial et renvoie l'observation de l'environnement correspondant à l'état initial

    - step() : Fonction permettant de prendre une action en entrée et de l'appliquer à l'environnement

    - compute_visibility_state() : Fonction qui renvoie le nombre de cases noires entre l'agent et le joueur

    - get_observation() : Fonction permettant d'observer l'état de l'environnement

    - calculate_reward() : Fonction permettant à l'environnement de récompenser ou pénaliser l'agent en fonction de l'action qui a été éxécuté selon les modalités suivantes : 
        * si l'agent fonce dans le mur, c'est-à-dire, qu'il touche une case noire alors le jeu s'arrête > pénalité
        * si l'agent entre en collision avec le joueur alors le jeu s'arrête > pénalité
        * plus le nombre de cases noires entre l'agent et le joueur augmente, moins l'IA est pénalisée
        * s'il y a au moins 3 cases noire entre l'agent et le joueur alors le jeu s'arrête > récompense

    - render() : Fonction qui permet d’afficher l’environnement

    - done() : L'épisode est terminé ou non. Si c'est le cas, vous devrez peut-être mettre fin à la simulation ou réinitialiser l'environnement pour redémarrer l'épisode.

    - info() : Cette fonction fournit des informations supplémentaires en fonction de l'environnement, telles que le nombre de vies restantes ou des informations générales qui peuvent être utiles pour le débogage.

Dans l'étape d'entrainement, j'ai utilisé la librairie open source Gym afin de pouvoir tester mon algorithme de renforcement sur l'environnement. 


### Étapes à suivre pour lancer le code

Le bon fonctionnement du jeu nécessite au préalable l'installation des packages Python suivants : Numpy, Gym, Time, Random, Bresenham, stable_baselines3, 
