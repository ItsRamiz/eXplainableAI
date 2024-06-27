import os
import numpy as np
import gymnasium as gym
import torch
from stable_baselines3 import PPO
from minigrid.wrappers import FlatObsWrapper
from pathlib import Path
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from custom_environment_test import createCustomEnv

# Create the video directory and remove old video files


from minigrid.core.world_object import Door, Goal, Key, Wall

video_dir = Path("videos")
video_dir.mkdir(parents=True, exist_ok=True)
for video_file in video_dir.glob("*.mp4"):
    video_file.unlink()

# Create a directory for the extracted clips
clips_dir = video_dir / "clips"
clips_dir.mkdir(parents=True, exist_ok=True)

# Get user inputs
user_inputs = []
user_inputs.append(int(input("Enter min time of video (in seconds): ")))       
user_inputs.append(int(input("Enter max number of steps: ")))
user_inputs.append(int(input("Enter min number of steps: ")))
user_inputs.append(int(input("Enter 1 if you want agent to win this game, 0 otherwise: ")))
user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall, 0 otherwise: "))) # currently this condition isn't relevant 

# Define the query as a vector
def query_func(user_inputs):
    vector = []
    vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
    vector.append(1 if user_inputs[1] > 0 else 0)
    vector.append(1 if user_inputs[2] > 0 else 0)
    vector.append(1 if user_inputs[3] == 1 else 0)
    vector.append(1 if user_inputs[4] == 1 else 0)
    return vector

# Check if the door is open in the environment
def is_door_open(env):
    grid = env.unwrapped.grid.encode()
    width, height, _ = grid.shape
    for i in range(width):
        for j in range(height):
            cell = grid[i, j]
            obj_idx, color_idx, state = cell
            if obj_idx == 4:  # 4 corresponds to door
                return state == 0  # 0=open, 1=closed, 2=locked
    return False

def get_key_color(self):
    for x in range(self.grid.width):
        for y in range(self.grid.height):
            obj = self.grid.get(x, y)
            if isinstance(obj, Door):
                return obj.color

# Initialize the environment with the RecordVideo wrapper
env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
env = FlatObsWrapper(env)
env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# Load the trained model
model = PPO.load(path='model.zip', env=env)

frame_rate = 15     
values = [0, 1, 2, 3, 4, 5, 6, 10]
probabilities = [0.1, 0.1, 0.1, 0, 0.1, 0, 0, 0.6]
videos_to_extract = []
number_of_steps = 0

isPickedKey = False

# Extract 10 different videos
for episode_id in range(10):
    first = None
    end = None
    v = [0, 0, 0, 0, 0]
    curr_number_of_steps = 0
    observation, info = env.reset()
    video_saved = False  # New flag to indicate if video segment was saved
    isPickedKey = False
    for step in range(10000):
        number_of_steps += 1
        curr_number_of_steps += 1

        action, _states = model.predict(observation, deterministic=False)

        if(action == 3 and (get_key_color(env) == "red" or get_key_color(env) == "blue")):
            isPickedKey = True

        if(isPickedKey == True):
            values.pop()
            values.append(action)
            action = np.random.choice(values, size=1, p=probabilities)

        observation, reward, terminated, truncated, info = env.step(action)

        user_check = query_func(user_inputs)

        if user_check[1] == 1:
            if curr_number_of_steps <= user_inputs[1]:
                v[0] = 1
                if first is None:
                    first = curr_number_of_steps
            else:
                v[0] = 0
                first = curr_number_of_steps
                v = [0, 0, 0, 0, 0]

        if user_check[2] == 1:
            if curr_number_of_steps >= user_inputs[2]:
                v[1] = 1
                if first is None:
                    first = curr_number_of_steps
            else:
                v[1] = 0
                first = curr_number_of_steps
                v = [0, 0, 0, 0, 0]

        if user_check[3] == 1:
            if is_door_open(env):
                v[2] = 1
                if first is None:
                    first = curr_number_of_steps
            else:
                v[2] = 0
        else:
            if not is_door_open(env):
                v[2] = 1
                if first is None:
                    first = curr_number_of_steps
            else:
                v[2] = 0

        if user_check[4] == 1:
            if action == 3:
                action = 0
                v[3] = 1
                if first is None:
                    first = curr_number_of_steps
            else:
                v[3] = 0
        else:
            if action != 3:
                v[3] = 1
                if first is None:
                    first = curr_number_of_steps
            else:
                v[3] = 0

        v[4] = 1  # in case of more conditions that we want to add

        if terminated or truncated:
            isPickedKey = False
            if all(v):  # Check if time of video matches user input
                if (curr_number_of_steps - first) >= (user_inputs[0] * frame_rate):
                    end = curr_number_of_steps
                    videos_to_extract.append((episode_id, first, end))
                    video_saved = True
            break  # Stop the episode if we met the conditions

    if not video_saved:
        env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: False)

env.close()

# Process all found videos
for video_info in videos_to_extract:
    episode_id, first, end = video_info
    video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"  # Use specific episode video file
    start_time = first / frame_rate
    end_time = end / frame_rate + 5
    output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
    if video_path.exists():
        ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
        print(f"Video segment saved as {output_clip_path}")

# Convert the recorded videos to MP4 using moviepy
def convert_to_mp4(video_path):
    clip = mp.VideoFileClip(str(video_path))
    clip.write_videofile(str(video_path.with_suffix('.mp4')))
    clip.close()  # Close the file after conversion

# Convert all video files to MP4
for video_file in clips_dir.glob("*.mp4"):
    convert_to_mp4(video_file)

# Duplicate frames to make the video longer
def extend_video(video_path, extension_factor=8):
    clip = mp.VideoFileClip(str(video_path))
    frames = [frame for frame in clip.iter_frames()]
    extended_frames = []
    for frame in frames:
        for _ in range(extension_factor):
            extended_frames.append(frame)
    new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
    new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))
    clip.close()  # Close the file after extending

# Extend the output videos
for video_info in videos_to_extract:
    episode_id = video_info[0]
    output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
    extend_video(output_clip_path, extension_factor=2)
