######################################### VERSION 1 #########################################
# ## extract one video

# import os
# import sys
# import numpy as np
# import gymnasium as gym
# import torch
# from stable_baselines3 import PPO
# from minigrid.wrappers import FlatObsWrapper
# from minigrid.manual_control import ManualControl
# from pathlib import Path
# import moviepy.editor as mp
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# from custom_environment_test import createCustomEnv

# # Create the video directory and remove old video files
# video_dir = Path("videos")
# video_dir.mkdir(parents=True, exist_ok=True)
# for video_file in video_dir.glob("*.mp4"):
#     video_file.unlink()

# # Get user inputs
# user_inputs = []
# user_inputs.append(int(input("Enter time of video (in seconds): ")))
# user_inputs.append(int(input("Enter max number of steps: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to win this game: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall: ")))

# print("User inputs:", user_inputs)

# def query_func(user_inputs):
#     vector = []
#     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
#     vector.append(1 if user_inputs[1] > 0 else 0)
#     vector.append(1 if user_inputs[2] == 1 else 0)
#     vector.append(1 if user_inputs[3] == 1 else 0)
#     return vector

# def is_door_open(env):
#     grid = env.unwrapped.grid.encode()
#     width, height, _ = grid.shape
    
#     for i in range(width):
#         for j in range(height):
#             cell = grid[i, j]
#             obj_idx, color_idx, state = cell
#             if obj_idx == 4:  # 4 corresponds to door
#                 print(f"Door found at ({i}, {j}) - state: {state}")
#                 return state == 0  # 0=open, 1=closed, 2=locked
#     return False

# # Initialize the environment with the RecordVideo wrapper
# env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# env = FlatObsWrapper(env)
# env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: episode_id == 0)

# # Load the trained model
# model = PPO.load(path='model.zip', env=env)

# observation, info = env.reset(seed=42)

# values = [0, 1, 2, 10]
# probabilities = [0.1, 0.1, 0.1, 0.70]

# number_of_steps = 0
# number_of_steps_until_key = 0
# isWinner = 0

# first = None
# end = None
# v = [0, 0, 0, 0]  

# # Assuming the frame rate is 15 FPS
# frame_rate = 15

# for step in range(10000):
#     number_of_steps += 1

#     action, _states = model.predict(observation, deterministic=False)

#     values.pop()
#     values.append(action)
#     action = np.random.choice(values, size=1, p=probabilities)

#     observation, reward, terminated, truncated, info = env.step(action)

#     # Check user inputs and adjust behavior accordingly
#     user_check = query_func(user_inputs)

#     # Check conditions and set frames accordingly
#     if user_check[1] == 1:
#         if number_of_steps >= user_inputs[1]:
#             v[0] = 1
#             if first is None:
#                 first = number_of_steps

#     if user_check[2] == 1:
#         # Check if the door is open
#         if is_door_open(env):
#             print(f"Step {step}: Door is open")
#             v[1] = 1
#             if first is None:
#                 first = number_of_steps
#     else:
#         if not is_door_open(env):
#             print(f"Step {step}: Door is not open")
#             v[1] = 1
#             if first is None:
#                 first = number_of_steps

#     if user_check[3] == 1:
#         if action == 3:
#             action = 0
#             v[2] = 1
#             if first is None:
#                 first = number_of_steps
#     else:
#         if action != 3:
#             v[2] = 1
#             if first is None:
#                 first = number_of_steps

#     v[3] = 1
#     if all(v):  # Check if all conditions in v are met
#         end = number_of_steps
#         break

#     if action == 3:
#         number_of_steps_until_key = number_of_steps

#     if terminated or truncated:
#         print("#END OF SESSION#")
#         print("Stats:")
#         print("STEPS =", number_of_steps)
#         print("STEP U. KEY =", number_of_steps_until_key)
#         number_of_steps = 0
#         number_of_steps_until_key = 0
#         observation, info = env.reset()

# env.close()

# # Define the path to the video
# video_path = list(video_dir.glob("*.mp4"))[0]  # Get the first recorded video

