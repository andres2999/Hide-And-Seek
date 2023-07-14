import gym
from gym import spaces
import numpy as np
import pickle
import random
from bresenham import bresenham

# création de la classe d'environnement JumboMana
# class regroupant les différentes fonctionnalités du jeu
class JumboMana(gym.Env):
    def __init__(self):
        # initialisation des caractéristiques de l'environnement de jeu
        super(JumboMana, self).__init__()
        self.grid_size = 12 # taille de la grille
        self.num_clusters = 5 # nombre de clusters de cases noires
        self.cluster_size = 10 # taille des clusters de cases noires
        self.grid = None
        with open('grid.pkl', 'rb') as f:
            self.grid = pickle.load(f)
        self.agent_position = (1, 0)
        self.player_position = (0, 0)
        self.action_space = spaces.Discrete(8) 
        self.observation_space = self.get_observation_space()
        self.visibility_state = self.compute_visibility_state()

    # position du joueur    
    def random_position(self):
        while True:
            position = np.random.randint(self.grid_size, size=2)
            if self.grid[position[0]][position[1]] == 0:
                return tuple(position)

    # position de l'agent en fonction du joueur  
    def closest_position(self, position):
        min_distance = float('inf')
        closest_pos = None
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    distance = abs(position[0] - i) + abs(position[1] - j)
                    line = list(bresenham(position[0], position[1], i, j))
                    visibility_state = sum(self.grid[x][y] for x, y in line)
                    if visibility_state == 0 and distance < min_distance:
                        min_distance = distance
                        closest_pos = (i, j)
        if closest_pos is None:
            while True:
                x, y = np.random.randint(0, self.grid_size, size=2)
                if self.grid[x][y] == 0:
                    return (x, y)
        return closest_pos


    # calcul du nb de cases noires entre l'agent et le player                    
    def compute_visibility_state(self):
        line = list(bresenham(self.agent_position[0], self.agent_position[1], self.player_position[0], self.player_position[1]))
        visibility_state = sum(self.grid[x][y] for x, y in line)
        return visibility_state

    # génère des clusters de cases noires
    def generate_clusters(self, grid_size, num_clusters, cluster_size):
        grid = np.zeros((grid_size, grid_size), dtype=int)
        cluster_centers = [list(np.random.randint(0, grid_size, size=2)) for _ in range(num_clusters)]
        for center in cluster_centers:
            for _ in range(cluster_size):
                direction = np.random.randint(0, 4)
                if direction == 0:   # up
                    if center[0] > 0:
                        center[0] -= 1
                elif direction == 1:  # right
                    if center[1] < grid_size - 1:
                        center[1] += 1
                elif direction == 2:  # down
                    if center[0] < grid_size - 1:
                        center[0] += 1
                elif direction == 3:  # left
                    if center[1] > 0:
                        center[1] -= 1
                grid[center[0]][center[1]] = 1
        return grid.tolist()

    # ensemble d'actions possibles de l'agent à chaque step
    def step(self, action):
        new_position = list(self.agent_position)
        if action == 0:   # Move up
            new_position[0] = max(0, self.agent_position[0] - 1)
        elif action == 1:  # Move right
            new_position[1] = min(self.grid_size - 1, self.agent_position[1] + 1)
        elif action == 2:  # Move down
            new_position[0] = min(self.grid_size - 1, self.agent_position[0] + 1)
        elif action == 3:  # Move left
            new_position[1] = max(0, self.agent_position[1] - 1)
        elif action == 4:  # Move up-right
            new_position[0] = max(0, self.agent_position[0] - 1)
            new_position[1] = min(self.grid_size - 1, self.agent_position[1] + 1)
        elif action == 5:  # Move down-right
            new_position[0] = min(self.grid_size - 1, self.agent_position[0] + 1)
            new_position[1] = min(self.grid_size - 1, self.agent_position[1] + 1)
        elif action == 6:  # Move down-left
            new_position[0] = min(self.grid_size - 1, self.agent_position[0] + 1)
            new_position[1] = max(0, self.agent_position[1] - 1)
        elif action == 7:  # Move up-left
            new_position[0] = max(0, self.agent_position[0] - 1)
            new_position[1] = max(0, self.agent_position[1] - 1)
        
        self.agent_position = (new_position[0], new_position[1])
        self.visibility_state = self.compute_visibility_state()
        reward, done = self.calculate_reward()
        return self.get_observation(), reward, done, {}
    
    # système de récompenses/pénalités
    def calculate_reward(self):
        # si l'agent fonce dans le mur (touche une case noire) le jeu s'arrête + pénalité
        if self.grid[self.agent_position[0]][self.agent_position[1]] == 1:
            print("Mur")
            return -1000.0, True
        # si l'agent entre en collision avec le player le jeu s'arrête + pénalité
        elif self.agent_position == self.player_position:
            print("Col")
            return -1000.0, True
        # le jeu s'arrête lorsque l'agent a réussi à se cacher du player (3 cases noires entre les 2) + récompense
        elif self.visibility_state >= 3:
            print("Success")
            #self.render()
            return 10.0, True
        # plus le nombre de cases noires entre l'agent et le player augmente, moins l'IA est pénalisée
        if self.visibility_state < 3:
            return (self.visibility_state*10)-10, False

    #  réinitialisation de l'environnement à son état initial
    def reset(self):
        with open('grid.pkl', 'rb') as f:
            self.grid = pickle.load(f)
        self.agent_position = (1, 0)
        self.player_position = (0, 0)
        self.visibility_state = self.compute_visibility_state()
        return self.get_observation()

    # observation de l'état de l'environnement
    def get_observation(self):
        flattened_grid = np.array(self.grid).flatten()
        normalized_agent_pos = np.array(self.agent_position) / self.grid_size
        normalized_player_pos = np.array(self.player_position) / self.grid_size
        return np.concatenate([flattened_grid, normalized_agent_pos, normalized_player_pos, [self.visibility_state]])

    # espace d'observation du modèle
    def get_observation_space(self):
        grid_elements = self.grid_size * self.grid_size 
        return spaces.Box(low=0, high=1, shape=(grid_elements + 5,), dtype=np.float32)


    # visualisation de l'environnement
    def render(self, mode='human'):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    print('■', end=' ')
                else:
                    if i == self.agent_position[0] and j == self.agent_position[1]:
                        print('A', end=' ')
                    elif i == self.player_position[0] and j == self.player_position[1]:
                        print('P', end=' ')
                    else:
                        print(' ', end=' ')
            print()
        print("Visibility state :", self.visibility_state)





