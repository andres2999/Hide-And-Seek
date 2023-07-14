import pickle
from utils import JumboMana

# génère les environnements de jeu
env = JumboMana()
grid = env.generate_clusters(env.grid_size, env.num_clusters, env.cluster_size)
for row in grid:
    for cell in row:
        print('■' if cell == 1 else ' ', end=' ')
    print()
with open('grid2.pkl', 'wb') as f:
    pickle.dump(grid, f)
print("Grid saved successfully.")