# # Cut the video from first to end
# if first is not None and end is not None:
#     print(f"Video segment from frame {first} to frame {end}")
#     start_time = first / frame_rate
#     end_time = end / frame_rate
#     ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname="output_clip.mp4")
#     print("Video segment saved as output_clip.mp4")
# else:
#     print("Conditions not met within the time limit.")

# # Optional: Convert the recorded videos to MP4 using moviepy
# def convert_to_mp4(video_path):
#     clip = mp.VideoFileClip(str(video_path))
#     clip.write_videofile(str(video_path.with_suffix('.mp4')))

# # Convert all video files to MP4
# for video_file in video_dir.glob("*.mp4"):
#     convert_to_mp4(video_file)

# # Duplicate frames to make the video longer
# def extend_video(video_path, extension_factor=2):
#     clip = mp.VideoFileClip(str(video_path))
#     frames = [frame for frame in clip.iter_frames()]
#     extended_frames = []
#     for frame in frames:
#         extended_frames.extend([frame] * extension_factor)  # Duplicate each frame
#     new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
#     new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))

# # Extend the output video
# output_clip_path = Path("output_clip.mp4")
# extend_video(output_clip_path, extension_factor=2)


######################################### VERSION 2 #########################################
# ### too many videos

# import os
# import sys
# import numpy as np
# import gymnasium as gym
# import torch
# from stable_baselines3 import PPO
# from minigrid.wrappers import FlatObsWrapper
# from minigrid.manual_control import ManualControl
# from pathlib import Path
# import moviepy.editor as mp
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# from custom_environment_test import createCustomEnv

# # Create the video directory and remove old video files
# video_dir = Path("videos")
# video_dir.mkdir(parents=True, exist_ok=True)
# for video_file in video_dir.glob("*.mp4"):
#     video_file.unlink()

# # Get user inputs
# user_inputs = []
# user_inputs.append(int(input("Enter time of video (in seconds): ")))
# user_inputs.append(int(input("Enter max number of steps: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to win this game: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall: ")))

# print("User inputs:", user_inputs)

# def query_func(user_inputs):
#     vector = []
#     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
#     vector.append(1 if user_inputs[1] > 0 else 0)
#     vector.append(1 if user_inputs[2] == 1 else 0)
#     vector.append(1 if user_inputs[3] == 1 else 0)
#     return vector

# def is_door_open(env):
#     grid = env.unwrapped.grid.encode()
#     width, height, _ = grid.shape
    
#     for i in range(width):
#         for j in range(height):
#             cell = grid[i, j]
#             obj_idx, color_idx, state = cell
#             if obj_idx == 4:  # 4 corresponds to door
#                 print(f"Door found at ({i}, {j}) - state: {state}")
#                 return state == 0  # 0=open, 1=closed, 2=locked
#     return False

# # Initialize the environment with the RecordVideo wrapper
# env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# env = FlatObsWrapper(env)
# env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# # Load the trained model
# model = PPO.load(path='model.zip', env=env)

# observation, info = env.reset(seed=42)

# values = [0, 1, 2, 10]
# probabilities = [0.1, 0.1, 0.1, 0.70]

# number_of_steps = 0
# number_of_steps_until_key = 0
# total_steps = 0
# isWinner = 0

# first = None
# end = None
# v = [0, 0, 0, 0]  

# # Assuming the frame rate is 15 FPS
# frame_rate = 15

# for step in range(10000):
#     number_of_steps += 1
#     total_steps += 1

#     action, _states = model.predict(observation, deterministic=False)

#     values.pop()
#     values.append(action)
#     action = np.random.choice(values, size=1, p=probabilities)

#     observation, reward, terminated, truncated, info = env.step(action)

#     # Check user inputs and adjust behavior accordingly
#     user_check = query_func(user_inputs)

#     # Check conditions and set frames accordingly
#     if user_check[1] == 1:
#         if number_of_steps >= user_inputs[1]:
#             v[0] = 1
#             if first is None:
#                 first = total_steps
#         else:
#             v[0] = 0
#             first = None
#             number_of_steps = 0

