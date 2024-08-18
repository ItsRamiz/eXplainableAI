import os
import numpy as np
import gymnasium as gym
from pathlib import Path
import utils
from flask import redirect, url_for
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from videos.video_utils import convert_to_mp4, extend_video


def submit_crossing_env(request):
    if request.method == 'POST':
        try:
            # Sanitize input data
            min_duration = int(request.form['minDuration'].replace(',', '')) if request.form['minDuration'] else 0
            max_steps = int(request.form['maxSteps'].replace(',', '')) if request.form['maxSteps'] else 1000000
            min_steps = int(request.form['minSteps'].replace(',', '')) if request.form['minSteps'] else 1
            is_winner = 1 if 'isWinner' in request.form else 0
            hit_a_wall = 1 if 'hitLava' in request.form else 0

            agent_model_path = Path(r'storage\LavaCrossing')

            if not agent_model_path.exists():
                return f"Model file not found: {agent_model_path}"

            # Collect user inputs
            user_inputs = [min_duration, max_steps, min_steps, is_winner, hit_a_wall]

            # Process the videos based on user inputs and agent type
            process_videos_lava(user_inputs, agent_model_path)

            # Redirect to video.html page with list of processed videos
            return redirect(url_for('video'))
        except ValueError as e:
            # Handle invalid input
            return f"Invalid input, please enter numeric values. Error: {e}"
    else:
        return "Request method is not POST"


def checkGameState(user_inputs, numberSteps, isWinner, isHitWall):
    # [min_duration, max_steps, min_steps, is_winner, hit_a_wall,]
    #      0           1          2           3         4           
    #   IGNORED                                                     

    if numberSteps <= user_inputs[1] and numberSteps >= user_inputs[2] and isWinner == user_inputs[3] and isHitWall == user_inputs[4]:
        return True
    else:
        return False

def process_videos_lava(user_inputs, agent_model_path):
    video_dir = Path("static/videos")
    video_dir.mkdir(parents=True, exist_ok=True)

    for video_file in video_dir.glob("*.mp4"):
        video_file.unlink()

    for video_file in video_dir.glob("*.meta.json"):
        video_file.unlink()

    env = utils.make_env('MiniGrid-LavaCrossingS9N1-v0', seed=0, render_mode="rgb_array")  # Ensure render_mode is set
    for _ in range(0):
        env.reset()
    print("Environment loaded\n")

    agent = utils.Agent(env.observation_space, env.action_space, str(agent_model_path),
                        argmax=False, use_memory=False, use_text=False)
    print("Agent loaded\n")

    env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)  # Add RecordVideo wrapper
    
    videos_to_extract = []

    for episode_id in range(10):

        curr_number_of_steps = 0
        obs, _ = env.reset()
        video_saved = False
        isWinner = False
        isHitWall = False

        for step in range(10000):
            curr_number_of_steps += 1

            action = agent.get_action(obs)
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            if (reward > 0):
                isWinner = 1

            if terminated or truncated:
                if checkGameState(user_inputs, curr_number_of_steps,isWinner,isHitWall):
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
                print(f"Deleting {video_file_name} and its corresponding .meta.json file")
                video_path.unlink()  # Delete the video file

                # Delete the corresponding .meta.json file
                meta_json_path = video_path.with_suffix(".meta.json")
                if meta_json_path.exists():
                    meta_json_path.unlink()
