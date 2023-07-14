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

    - observation() : Fonction permettant d'observer l'état de l'environnement

    - reward() : Fonction permettant à l'environnement de récompenser ou pénaliser l'agent en fonction de l'action qui a été éxécuté

    - done() : L'épisode est terminé ou non. Si c'est le cas, vous devrez peut-être mettre fin à la simulation ou réinitialiser l'environnement pour redémarrer l'épisode.

    - info() : Cette fonction fournit des informations supplémentaires en fonction de l'environnement, telles que le nombre de vies restantes ou des informations générales qui peuvent être utiles pour le débogage.

Pour ce faire, j'ai utilisé la librairie open source Gym qui permet de développer et de comparer des algorithmes d'apprentissage par renforcement en fournissant une API standard pour communiquer entre les algorithmes d'apprentissage et les environnements, ainsi qu'un ensemble standard d'environnements conformes à cette API. Depuis sa sortie, l'API de Gym est devenue la norme dans ce domaine.