#     if user_check[2] == 1:
#         # User wants the agent to win (door should be open)
#         if is_door_open(env):
#             print(f"Step {step}: Door is open")
#             v[1] = 1
#             if first is None:
#                 first = total_steps
#         else:
#             v[1] = 0
#     else:
#         # User does not want the agent to win (door should be closed)
#         if not is_door_open(env):
#             print(f"Step {step}: Door is not open")
#             v[1] = 1
#             if first is None:
#                 first = total_steps
#         else:
#             v[1] = 0

#     if user_check[3] == 1:
#         # User wants the agent to get stuck on the wall
#         if action == 3:
#             action = 0
#             v[2] = 1
#             if first is None:
#                 first = total_steps
#     else:
#         # User does not want the agent to get stuck on the wall
#         if action != 3:
#             v[2] = 1
#             if first is None:
#                 first = total_steps

#     v[3] = 1
#     if all(v):  # Check if all conditions in v are met
#         end = total_steps
#         break

#     if action == 3:
#         number_of_steps_until_key = total_steps

#     if terminated or truncated:
#         print("#END OF SESSION#")
#         print("Stats:")
#         print("STEPS =", number_of_steps)
#         print("STEP U. KEY =", number_of_steps_until_key)
#         number_of_steps = 0  # Reset number of steps for the new episode
#         first = None
#         observation, info = env.reset()

# env.close()

# # Define the path to the video
# video_path = list(video_dir.glob("*.mp4"))[0]  # Get the first recorded video

# # Cut the video from first to end
# if first is not None and end is not None:
#     print(f"Video segment from frame {first} to frame {end}")
#     start_time = first / frame_rate
#     end_time = end / frame_rate
#     ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname="output_clip.mp4")
#     print("Video segment saved as output_clip.mp4")
# else:
#     print("Conditions not met within the time limit.")

# # Optional: Convert the recorded videos to MP4 using moviepy
# def convert_to_mp4(video_path):
#     clip = mp.VideoFileClip(str(video_path))
#     clip.write_videofile(str(video_path.with_suffix('.mp4')))

# # Convert all video files to MP4
# for video_file in video_dir.glob("*.mp4"):
#     convert_to_mp4(video_file)

# # Duplicate frames to make the video longer
# def extend_video(video_path, extension_factor=8):
#     clip = mp.VideoFileClip(str(video_path))
#     frames = [frame for frame in clip.iter_frames()]
#     extended_frames = []
#     for frame in frames:
#         for _ in range(extension_factor):
#             extended_frames.append(frame)
#     new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
#     new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))

# # Extend the output video
# output_clip_path = Path("output_clip.mp4")
# extend_video(output_clip_path, extension_factor=2)

######################################### VERSION 3 #########################################
# extact rl videos, output, and extended

# import os
# import sys
# import numpy as np
# import gymnasium as gym
# import torch
# from stable_baselines3 import PPO
# from minigrid.wrappers import FlatObsWrapper
# from pathlib import Path
# import moviepy.editor as mp
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# from custom_environment_test import createCustomEnv

# # Create the video directory and remove old video files
# video_dir = Path("videos")
# video_dir.mkdir(parents=True, exist_ok=True)
# for video_file in video_dir.glob("*.mp4"):
#     video_file.unlink()

# # Get user inputs
# user_inputs = []
# user_inputs.append(int(input("Enter time of video (in seconds): ")))
# user_inputs.append(int(input("Enter max number of steps: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to win this game: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall: ")))     

# # print("User inputs:", user_inputs)

# def query_func(user_inputs):
#     vector = []
#     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
#     vector.append(1 if user_inputs[1] > 0 else 0)
#     vector.append(1 if user_inputs[2] == 1 else 0)
#     vector.append(1 if user_inputs[3] == 1 else 0)
#     return vector

