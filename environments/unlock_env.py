import os
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from minigrid.wrappers import FlatObsWrapper
from pathlib import Path
from minigrid.core.world_object import Door
import numpy
import utils
from utils import device
from flask import redirect, url_for
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from videos.video_utils import convert_to_mp4, extend_video

def submit_unlock_env(request):
    if request.method == 'POST':
        try:
            # Sanitize input data
            min_duration = int(request.form['minDuration'].replace(',', ''))
            max_steps = int(request.form['maxSteps'].replace(',', ''))
            min_steps = int(request.form['minSteps'].replace(',', ''))
            is_winner = 1 if 'isWinner' in request.form else 0
            hit_a_wall = 1 if 'hitAWall' in request.form else 0
            door_position = int(request.form['doorPosition'].replace(',', ''))
            key_color = request.form['keyColor']
            steps_until_key = int(request.form['stepsUntilKey'].replace(',', ''))
            agent_type = request.form['agentType']
            if agent_type == 'ppo':
                agent_model_path = Path(r'storage\model.zip')
            elif agent_type == 'rl_starter':
                agent_model_path = Path(r'storage\Unlockenv')

            if not agent_model_path.exists():
                return f"Model file not found: {agent_model_path}"

            # Collect user inputs
            user_inputs = [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color, steps_until_key]

            # Process the videos based on user inputs and agent type
            process_videos_unlock(user_inputs, agent_type, agent_model_path)

            # Redirect to video.html page with list of processed videos
            return redirect(url_for('video'))
        except ValueError as e:
            # Handle invalid input
            return f"Invalid input, please enter numeric values. Error: {e}"
    else:
        return "Request method is not POST"

def process_videos_unlock(user_inputs, agent_type, agent_model_path):
    video_dir = Path("static/videos")
    video_dir.mkdir(parents=True, exist_ok=True)
    for video_file in video_dir.glob("*.mp4"):
        video_file.unlink()

    clips_dir = video_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    if agent_type == 'ppo':
        env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
        env = FlatObsWrapper(env)
        env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

        model = PPO.load(path=str(agent_model_path), env=env)

        frame_rate = 15
        values = [0, 1, 2, 3, 4, 5, 6, 10]
        probabilities = [0.1, 0.1, 0.1, 0, 0.1, 0, 0, 0.6]
        videos_to_extract = []
        number_of_steps = 0

        isPickedKey = False

        for episode_id in range(10):
            first = None
            end = None
            v = [0, 0, 0, 0, 0]
            curr_number_of_steps = 0
            observation, info = env.reset()
            video_saved = False
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

                user_check = query_unlock(user_inputs)

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

                v[4] = 1

                if terminated or truncated:
                    isPickedKey = False
                    if all(v):
                        if (curr_number_of_steps - first) >= (user_inputs[0] * frame_rate):
                            end = curr_number_of_steps
                            videos_to_extract.append((episode_id, first, end))
                            video_saved = True
                    break

            if not video_saved:
                env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: False)

        env.close()

        for video_info in videos_to_extract:
            episode_id, first, end = video_info
            video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"
            start_time = first / frame_rate
            end_time = end / frame_rate + 5
            output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
            if video_path.exists():
                ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
                print(f"Video segment saved as {output_clip_path}")

    elif agent_type == 'rl_starter':
        env = utils.make_env('MiniGrid-Unlock-v0', seed=0, render_mode="rgb_array")  # Ensure render_mode is set
        for _ in range(0):
            env.reset()
        print("Environment loaded\n")

        agent = utils.Agent(env.observation_space, env.action_space, str(agent_model_path),
                            argmax=False, use_memory=False, use_text=False)
        print("Agent loaded\n")

        env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)  # Add RecordVideo wrapper

        frame_rate = 15
        values = [0, 1, 2, 3, 4, 5, 6, 10]
        probabilities = [0.1, 0.1, 0.1, 0, 0.1, 0, 0, 0.6]
        videos_to_extract = []
        number_of_steps = 0

        isPickedKey = False

        for episode_id in range(10):
            first = None
            end = None
            v = [0, 0, 0, 0, 0]
            curr_number_of_steps = 0
            obs, _ = env.reset()
            video_saved = False
            isPickedKey = False
            for step in range(10000):
                number_of_steps += 1
                curr_number_of_steps += 1

                action = agent.get_action(obs)

                obs, reward, terminated, truncated, _ = env.step(action)
                done = terminated or truncated

                if(action == 3 and (get_key_color(env) == "red" or get_key_color(env) == "blue")):
                    isPickedKey = True

                if(isPickedKey == True):
                    values.pop()
                    values.append(action)
                    action = np.random.choice(values, size=1, p=probabilities)

                user_check = query_unlock(user_inputs)

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

                v[4] = 1

                if done:
                    isPickedKey = False
                    if all(v):
                        if (curr_number_of_steps - first) >= (user_inputs[0] * frame_rate):
                            end = curr_number_of_steps
                            videos_to_extract.append((episode_id, first, end))
                            video_saved = True
                    break

            if not video_saved:
                env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: False)

        env.close()

        for video_info in videos_to_extract:
            episode_id, first, end = video_info
            video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"
            start_time = first / frame_rate
            end_time = end / frame_rate + 5
            output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
            if video_path.exists():
                ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
                print(f"Video segment saved as {output_clip_path}")

    for video_file in clips_dir.glob("*.mp4"):
        convert_to_mp4(video_file)

    for video_info in videos_to_extract:
        episode_id = video_info[0]
        output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
        extend_video(output_clip_path, extension_factor=2)

def query_unlock(user_inputs):
    vector = []
    vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
    vector.append(1 if user_inputs[1] > 0 else 0)
    vector.append(1 if user_inputs[2] > 0 else 0)
    vector.append(1 if user_inputs[3] == 1 else 0)
    vector.append(1 if user_inputs[4] == 1 else 0)
    vector.append(1 if user_inputs[5] > 0 and user_inputs[5] <= 5 else 0)
    vector.append(1 if user_inputs[6] in ["red", "green", "blue", "purple", "yellow", "grey"] else 0)
    return vector

def is_door_open(env):
    grid = env.unwrapped.grid.encode()
    width, height, _ = grid.shape
    for i in range(width):
        for j in range(height):
            cell = grid[i, j]
            obj_idx, color_idx, state = cell
            if obj_idx == 4:
                return state == 0
    return False

def get_key_color(env):
    for x in range(env.grid.width):
        for y in range(env.grid.height):
            obj = env.grid.get(x, y)
            if isinstance(obj, Door):
                return obj.color
