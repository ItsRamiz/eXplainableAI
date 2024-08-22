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
from moviepy.editor import VideoFileClip, vfx

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


def submit_unlock_env(request):
    if request.method == 'POST':
        try:
            # Sanitize input data with default value -999 for empty fields
            min_duration = int(request.form['minDuration'].replace(',', '')) if request.form['minDuration'] else 0
            max_steps = int(request.form['maxSteps'].replace(',', '')) if request.form['maxSteps'] else 1000000
            min_steps = int(request.form['minSteps'].replace(',', '')) if request.form['minSteps'] else 0
            door_position = int(request.form['doorPosition'].replace(',', '')) if request.form['doorPosition'] else -999
            max_steps_until_key = int(request.form['stepsUntilKey'].replace(',', '')) if request.form[
                'stepsUntilKey'] else 1000000

            # Check for checkbox and select fields
            is_winner = 1 if 'isWinner' in request.form else 0
            hit_a_wall = 1 if 'hitAWall' in request.form else 0
            key_color = request.form['keyColor'] if 'keyColor' in request.form and request.form[
                'keyColor'] else 'unknown'

            agent_model_path = Path(r'storage\Unlockenv')

            if not agent_model_path.exists():
                return f"Model file not found: {agent_model_path}"

            # Collect user inputs
            user_inputs = [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color,
                           max_steps_until_key]

            # Process the videos based on user inputs and agent type
            process_videos_unlock(user_inputs, agent_model_path)

            # Redirect to video.html page with list of processed videos
            return redirect(url_for('video'))
        except ValueError as e:
            # Handle invalid input
            return f"Invalid input, please enter numeric values. Error: {e}"
    else:
        return "Request method is not POST"

def checkGameState(user_inputs,numberSteps, isWinner, isHitWall, KeyColor, MaxStepUntilKey):
    # [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color, max_steps_until_key]
    #      0           1          2           3         4             5          6          7
    #                                                        IGNORED

    if numberSteps <= user_inputs[1] and isWinner == user_inputs[3] and isHitWall == user_inputs[4] and (KeyColor == user_inputs[6] or user_inputs[6] == 'unknown') and MaxStepUntilKey <= user_inputs[7]:
        return True
    else:
        return False


def process_videos_unlock(user_inputs,
                          agent_model_path):  # [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color, max_steps_until_key]
    # USER INPUT MAPPING LEGEND
    video_dir = Path("static/videos")
    video_dir.mkdir(parents=True, exist_ok=True)
    for video_file in video_dir.glob("*.mp4"):
        video_file.unlink()

    for video_file in video_dir.glob("*.meta.json"):
        video_file.unlink()


    env = utils.make_env('MiniGrid-Unlock-v0', seed=0, render_mode="rgb_array")  # Ensure render_mode is set
    for _ in range(0):
        env.reset()

    agent = utils.Agent(env.observation_space, env.action_space, str(agent_model_path),
                        argmax=False, use_memory=False, use_text=False)

    env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir),
                                    episode_trigger=lambda episode_id: True)  # Add RecordVideo wrapper

    obs, _ = env.reset()
    values = [0, 1, 2, 3, 4, 5, 6, 10]
    probabilities = [0.1, 0.1, 0.1, 0, 0.2, 0, 0, 0.5]
    videos_to_extract = []

    isPickedKey = False

    for episode_id in range(10):

        curr_number_of_steps = 0
        obs , info = env.reset()
        video_saved = False
        isPickedKey = False
        isWinner = False
        isHitWall = False
        KeyColor = get_key_color(env)
        StepUntilKey = 0

        for step in range(10000):

            curr_number_of_steps += 1

            action = agent.get_action(obs)

            obs, reward, terminated, truncated, _ = env.step(action)

            if (action == 3 and (get_key_color(env) == "red" or get_key_color(env) == "blue")):
                isPickedKey = True

            if (isPickedKey == True):
                values.pop()
                values.append(action)
                action = np.random.choice(values, size=1, p=probabilities)

            if (action == 3):
                StepUntilKey = curr_number_of_steps
                isPickedKey = True

            if (reward > 0):
                isWinner = 1

            if terminated or truncated:
                if checkGameState(user_inputs,curr_number_of_steps, isWinner, isHitWall, KeyColor, StepUntilKey):
                    videos_to_extract.append(episode_id)
                break
            
    env.close()

    #######################
    #### Saving Videos ####
    #######################
    video_files_to_keep = {f"rl-video-episode-{video_info}.mp4" for video_info in videos_to_extract}

    # List all .mp4 files in the directory
    directory_videos = list(video_dir.glob("*.mp4"))

    # Loop through the videos in the directory
    for video_path in directory_videos:
        # Extract the file name from the path
        video_file_name = video_path.name
        
        # If the video is not in the list of videos to keep, delete it
        if video_file_name not in video_files_to_keep:
            video_path.unlink()  # Delete the video file

            # Delete the corresponding .meta.json file
            meta_json_path = video_path.with_suffix(".meta.json")
            if meta_json_path.exists():
                meta_json_path.unlink()
        else:
             with VideoFileClip(str(video_path)) as video_clip:
                if video_clip.duration < user_inputs[0]:
                    video_clip.close()
                    video_path.unlink() 
                    meta_json_path = video_path.with_suffix(".meta.json")
                    if meta_json_path.exists():
                        meta_json_path.unlink()