# def is_door_open(env):
#     grid = env.unwrapped.grid.encode()
#     width, height, _ = grid.shape
    
#     for i in range(width):
#         for j in range(height):
#             cell = grid[i, j]
#             obj_idx, color_idx, state = cell
#             if obj_idx == 4:  # 4 corresponds to door
#                 # print(f"Door found at ({i}, {j}) - state: {state}")
#                 return state == 0  # 0=open, 1=closed, 2=locked
#     return False

# # Initialize the environment with the RecordVideo wrapper
# env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# env = FlatObsWrapper(env)
# env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# # Load the trained model
# model = PPO.load(path='model.zip', env=env)

# values = [0, 1, 2, 10]
# probabilities = [0.1, 0.1, 0.1, 0.70]

# frame_rate = 10
# videos_to_extract = []

# for episode_id in range(10):  # 10 = num of videos to extract
#     first = None
#     end = None
#     v = [0, 0, 0, 0]
#     number_of_steps = 0
    
#     observation, info = env.reset()
#     for step in range(10000):
#         number_of_steps += 1

#         action, _states = model.predict(observation, deterministic=False)

#         values.pop()
#         values.append(action)
#         action = np.random.choice(values, size=1, p=probabilities)

#         observation, reward, terminated, truncated, info = env.step(action)

#         user_check = query_func(user_inputs)

#         if user_check[1] == 1:
#             if number_of_steps >= user_inputs[1]:
#                 v[0] = 1
#                 if first is None:
#                     first = number_of_steps

#         if user_check[2] == 1:
#             if is_door_open(env):
#                 v[1] = 1
#                 if first is None:
#                     first = number_of_steps
#         else:
#             if not is_door_open(env):
#                 v[1] = 1
#                 if first is None:
#                     first = number_of_steps

#         if user_check[3] == 1:
#             if action == 3:
#                 action = 0
#                 v[2] = 1
#                 if first is None:
#                     first = number_of_steps
#         else:
#             if action != 3:
#                 v[2] = 1
#                 if first is None:
#                     first = number_of_steps

#         v[3] = 1
#         if all(v):
#             end = number_of_steps
#             videos_to_extract.append((episode_id, first, end))
#             break  # Stop the episode if we met the conditions

#         if terminated or truncated:
#             break

# env.close()

# # Process all found videos
# for video_info in videos_to_extract:
#     episode_id, first, end = video_info
#     video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"  # Use specific episode video file
#     start_time = first / frame_rate
#     end_time = end / frame_rate
#     output_clip_path = video_dir / f"output_clip_episode_{episode_id}.mp4"
#     if video_path.exists():
#         ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
#         # print(f"Video segment saved as {output_clip_path}")

# # Optional: Convert the recorded videos to MP4 using moviepy
# def convert_to_mp4(video_path):
#     clip = mp.VideoFileClip(str(video_path))
#     clip.write_videofile(str(video_path.with_suffix('.mp4')))

# # Convert all video files to MP4
# for video_file in video_dir.glob("*.mp4"):
#     convert_to_mp4(video_file)

# # Duplicate frames to make the video longer
# def extend_video(video_path, extension_factor=8):
#     clip = mp.VideoFileClip(str(video_path))
#     frames = [frame for frame in clip.iter_frames()]
#     extended_frames = []
#     for frame in frames:
#         for _ in range(extension_factor):
#             extended_frames.append(frame)
#     new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
#     new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))

# # Extend the output videos
# for video_info in videos_to_extract:
#     episode_id = video_info[0]
#     output_clip_path = video_dir / f"output_clip_episode_{episode_id}.mp4"
#     extend_video(output_clip_path, extension_factor=2)

######################################### VERSION 4 #########################################
# # # ###### without min condition:

# import os
# import numpy as np
# import gymnasium as gym
# import torch
# from stable_baselines3 import PPO
# from minigrid.wrappers import FlatObsWrapper
# from pathlib import Path
# import moviepy.editor as mp
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# from custom_environment_test import createCustomEnv

