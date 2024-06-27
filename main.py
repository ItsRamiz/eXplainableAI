import os
import sys

import gymnasium as gym
import numpy as np
import torch
from stable_baselines3 import PPO
from minigrid.wrappers import FlatObsWrapper
from minigrid.core.world_object import Door, Goal, Key, Wall
from minigrid.manual_control import ManualControl

from custom_environment_test import createCustomEnv
def get_key_color(self):
    for x in range(self.grid.width):
        for y in range(self.grid.height):
            obj = self.grid.get(x, y)
            if isinstance(obj, Door):
                return obj.color

#np.set_printoptions(threshold=np.inf)

env = FlatObsWrapper(gym.make('MiniGrid-Unlock-v0', render_mode="human"))

model = PPO.load(path='model.zip', env=env)

observation, info = env.reset(seed=42)


values = [0, 1, 2, 10]
probabilities = [0.1, 0.1, 0.1, 0.70]


number_of_steps = 0
number_of_steps_until_key = 0
isWinner = 0
env_zeros = np.zeros((4,5))
for _ in range(10000):

    i, j = env.agent_pos

    number_of_steps += 1


    action, _states = model.predict(observation, deterministic=False)
    if(action ==3):
        print(get_key_color(env))
    #values.pop()
    #values.append(action)
    #action = np.random.choice(values, size=1, p=probabilities)

    #if action == 3:
    #    number_of_steps_until_key = number_of_steps

    observation, reward, terminated, truncated, info = env.step(action)


    if terminated or truncated:

        print("#END OF S1ESSION#")
        print("Stats:")
        print("STEPS = " , number_of_steps)
        print("STEP U. KEY = " , number_of_steps_until_key)
        number_of_steps = 0
        number_of_steps_until_key = 0
        observation, info = env.reset()

env.close()