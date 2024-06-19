import os
import sys
import numpy as np
import gymnasium as gym
import torch
from stable_baselines3 import PPO
from minigrid.wrappers import FlatObsWrapper
from minigrid.manual_control import ManualControl
from pathlib import Path
import moviepy.editor as mp

from custom_environment_test import createCustomEnv

# Create the video directory
video_dir = Path("videos")
video_dir.mkdir(parents=True, exist_ok=True)

# Initialize the environment with the Monitor wrapper
env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
env = FlatObsWrapper(env)
env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# Load the trained model
model = PPO.load(path='model.zip', env=env)

observation, info = env.reset(seed=42)

values = [0, 1, 2, 10]
probabilities = [0.1, 0.1, 0.1, 0.70]

number_of_steps = 0
number_of_steps_until_key = 0
isWinner = 0

for _ in range(10000):
    number_of_steps += 1

    action, _states = model.predict(observation, deterministic=False)

    values.pop()
    values.append(action)
    action = np.random.choice(values, size=1, p=probabilities)

    if action == 3:
        number_of_steps_until_key = number_of_steps

    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        print("#END OF SESSION#")
        print("Stats:")
        print("STEPS =", number_of_steps)
        print("STEP U. KEY =", number_of_steps_until_key)
        number_of_steps = 0
        number_of_steps_until_key = 0
        observation, info = env.reset()

env.close()

# Optional: Convert the recorded videos to MP4 using moviepy
def convert_to_mp4(video_path):
    clip = mp.VideoFileClip(str(video_path))
    clip.write_videofile(str(video_path.with_suffix('.mp4')))

# Convert all video files to MP4
for video_file in video_dir.glob("*.mp4"):
    convert_to_mp4(video_file)