# # Create the video directory and remove old video files
# video_dir = Path("videos")
# video_dir.mkdir(parents=True, exist_ok=True)
# for video_file in video_dir.glob("*.mp4"):
#     video_file.unlink()

# user_inputs = []
# user_inputs.append(int(input("Enter time of video (in seconds): ")))
# user_inputs.append(int(input("Enter max number of steps: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to win this game: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall: ")))

# def query_func(user_inputs):
#     vector = []
#     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
#     vector.append(1 if user_inputs[1] > 0 else 0)
#     vector.append(1 if user_inputs[2] == 1 else 0)
#     vector.append(1 if user_inputs[3] == 1 else 0)
#     return vector

# def is_door_open(env):
#     grid = env.unwrapped.grid.encode()
#     width, height, _ = grid.shape
#     for i in range(width):
#         for j in range(height):
#             cell = grid[i, j]
#             obj_idx, color_idx, state = cell
#             if obj_idx == 4:  # 4 corresponds to door
#                 return state == 0  # 0=open, 1=closed, 2=locked
#     return False

# # Initialize the environment with the RecordVideo wrapper
# env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# env = FlatObsWrapper(env)
# env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# # Load the trained model
# model = PPO.load(path='model.zip', env=env)

# frame_rate = 10

# # Run a single episode
# observation, info = env.reset()
# episode_id = 0
# first = None
# end = None
# v = [0, 0, 0, 0]
# number_of_steps = 0

# for step in range(10000):
#     number_of_steps += 1
#     action, _states = model.predict(observation, deterministic=False)
#     observation, reward, terminated, truncated, info = env.step(action)

#     user_check = query_func(user_inputs)

#     if user_check[1] == 1 and number_of_steps >= user_inputs[1]:
#         v[0] = 1
#         if first is None:
#             first = number_of_steps

#     if user_check[2] == 1:
#         if is_door_open(env):
#             v[1] = 1
#             if first is None:
#                 first = number_of_steps
#     else:
#         if not is_door_open(env):
#             v[1] = 1
#             if first is None:
#                 first = number_of_steps

#     if user_check[3] == 1 and action == 3:
#         action = 0
#         v[2] = 1
#         if first is None:
#             first = number_of_steps
#     elif action != 3:
#         v[2] = 1
#         if first is None:
#             first = number_of_steps

#     v[3] = 1
#     if all(v):
#         end = number_of_steps
#         break  # Stop the episode if we met the conditions

#     if terminated or truncated:
#         break

# env.close()

# # Extract the video segment according to the first and end parameters
# video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"  # Use the single episode video file
# output_clip_path = None
# if first is not None and end is not None:
#     start_time = first / frame_rate
#     end_time = end / frame_rate
#     output_clip_path = video_dir / f"output_clip_episode_{episode_id}.mp4"
#     if video_path.exists():
#         ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
#         print(f"Video segment saved as {output_clip_path}")
#     else:
#         print(f"Video path {video_path} does not exist.")
# else:
#     print("No valid first and end parameters for extraction.")

# # Optional: Convert the recorded videos to MP4 using moviepy
# def convert_to_mp4(video_path):
#     clip = mp.VideoFileClip(str(video_path))
#     clip.write_videofile(str(video_path.with_suffix('.mp4')))

# # Convert the output video file to MP4
# if output_clip_path and output_clip_path.exists():
#     convert_to_mp4(output_clip_path)
# else:
#     print(f"Output clip path {output_clip_path} does not exist for conversion.")

# # Duplicate frames to make the video longer
# def extend_video(video_path, extension_factor=8):
#     clip = mp.VideoFileClip(str(video_path))
#     frames = [frame for frame in clip.iter_frames()]
#     extended_frames = []
#     for frame in frames:
#         for _ in range(extension_factor):
#             extended_frames.append(frame)
#     new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
#     new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))

# # Extend the output videos
# if output_clip_path and output_clip_path.exists():
#     extend_video(output_clip_path, extension_factor=2)
# else:
#     print(f"Output clip path {output_clip_path} does not exist for extending.")

