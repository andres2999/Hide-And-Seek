from utils import JumboMana
import gym
from stable_baselines3 import PPO
import os

# entrainement du modèle
env = JumboMana()
model = PPO('MlpPolicy', env, verbose=1) # utilisation du modèle PPO de stable baselines3
model.learn(total_timesteps=int(1e5))
model.save('jumbo_mana_model') # sauvegarde du modèle
env.close()
