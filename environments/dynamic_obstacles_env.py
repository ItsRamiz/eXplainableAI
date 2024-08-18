import os
import numpy as np
import gymnasium as gym
from pathlib import Path
import utils
from flask import redirect, url_for
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from videos.video_utils import convert_to_mp4, extend_video
from minigrid.core.constants import OBJECT_TO_IDX
from minigrid.core.world_object import Ball

def check_surrounding_balls(env, agent_pos):
    ball_count = 0
    surrounding_positions = [
        (agent_pos[0] + 1, agent_pos[1]),  # right
        (agent_pos[0] - 1, agent_pos[1]),  # left
        (agent_pos[0], agent_pos[1] + 1),  # down
        (agent_pos[0], agent_pos[1] - 1),  # up
    ]

    for pos in surrounding_positions:
        if 0 <= pos[0] < env.width and 0 <= pos[1] < env.height:  # Ensure position is within bounds
            obj = env.grid.get(pos[0], pos[1])
            if isinstance(obj, Ball):
                ball_count += 1

    return ball_count

def submit_DynamicObstaclesEnv(request):
    if request.method == 'POST':
        try:
            # Sanitize input data
            min_duration = int(request.form['minDuration'].replace(',', '')) if request.form['minDuration'] else 0
            max_steps = int(request.form['maxSteps'].replace(',', '')) if request.form['maxSteps'] else 1000000
            min_steps = int(request.form['minSteps'].replace(',', '')) if request.form['minSteps'] else 1
            is_winner = 1 if 'isWinner' in request.form else 0

            agent_model_path1 = Path(r'storage\DynamicObstacle6x6')
            agent_model_path2 = Path(r'storage\DynamicObstacle6x6v2')

            if not agent_model_path1.exists():
                return f"Model file not found: {agent_model_path1}"
            if not agent_model_path2.exists():
                return f"Model file not found: {agent_model_path2}"

            # Collect user inputs
            user_inputs = [min_duration, max_steps, min_steps, is_winner]

            # Process the videos based on user inputs and agent type
            process_videos_DynamicObstacles(user_inputs, agent_model_path1, agent_model_path2)
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

    if numberSteps <= user_inputs[1] and numberSteps >= user_inputs[2] and isWinner == user_inputs[3]:
        return True
    else:
        return False

def process_videos_DynamicObstacles(user_inputs, agent_model_path,agent_model_path_2):
    video_dir = Path("static/videos")
    video_dir.mkdir(parents=True, exist_ok=True)
    for video_file in video_dir.glob("*.mp4"):
        video_file.unlink()

    clips_dir = video_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    env = utils.make_env('MiniGrid-Dynamic-Obstacles-6x6-v0', seed=0, render_mode="rgb_array") 
    for _ in range(0):
        env.reset()
    print("Environment loaded\n")

    agent = utils.Agent(env.observation_space, env.action_space, str(agent_model_path),
                        argmax=False, use_memory=False, use_text=False)
    
    agent_bad = utils.Agent(env.observation_space, env.action_space, str(agent_model_path_2),
                        argmax=False, use_memory=False, use_text=False)

    print("Agent loaded\n")

    env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)  # Add RecordVideo wrapper

    frame_rate = 15
    values = [0, 1, 2, 3, 4, 5, 6]
    probabilities = [1/6, 1/6, 1/6, 1/6, 0/7, 1/6, 1/6]
    videos_to_extract = []
    number_of_steps = 0

    for episode_id in range(10):

        curr_number_of_steps = 0
        obs, _ = env.reset()
        video_saved = False
        isWinner = False
        isHitWall = False
        current_agent = agent

        for step in range(10000):

            curr_number_of_steps += 1

            action = current_agent.get_action(obs)
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            agent_pos = env.agent_pos

            balls_around = check_surrounding_balls(env, agent_pos)
            
            if(balls_around > 1):
                current_agent = agent_bad

            if (reward > 0):
                isWinner = 1

            if terminated or truncated:
                if checkGameState(user_inputs, curr_number_of_steps,isWinner,isHitWall):
                    videos_to_extract.append((episode_id, 0, curr_number_of_steps))
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

def query_DynamicObstacles(user_inputs):
    vector = []
    vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
    vector.append(1 if user_inputs[1] > 0 else 0)
    vector.append(1 if user_inputs[2] > 0 else 0)
    vector.append(1 if user_inputs[3] == 1 else 0)
    return vector