######################################### VERSION 5 #########################################
# extract 1 video with min

# import os
# import numpy as np
# import gymnasium as gym
# import torch
# from stable_baselines3 import PPO
# from minigrid.wrappers import FlatObsWrapper
# from pathlib import Path
# import moviepy.editor as mp
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# from custom_environment_test import createCustomEnv

# # Create the video directory and remove old video files
# video_dir = Path("videos")
# video_dir.mkdir(parents=True, exist_ok=True)
# for video_file in video_dir.glob("*.mp4"):
#     video_file.unlink()

# user_inputs = []
# user_inputs.append(int(input("Enter time of video (in seconds): ")))
# user_inputs.append(int(input("Enter max number of steps: ")))
# user_inputs.append(int(input("Enter min number of steps: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to win this game: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall: ")))

# def query_func(user_inputs):
#     vector = []
#     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
#     vector.append(1 if user_inputs[1] > 0 else 0)
#     vector.append(1 if user_inputs[2] > 0 else 0)
#     vector.append(1 if user_inputs[3] == 1 else 0)
#     vector.append(1 if user_inputs[4] == 1 else 0)
#     return vector

# def is_door_open(env):
#     grid = env.unwrapped.grid.encode()
#     width, height, _ = grid.shape
#     for i in range(width):
#         for j in range(height):
#             cell = grid[i, j]
#             obj_idx, color_idx, state = cell
#             if obj_idx == 4:  # 4 corresponds to door
#                 return state == 0  # 0=open, 1=closed, 2=locked
#     return False

# # Initialize the environment with the RecordVideo wrapper
# env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# env = FlatObsWrapper(env)
# env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# # Load the trained model
# model = PPO.load(path='model.zip', env=env)

# frame_rate = 10

# # Run a single episode
# observation, info = env.reset()
# episode_id = 0
# first = None
# end = None
# v = [0, 0, 0, 0, 0]
# number_of_steps = 0

# for step in range(10000):
#     number_of_steps += 1
#     action, _states = model.predict(observation, deterministic=False)
#     observation, reward, terminated, truncated, info = env.step(action)

#     user_check = query_func(user_inputs)

#     if user_check[1] == 1 and number_of_steps >= user_inputs[1]:
#         v[0] = 1
#         if first is None:
#             first = number_of_steps

#     if user_check[2] == 1 and number_of_steps <= user_inputs[1]:
#         v[1] = 1
#         if first is None:
#             first = number_of_steps

#     if user_check[3] == 1:
#         if is_door_open(env):
#             v[2] = 1
#             if first is None:
#                 first = number_of_steps
#     else:
#         if not is_door_open(env):
#             v[1] = 1
#             if first is None:
#                 first = number_of_steps

#     if user_check[4] == 1 and action == 3:
#         action = 0
#         v[3] = 1
#         if first is None:
#             first = number_of_steps
#     elif action != 3:
#         v[3] = 1
#         if first is None:
#             first = number_of_steps

#     v[4] = 1
#     if all(v):
#         end = number_of_steps
#         break  # Stop the episode if we met the conditions

#     # if terminated or truncated:
#     #     break

# env.close()

# # Extract the video segment according to the first and end parameters
# video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"  # Use the single episode video file
# output_clip_path = None
# if first is not None and end is not None:
#     start_time = first / frame_rate
#     end_time = end / frame_rate
#     output_clip_path = video_dir / f"output_clip_episode_{episode_id}.mp4"
#     if video_path.exists():
#         ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
#         print(f"Video segment saved as {output_clip_path}")
#     else:
#         print(f"Video path {video_path} does not exist.")
# else:
#     print("No valid first and end parameters for extraction.")

# # Optional: Convert the recorded videos to MP4 using moviepy
# def convert_to_mp4(video_path):
#     clip = mp.VideoFileClip(str(video_path))
#     clip.write_videofile(str(video_path.with_suffix('.mp4')))

