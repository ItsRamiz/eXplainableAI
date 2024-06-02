import os
import gymnasium as gym
import torch
from stable_baselines3 import PPO
from minigrid.wrappers import FlatObsWrapper

# Create the environment and apply the FlatObsWrapper
env = FlatObsWrapper(gym.make('MiniGrid-Unlock-v0', render_mode="human"))

# Load the pre-trained PPO model
model = PPO.load(path='model.zip', env=env)

# Reset the environment to get the initial observation
observation, info = env.reset(seed=42)

# Run the environment for a set number of steps
for _ in range(100000):
    # Predict the action using the model
    action, _states = model.predict(observation, deterministic=False)

    # Step the environment with the predicted action
    observation, reward, terminated, truncated, info = env.step(action)

    # Reset the environment if it reaches a terminal state
    if terminated or truncated:
        observation, info = env.reset()

# Close the environment
env.close()