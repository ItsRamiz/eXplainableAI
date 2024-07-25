from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
import gymnasium as gym
import torch
from stable_baselines3 import PPO
from minigrid.wrappers import FlatObsWrapper
from pathlib import Path
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess
from minigrid.core.world_object import Door  # Import the Door class

app = Flask(__name__, template_folder='templates')

# This is the main page of the UI
@app.route('/')
def index():
    return render_template('UI_System.html')

# This is the page where the user can input the parameters of the unlock environment
@app.route('/__env')
def unlock_env():
    return render_template('__Env.html')

# This page is opened when user clicks unsupported environment
@app.route('/loading')
def loading():
    return render_template('loading.html')

# This function is called when the user submits the form on the unlock_env page
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Sanitize input data
            # text feild
            input1 = int(request.form['input1'].replace(',', ''))
            input2 = int(request.form['input1'].replace(',', ''))
            # check box
            input3 = 1 if 'input3' in request.form else 0
            # combo box
            input4 = request.form['input4']
    
            # Collect user inputs
            user_inputs = [input1, input2, input3, input4]

            # Process the videos based on user inputs
            process_videos(user_inputs)

            # Redirect to video.html page with list of processed videos
            return redirect(url_for('video'))
        except ValueError as e:
            # Handle invalid input
            return f"Invalid input, please enter numeric values. Error: {e}"
    else:
        return "Request method is not POST"

@app.route('/video')
def video():
    video_dir = Path("static/videos")
    video_files = [str(video.relative_to("static")) for video in video_dir.glob("*.mp4")]
    return render_template('video.html', videos=video_files)

def process_videos(user_inputs):
    video_dir = Path("static/videos")
    video_dir.mkdir(parents=True, exist_ok=True)
    for video_file in video_dir.glob("*.mp4"):
        video_file.unlink()

    clips_dir = video_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    # change the env according to ur request
    env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
    env = FlatObsWrapper(env)
    env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

    # Load your own trained model
    model = PPO.load(path='model.zip', env=env)

    frame_rate = 15
    values = [0, 1, 2, 3, 4, 5, 6, 10]      # the defined actions
    probabilities = [0.1, 0.1, 0.1, 0, 0.1, 0, 0, 0.6]  # give wight for each action
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

            user_check = query_func(user_inputs)

            ## check the user inputs
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

    for video_file in clips_dir.glob("*.mp4"):
        convert_to_mp4(video_file)

    for video_info in videos_to_extract:
        episode_id = video_info[0]
        output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
        extend_video(output_clip_path, extension_factor=2)

def query_func(user_inputs):
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

def convert_to_mp4(video_path):
    clip = mp.VideoFileClip(str(video_path))
    output_path = video_path.with_suffix(".mp4")
    clip.write_videofile(str(output_path), codec="libx264")

def extend_video(video_path, extension_factor):
    original_clip = mp.VideoFileClip(str(video_path))
    extended_clip = original_clip.fx(mp.vfx.time_symmetrize)
    output_path = video_path.with_suffix(".extended.mp4")
    extended_clip.write_videofile(str(output_path), codec="libx264")

if __name__ == "__main__":
    app.run(debug=True)