# # Convert the output video file to MP4
# if output_clip_path and output_clip_path.exists():
#     convert_to_mp4(output_clip_path)
# else:
#     print(f"Output clip path {output_clip_path} does not exist for conversion.")

# # Duplicate frames to make the video longer
# def extend_video(video_path, extension_factor=8):
#     clip = mp.VideoFileClip(str(video_path))
#     frames = [frame for frame in clip.iter_frames()]
#     extended_frames = []
#     for frame in frames:
#         for _ in range(extension_factor):
#             extended_frames.append(frame)
#     new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
#     new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))

# # Extend the output videos
# if output_clip_path and output_clip_path.exists():
#     extend_video(output_clip_path, extension_factor=2)
# else:
#     print(f"Output clip path {output_clip_path} does not exist for extending.")



# ######################################### VERSION 6 #########################################
# ### recorded video is not as expected.. when agent is done with the game, the recording stops

# import os
# import numpy as np
# import gymnasium as gym
# import torch
# from stable_baselines3 import PPO
# from minigrid.wrappers import FlatObsWrapper
# from pathlib import Path
# import moviepy.editor as mp
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from custom_environment_test import createCustomEnv

# # Create the video directory and remove old video files
# video_dir = Path("videos")
# video_dir.mkdir(parents=True, exist_ok=True)
# for video_file in video_dir.glob("*.mp4"):
#     video_file.unlink()

# # Create a directory for the extracted clips
# clips_dir = video_dir / "clips"
# clips_dir.mkdir(parents=True, exist_ok=True)

# # Get user inputs
# user_inputs = []
# user_inputs.append(int(input("Enter time of video (in seconds): ")))       
# user_inputs.append(int(input("Enter max number of steps: ")))
# user_inputs.append(int(input("Enter min number of steps: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to win this game, 0 otherwise: ")))
# user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall, 0 otherwise: "))) # currently thuis condition is't relevant 

# # Define the query as a vector
# def query_func(user_inputs):
#     vector = []
#     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
#     vector.append(1 if user_inputs[1] > 0 else 0)
#     vector.append(1 if user_inputs[2] > 0 else 0)
#     vector.append(1 if user_inputs[3] == 1 else 0)
#     vector.append(1 if user_inputs[4] == 1 else 0)
#     return vector

# # Check if the door is open in the environment
# def is_door_open(env):
#     grid = env.unwrapped.grid.encode()
#     width, height, _ = grid.shape
#     for i in range(width):
#         for j in range(height):
#             cell = grid[i, j]
#             obj_idx, color_idx, state = cell
#             if obj_idx == 4:  # 4 corresponds to door
#                 return state == 0  # 0=open, 1=closed, 2=locked
#     return False

# # Initialize the environment with the RecordVideo wrapper
# env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# env = FlatObsWrapper(env)
# env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# # Load the trained model
# model = PPO.load(path='model.zip', env=env)

# frame_rate = 15     
# values = [0, 1, 2, 3, 4, 5, 6, 10]
# probabilities = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3]
# videos_to_extract = []
# number_of_steps = 0


# # Extract 10 different videos
# for episode_id in range(10):
#     first = None
#     end = None
#     v = [0, 0, 0, 0, 0]
#     curr_number_of_steps = 0
#     observation, info = env.reset()
#     for step in range(10000):
#         number_of_steps += 1
#         curr_number_of_steps +=1
#         action, _states = model.predict(observation, deterministic=False)

#         values.pop()
#         values.append(action)
#         action = np.random.choice(values, size=1, p=probabilities)

#         observation, reward, terminated, truncated, info = env.step(action)

#         user_check = query_func(user_inputs)

#         if user_check[1] == 1:
#             if curr_number_of_steps <= user_inputs[1]:
#                 v[0] = 1
#                 if first is None:
#                     first = number_of_steps
#             else:
#                 v[0] = 0
#                 curr_number_of_steps = 0
#                 first = None

