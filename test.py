from utils import JumboMana
import gym
from stable_baselines3 import PPO
import time

# test 
env = JumboMana()
model = PPO.load("jumbo_mana_model") # chargement du modèle pré-entrainé
num_episodes = 100
for episode in range(num_episodes):
    obs = env.reset()
    done = False
    total_rewards = 0
    while not done:
        env.render() 
        time.sleep(1) 
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_rewards += reward

    print(f"Episode: {episode + 1}, Rewards: {total_rewards}")

env.close()