#         if user_check[2] == 1:
#             if curr_number_of_steps >= user_inputs[2]:
#                 v[1] = 1
#                 if first is None:
#                     first = number_of_steps
#             else:
#                 v[1] = 0
#                 curr_number_of_steps = 0
#                 first = None

#         if user_check[3] == 1:
#             if is_door_open(env):
#                 v[2] = 1
#                 if first is None:
#                     first = number_of_steps
#             else:
#                 v[2] = 0
#         else:
#             if not is_door_open(env):
#                 v[2] = 1
#                 if first is None:
#                     first = number_of_steps
#             else:
#                 v[2] = 0

#         if user_check[4] == 1:
#             if action == 3:
#                 action = 0
#                 v[3] = 1
#                 if first is None:
#                     first = number_of_steps
#             else:
#                 v[3] = 0
#         else:
#             if action != 3:
#                 v[3] = 1
#                 if first is None:
#                     first = number_of_steps
#             else:
#                 v[3] = 0

#         v[4] = 1     # in case of more conditions that we ant to add
#         # if all(v):
#         #     end = number_of_steps
#         #     # Check if time of video matches user input
#         #     if (end - first) != (user_inputs[0] * frame_rate) :  
#         #         break  
#         #     videos_to_extract.append((episode_id, first, end))
#         #     break  # Stop the episode if we met the conditions

#         # if terminated or truncated:    
#         #     break
#         if terminated or truncated:
#             if all(v) and (number_of_steps - first) == (user_inputs[0] * frame_rate):  # Check if time of video matches user input
#                 end = number_of_steps
#                 videos_to_extract.append((episode_id, first, end))
#             break  # Stop the episode if we met the conditions
# env.close()

# # Process all found videos
# for video_info in videos_to_extract:
#     episode_id, first, end = video_info
#     video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"  # Use specific episode video file
#     start_time = first / frame_rate
#     end_time = end / frame_rate
#     output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
#     if video_path.exists():
#         ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
#         print(f"Video segment saved as {output_clip_path}")

# # Convert the recorded videos to MP4 using moviepy
# def convert_to_mp4(video_path):
#     clip = mp.VideoFileClip(str(video_path))
#     clip.write_videofile(str(video_path.with_suffix('.mp4')))
#     clip.close()  # Close the file after conversion

# # Convert all video files to MP4
# for video_file in clips_dir.glob("*.mp4"):
#     convert_to_mp4(video_file)

# # Duplicate frames to make the video longer
# def extend_video(video_path, extension_factor=8):
#     clip = mp.VideoFileClip(str(video_path))
#     frames = [frame for frame in clip.iter_frames()]
#     extended_frames = []
#     for frame in frames:
#         for _ in range(extension_factor):
#             extended_frames.append(frame)
#     new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
#     new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))
#     clip.close()  # Close the file after extending

# # Extend the output videos
# for video_info in videos_to_extract:
#     episode_id = video_info[0]
#     output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
#     extend_video(output_clip_path, extension_factor=2)




######################################### VERSION 7 #########################################
### extract video from the specific video saved

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
# def is_door_open(env):
#     grid = env.unwrapped.grid
#     for i in range(grid.width):
#         for j in range(grid.height):
#             cell = grid.get(i, j)
#             if cell and cell.type == 'door':
#                 return cell.is_open
#     return False

# Initialize the environment with the RecordVideo wrapper
env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
env = FlatObsWrapper(env)
env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# Load the trained model
model = PPO.load(path='model.zip', env=env)

frame_rate = 15     
values = [0, 1, 2, 3, 4, 5, 6, 10]
probabilities = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3]
videos_to_extract = []
number_of_steps = 0

# Extract 10 different videos
for episode_id in range(10):
    first = None
    end = None
    v = [0, 0, 0, 0, 0]
    curr_number_of_steps = 0
    observation, info = env.reset()
    video_saved = False  # New flag to indicate if video segment was saved

    for step in range(10000):
        number_of_steps += 1
        curr_number_of_steps += 1
        action, _states = model.predict(observation, deterministic=False)

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
            if all(v) :  # Check if time of video matches user input
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
