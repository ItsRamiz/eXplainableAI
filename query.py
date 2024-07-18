# # # # # # Define the query as a vector
# # # # # def query_func(user_inputs):
# # # # #     vector = []
# # # # #     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
# # # # #     vector.append(1 if user_inputs[1] > 0 else 0)
# # # # #     vector.append(1 if user_inputs[2] > 0 else 0)
# # # # #     vector.append(1 if user_inputs[3] == 1 else 0)
# # # # #     vector.append(1 if user_inputs[4] == 1 else 0)
# # # # #     vector.append(1 if user_inputs[5] > 0 and user_inputs[5] <= 5 else 0)
# # # # #     vector.append(1 if user_inputs[6] in ["red", "green", "blue", "purple", "yellow", "grey"] else 0)
# # # # #     return vector


# # # # # def main():
# # # # #     user_inputs = []
# # # # #     user_inputs.append(int(input("Enter min time of video (in seconds): ")))
# # # # #     user_inputs.append(int(input("Enter max number of steps: ")))
# # # # #     user_inputs.append(int(input("Enter min number of steps: ")))
# # # # #     user_inputs.append(int(input("Enter 1 if you want agent to win this game, 0 otherwise: ")))
# # # # #     user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall, 0 otherwise: "))) # currently this condition isn't relevant
# # # # #     user_inputs.append(int(input("Enter positsion of the door (choose 1-5):")))
# # # # #     user_inputs.append(str(input("Enter color of the door (red, green, blue, purple, yellow, grey):")))
# # # # #     return query_func(user_inputs)

# # # # # # Get user inputs
# # # # # if __name__ == "__main__":
# # # # #     main()



# # # # from flask import Flask, render_template, request, redirect, url_for

# # # # app = Flask(__name__, template_folder='templates')

# # # # @app.route('/')
# # # # def index():
# # # #     print("hi index")
# # # #     return render_template('UnlockEnv.html')

# # # # @app.route('/submit', methods=['POST'])
# # # # def submit():
# # # #     print("got here!")
# # # #     if request.method == 'POST':
# # # #         # Get form data
# # # #         min_duration = int(request.form['minDuration'])
# # # #         max_steps = int(request.form['maxSteps'])
# # # #         min_steps = int(request.form['minSteps'])
# # # #         is_winner = 1 if 'isWinner' in request.form else 0
# # # #         hit_a_wall = 1 if 'hitAWall' in request.form else 0
# # # #         door_position = int(request.form['doorPosition'])
# # # #         key_color = request.form['keyColor']
# # # #         steps_until_key = int(request.form['stepsUntilKey'])

# # # #         # Process the data (example: print to console)
# # # #         print(f"Min Duration: {min_duration}")
# # # #         print(f"Max Steps: {max_steps}")
# # # #         print(f"Min Steps: {min_steps}")
# # # #         print(f"Is Winner: {is_winner}")
# # # #         print(f"Hit A Wall: {hit_a_wall}")
# # # #         print(f"Door Position: {door_position}")
# # # #         print(f"Key Color: {key_color}")
# # # #         print(f"Steps Until Last Picked Key: {steps_until_key}")

# # # #         vector = []
# # # #         vector.append(1 if min_duration > 0 and min_duration <= 5 else 0)
# # # #         vector.append(1 if max_steps > 0 else 0)
# # # #         vector.append(1 if min_steps > 0 else 0)
# # # #         vector.append(1 if is_winner == 1 else 0)
# # # #         vector.append(1 if hit_a_wall == 1 else 0)
# # # #         vector.append(1 if door_position > 0 and door_position <= 5 else 0)
# # # #         vector.append(1 if key_color in ["red", "green", "blue", "purple", "yellow", "grey"] else 0)
# # # #         return vector
    



# # # #         # Redirect to video.html page
# # # #         return redirect(url_for('video'))


# # # # @app.route('/video.html')
# # # # def video():
# # # #     # Render the video.html template
# # # #     return render_template('video.html')

# # # # if __name__ == '__main__':
# # # #     print("Running the app...")
# # # #     app.run(debug=True)



# # # from flask import Flask, render_template, request, redirect, url_for
# # # import os
# # # import numpy as np
# # # import gymnasium as gym
# # # import torch
# # # from stable_baselines3 import PPO
# # # from minigrid.wrappers import FlatObsWrapper
# # # from pathlib import Path
# # # import moviepy.editor as mp
# # # from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# # # import subprocess
# # # from minigrid.core.world_object import Door  # Import the Door class

# # # app = Flask(__name__, template_folder='templates')

# # # @app.route('/')
# # # def index():
# # #     return render_template('UnlockEnv.html')

# # # @app.route('/submit', methods=['POST'])
# # # def submit():
# # #     if request.method == 'POST':
# # #         try:
# # #             # Sanitize input data
# # #             min_duration = int(request.form['minDuration'].replace(',', ''))
# # #             max_steps = int(request.form['maxSteps'].replace(',', ''))
# # #             min_steps = int(request.form['minSteps'].replace(',', ''))
# # #             is_winner = 1 if 'isWinner' in request.form else 0
# # #             hit_a_wall = 1 if 'hitAWall' in request.form else 0
# # #             door_position = int(request.form['doorPosition'].replace(',', ''))
# # #             key_color = request.form['keyColor']
# # #             steps_until_key = int(request.form['stepsUntilKey'].replace(',', ''))

# # #             # Collect user inputs
# # #             user_inputs = [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color, steps_until_key]

# # #             # Process the videos based on user inputs
# # #             process_videos(user_inputs)

# # #             # Redirect to video.html page
# # #             return redirect(url_for('video'))
# # #         except ValueError as e:
# # #             # Handle invalid input
# # #             return f"Invalid input, please enter numeric values. Error: {e}"
# # #     else:
# # #         return "Request method is not POST"

# # # @app.route('/video.html')
# # # def video():
# # #     return render_template('video.html')

# # # def process_videos(user_inputs):
# # #     video_dir = Path("videos")
# # #     video_dir.mkdir(parents=True, exist_ok=True)
# # #     for video_file in video_dir.glob("*.mp4"):
# # #         video_file.unlink()

# # #     clips_dir = video_dir / "clips"
# # #     clips_dir.mkdir(parents=True, exist_ok=True)

# # #     env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# # #     env = FlatObsWrapper(env)
# # #     env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# # #     model = PPO.load(path='model.zip', env=env)

# # #     frame_rate = 15
# # #     values = [0, 1, 2, 3, 4, 5, 6, 10]
# # #     probabilities = [0.1, 0.1, 0.1, 0, 0.1, 0, 0, 0.6]
# # #     videos_to_extract = []
# # #     number_of_steps = 0

# # #     isPickedKey = False

# # #     for episode_id in range(10):
# # #         first = None
# # #         end = None
# # #         v = [0, 0, 0, 0, 0]
# # #         curr_number_of_steps = 0
# # #         observation, info = env.reset()
# # #         video_saved = False
# # #         isPickedKey = False
# # #         for step in range(10000):
# # #             number_of_steps += 1
# # #             curr_number_of_steps += 1

# # #             action, _states = model.predict(observation, deterministic=False)

# # #             if(action == 3 and (get_key_color(env) == "red" or get_key_color(env) == "blue")):
# # #                 isPickedKey = True

# # #             if(isPickedKey == True):
# # #                 values.pop()
# # #                 values.append(action)
# # #                 action = np.random.choice(values, size=1, p=probabilities)

# # #             observation, reward, terminated, truncated, info = env.step(action)

# # #             user_check = query_func(user_inputs)

# # #             if user_check[1] == 1:
# # #                 if curr_number_of_steps <= user_inputs[1]:
# # #                     v[0] = 1
# # #                     if first is None:
# # #                         first = curr_number_of_steps
# # #                 else:
# # #                     v[0] = 0
# # #                     first = curr_number_of_steps
# # #                     v = [0, 0, 0, 0, 0]

# # #             if user_check[2] == 1:
# # #                 if curr_number_of_steps >= user_inputs[2]:
# # #                     v[1] = 1
# # #                     if first is None:
# # #                         first = curr_number_of_steps
# # #                 else:
# # #                     v[1] = 0
# # #                     first = curr_number_of_steps
# # #                     v = [0, 0, 0, 0, 0]

# # #             if user_check[3] == 1:
# # #                 if is_door_open(env):
# # #                     v[2] = 1
# # #                     if first is None:
# # #                         first = curr_number_of_steps
# # #                 else:
# # #                     v[2] = 0
# # #             else:
# # #                 if not is_door_open(env):
# # #                     v[2] = 1
# # #                     if first is None:
# # #                         first = curr_number_of_steps
# # #                 else:
# # #                     v[2] = 0

# # #             if user_check[4] == 1:
# # #                 if action == 3:
# # #                     action = 0
# # #                     v[3] = 1
# # #                     if first is None:
# # #                         first = curr_number_of_steps
# # #                 else:
# # #                     v[3] = 0
# # #             else:
# # #                 if action != 3:
# # #                     v[3] = 1
# # #                     if first is None:
# # #                         first = curr_number_of_steps
# # #                 else:
# # #                     v[3] = 0

# # #             v[4] = 1

# # #             if terminated or truncated:
# # #                 isPickedKey = False
# # #                 if all(v):
# # #                     if (curr_number_of_steps - first) >= (user_inputs[0] * frame_rate):
# # #                         end = curr_number_of_steps
# # #                         videos_to_extract.append((episode_id, first, end))
# # #                         video_saved = True
# # #                 break

# # #         if not video_saved:
# # #             env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: False)

# # #     env.close()

# # #     for video_info in videos_to_extract:
# # #         episode_id, first, end = video_info
# # #         video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"
# # #         start_time = first / frame_rate
# # #         end_time = end / frame_rate + 5
# # #         output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
# # #         if video_path.exists():
# # #             ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
# # #             print(f"Video segment saved as {output_clip_path}")

# # #     for video_file in clips_dir.glob("*.mp4"):
# # #         convert_to_mp4(video_file)

# # #     for video_info in videos_to_extract:
# # #         episode_id = video_info[0]
# # #         output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
# # #         extend_video(output_clip_path, extension_factor=2)

# # # def query_func(user_inputs):
# # #     vector = []
# # #     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
# # #     vector.append(1 if user_inputs[1] > 0 else 0)
# # #     vector.append(1 if user_inputs[2] > 0 else 0)
# # #     vector.append(1 if user_inputs[3] == 1 else 0)
# # #     vector.append(1 if user_inputs[4] == 1 else 0)
# # #     vector.append(1 if user_inputs[5] > 0 and user_inputs[5] <= 5 else 0)
# # #     vector.append(1 if user_inputs[6] in ["red", "green", "blue", "purple", "yellow", "grey"] else 0)
# # #     return vector

# # # def is_door_open(env):
# # #     grid = env.unwrapped.grid.encode()
# # #     width, height, _ = grid.shape
# # #     for i in range(width):
# # #         for j in range(height):
# # #             cell = grid[i, j]
# # #             obj_idx, color_idx, state = cell
# # #             if obj_idx == 4:
# # #                 return state == 0
# # #     return False


# # # def get_key_color(self):
# # #     for x in range(self.grid.width):
# # #         for y in range(self.grid.height):
# # #             obj = self.grid.get(x, y)
# # #             if isinstance(obj, Door):
# # #                 return obj.color

# # # def convert_to_mp4(video_path):
# # #     clip = mp.VideoFileClip(str(video_path))
# # #     clip.write_videofile(str(video_path.with_suffix('.mp4')))
# # #     clip.close()

# # # def extend_video(video_path, extension_factor=8):
# # #     clip = mp.VideoFileClip(str(video_path))
# # #     frames = [frame for frame in clip.iter_frames()]
# # #     extended_frames = []
# # #     for frame in frames:
# # #         for _ in range(extension_factor):
# # #             extended_frames.append(frame)
# # #     new_clip = mp.ImageSequenceClip(extended_frames, fps=clip.fps)
# # #     new_clip.write_videofile(str(video_path.with_name("extended_" + video_path.name)))
# # #     clip.close()

# # # if __name__ == '__main__':
# # #     app.run(debug=True)


# # from flask import Flask, render_template, request, redirect, url_for
# # import os
# # import numpy as np
# # import gymnasium as gym
# # import torch
# # from stable_baselines3 import PPO
# # from minigrid.wrappers import FlatObsWrapper
# # from pathlib import Path
# # import moviepy.editor as mp
# # from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# # import subprocess
# # from minigrid.core.world_object import Door  # Import the Door class

# # app = Flask(__name__, template_folder='templates')

# # @app.route('/')
# # def index():
# #     return render_template('UnlockEnv.html')

# # @app.route('/submit', methods=['POST'])
# # def submit():
# #     if request.method == 'POST':
# #         try:
# #             # Sanitize input data
# #             min_duration = int(request.form['minDuration'].replace(',', ''))
# #             max_steps = int(request.form['maxSteps'].replace(',', ''))
# #             min_steps = int(request.form['minSteps'].replace(',', ''))
# #             is_winner = 1 if 'isWinner' in request.form else 0
# #             hit_a_wall = 1 if 'hitAWall' in request.form else 0
# #             door_position = int(request.form['doorPosition'].replace(',', ''))
# #             key_color = request.form['keyColor']
# #             steps_until_key = int(request.form['stepsUntilKey'].replace(',', ''))

# #             # Collect user inputs
# #             user_inputs = [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color, steps_until_key]

# #             # Process the videos based on user inputs
# #             process_videos(user_inputs)

# #             # Redirect to video.html page with list of processed videos
# #             return redirect(url_for('video'))
# #         except ValueError as e:
# #             # Handle invalid input
# #             return f"Invalid input, please enter numeric values. Error: {e}"
# #     else:
# #         return "Request method is not POST"

# # @app.route('/video.html')
# # def video():
# #     video_dir = Path("static/videos")
# #     video_files = [str(video.relative_to("static")) for video in video_dir.glob("*.mp4")]
# #     return render_template('video.html', videos=video_files)

# # def process_videos(user_inputs):
# #     video_dir = Path("static/videos")
# #     video_dir.mkdir(parents=True, exist_ok=True)
# #     for video_file in video_dir.glob("*.mp4"):
# #         video_file.unlink()

# #     clips_dir = video_dir / "clips"
# #     clips_dir.mkdir(parents=True, exist_ok=True)

# #     env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
# #     env = FlatObsWrapper(env)
# #     env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

# #     model = PPO.load(path='model.zip', env=env)

# #     frame_rate = 15
# #     values = [0, 1, 2, 3, 4, 5, 6, 10]
# #     probabilities = [0.1, 0.1, 0.1, 0, 0.1, 0, 0, 0.6]
# #     videos_to_extract = []
# #     number_of_steps = 0

# #     isPickedKey = False

# #     for episode_id in range(10):
# #         first = None
# #         end = None
# #         v = [0, 0, 0, 0, 0]
# #         curr_number_of_steps = 0
# #         observation, info = env.reset()
# #         video_saved = False
# #         isPickedKey = False
# #         for step in range(10000):
# #             number_of_steps += 1
# #             curr_number_of_steps += 1

# #             action, _states = model.predict(observation, deterministic=False)

# #             if(action == 3 and (get_key_color(env) == "red" or get_key_color(env) == "blue")):
# #                 isPickedKey = True

# #             if(isPickedKey == True):
# #                 values.pop()
# #                 values.append(action)
# #                 action = np.random.choice(values, size=1, p=probabilities)

# #             observation, reward, terminated, truncated, info = env.step(action)

# #             user_check = query_func(user_inputs)

# #             if user_check[1] == 1:
# #                 if curr_number_of_steps <= user_inputs[1]:
# #                     v[0] = 1
# #                     if first is None:
# #                         first = curr_number_of_steps
# #                 else:
# #                     v[0] = 0
# #                     first = curr_number_of_steps
# #                     v = [0, 0, 0, 0, 0]

# #             if user_check[2] == 1:
# #                 if curr_number_of_steps >= user_inputs[2]:
# #                     v[1] = 1
# #                     if first is None:
# #                         first = curr_number_of_steps
# #                 else:
# #                     v[1] = 0
# #                     first = curr_number_of_steps
# #                     v = [0, 0, 0, 0, 0]

# #             if user_check[3] == 1:
# #                 if is_door_open(env):
# #                     v[2] = 1
# #                     if first is None:
# #                         first = curr_number_of_steps
# #                 else:
# #                     v[2] = 0
# #             else:
# #                 if not is_door_open(env):
# #                     v[2] = 1
# #                     if first is None:
# #                         first = curr_number_of_steps
# #                 else:
# #                     v[2] = 0

# #             if user_check[4] == 1:
# #                 if action == 3:
# #                     action = 0
# #                     v[3] = 1
# #                     if first is None:
# #                         first = curr_number_of_steps
# #                 else:
# #                     v[3] = 0
# #             else:
# #                 if action != 3:
# #                     v[3] = 1
# #                     if first is None:
# #                         first = curr_number_of_steps
# #                 else:
# #                     v[3] = 0

# #             v[4] = 1

# #             if terminated or truncated:
# #                 isPickedKey = False
# #                 if all(v):
# #                     if (curr_number_of_steps - first) >= (user_inputs[0] * frame_rate):
# #                         end = curr_number_of_steps
# #                         videos_to_extract.append((episode_id, first, end))
# #                         video_saved = True
# #                 break

# #         if not video_saved:
# #             env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: False)

# #     env.close()

# #     for video_info in videos_to_extract:
# #         episode_id, first, end = video_info
# #         video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"
# #         start_time = first / frame_rate
# #         end_time = end / frame_rate + 5
# #         output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
# #         if video_path.exists():
# #             ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
# #             print(f"Video segment saved as {output_clip_path}")

# #     for video_file in clips_dir.glob("*.mp4"):
# #         convert_to_mp4(video_file)

# #     for video_info in videos_to_extract:
# #         episode_id = video_info[0]
# #         output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
# #         extend_video(output_clip_path, extension_factor=2)

# # def query_func(user_inputs):
# #     vector = []
# #     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
# #     vector.append(1 if user_inputs[1] > 0 else 0)
# #     vector.append(1 if user_inputs[2] > 0 else 0)
# #     vector.append(1 if user_inputs[3] == 1 else 0)
# #     vector.append(1 if user_inputs[4] == 1 else 0)
# #     vector.append(1 if user_inputs[5] > 0 and user_inputs[5] <= 5 else 0)
# #     vector.append(1 if user_inputs[6] in ["red", "green", "blue", "purple", "yellow", "grey"] else 0)
# #     return vector

# # def is_door_open(env):
# #     grid = env.unwrapped.grid.encode()
# #     width, height, _ = grid.shape
# #     for i in range(width):
# #         for j in range(height):
# #             cell = grid[i, j]
# #             obj_idx, color_idx, state = cell
# #             if obj_idx == 4:
# #                 return state == 0
# #     return False

# # def get_key_color(self):
# #     for x in range(self.grid.width):
# #         for y in range(self.grid.height):
# #             obj = self.grid.get(x, y)
# #             if isinstance(obj, Door):
# #                 return obj.color

# # def convert_to_mp4(video_path):
# #     clip = mp.VideoFileClip(str(video_path))
# #     output_path = video_path.with_suffix(".mp4")
# #     clip.write_videofile(str(output_path), codec="libx264")

# # def extend_video(video_path, extension_factor):
# #     original_clip = mp.VideoFileClip(str(video_path))
# #     extended_clip = original_clip.fx(mp.vfx.time_symmetrize)
# #     output_path = video_path.with_suffix(".extended.mp4")
# #     extended_clip.write_videofile(str(output_path), codec="libx264")

# # if __name__ == "__main__":
# #     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for
# import os
# import numpy as np
# import gymnasium as gym
# import torch
# from stable_baselines3 import PPO
# from minigrid.wrappers import FlatObsWrapper
# from pathlib import Path
# import moviepy.editor as mp
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# import subprocess
# from minigrid.core.world_object import Door  # Import the Door class

# app = Flask(__name__, template_folder='templates')

# @app.route('/')
# def index():
#     return render_template('UI_System.html')

# @app.route('/unlock_env')
# def unlock_env():
#     return render_template('UnlockEnv.html')

# @app.route('/loading')
# def loading():
#     return render_template('loading.html')

# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         try:
#             # Sanitize input data
#             min_duration = int(request.form['minDuration'].replace(',', ''))
#             max_steps = int(request.form['maxSteps'].replace(',', ''))
#             min_steps = int(request.form['minSteps'].replace(',', ''))
#             is_winner = 1 if 'isWinner' in request.form else 0
#             hit_a_wall = 1 if 'hitAWall' in request.form else 0
#             door_position = int(request.form['doorPosition'].replace(',', ''))
#             key_color = request.form['keyColor']
#             steps_until_key = int(request.form['stepsUntilKey'].replace(',', ''))

#             # Collect user inputs
#             user_inputs = [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color, steps_until_key]

#             # Process the videos based on user inputs
#             process_videos(user_inputs)

#             # Redirect to video.html page with list of processed videos
#             return redirect(url_for('video'))
#         except ValueError as e:
#             # Handle invalid input
#             return f"Invalid input, please enter numeric values. Error: {e}"
#     else:
#         return "Request method is not POST"

# @app.route('/video')
# def video():
#     video_dir = Path("static/videos")
#     video_files = [str(video.relative_to("static")) for video in video_dir.glob("*.mp4")]
#     return render_template('video.html', videos=video_files)

# def process_videos(user_inputs):
#     video_dir = Path("static/videos")
#     video_dir.mkdir(parents=True, exist_ok=True)
#     for video_file in video_dir.glob("*.mp4"):
#         video_file.unlink()

#     clips_dir = video_dir / "clips"
#     clips_dir.mkdir(parents=True, exist_ok=True)

#     env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
#     env = FlatObsWrapper(env)
#     env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

#     model = PPO.load(path='model.zip', env=env)

#     frame_rate = 15
#     values = [0, 1, 2, 3, 4, 5, 6, 10]
#     probabilities = [0.1, 0.1, 0.1, 0, 0.1, 0, 0, 0.6]
#     videos_to_extract = []
#     number_of_steps = 0

#     isPickedKey = False

#     for episode_id in range(10):
#         first = None
#         end = None
#         v = [0, 0, 0, 0, 0]
#         curr_number_of_steps = 0
#         observation, info = env.reset()
#         video_saved = False
#         isPickedKey = False
#         for step in range(10000):
#             number_of_steps += 1
#             curr_number_of_steps += 1

#             action, _states = model.predict(observation, deterministic=False)

#             if(action == 3 and (get_key_color(env) == "red" or get_key_color(env) == "blue")):
#                 isPickedKey = True

#             if(isPickedKey == True):
#                 values.pop()
#                 values.append(action)
#                 action = np.random.choice(values, size=1, p=probabilities)

#             observation, reward, terminated, truncated, info = env.step(action)

#             user_check = query_func(user_inputs)

#             if user_check[1] == 1:
#                 if curr_number_of_steps <= user_inputs[1]:
#                     v[0] = 1
#                     if first is None:
#                         first = curr_number_of_steps
#                 else:
#                     v[0] = 0
#                     first = curr_number_of_steps
#                     v = [0, 0, 0, 0, 0]

#             if user_check[2] == 1:
#                 if curr_number_of_steps >= user_inputs[2]:
#                     v[1] = 1
#                     if first is None:
#                         first = curr_number_of_steps
#                 else:
#                     v[1] = 0
#                     first = curr_number_of_steps
#                     v = [0, 0, 0, 0, 0]

#             if user_check[3] == 1:
#                 if is_door_open(env):
#                     v[2] = 1
#                     if first is None:
#                         first = curr_number_of_steps
#                 else:
#                     v[2] = 0
#             else:
#                 if not is_door_open(env):
#                     v[2] = 1
#                     if first is None:
#                         first = curr_number_of_steps
#                 else:
#                     v[2] = 0

#             if user_check[4] == 1:
#                 if action == 3:
#                     action = 0
#                     v[3] = 1
#                     if first is None:
#                         first = curr_number_of_steps
#                 else:
#                     v[3] = 0
#             else:
#                 if action != 3:
#                     v[3] = 1
#                     if first is None:
#                         first = curr_number_of_steps
#                 else:
#                     v[3] = 0

#             v[4] = 1

#             if terminated or truncated:
#                 isPickedKey = False
#                 if all(v):
#                     if (curr_number_of_steps - first) >= (user_inputs[0] * frame_rate):
#                         end = curr_number_of_steps
#                         videos_to_extract.append((episode_id, first, end))
#                         video_saved = True
#                 break

#         if not video_saved:
#             env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: False)

#     env.close()

#     for video_info in videos_to_extract:
#         episode_id, first, end = video_info
#         video_path = video_dir / f"rl-video-episode-{episode_id}.mp4"
#         start_time = first / frame_rate
#         end_time = end / frame_rate + 5
#         output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
#         if video_path.exists():
#             ffmpeg_extract_subclip(str(video_path), start_time, end_time, targetname=str(output_clip_path))
#             print(f"Video segment saved as {output_clip_path}")

#     for video_file in clips_dir.glob("*.mp4"):
#         convert_to_mp4(video_file)

#     for video_info in videos_to_extract:
#         episode_id = video_info[0]
#         output_clip_path = clips_dir / f"output_clip_episode_{episode_id}.mp4"
#         extend_video(output_clip_path, extension_factor=2)

# def query_func(user_inputs):
#     vector = []
#     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
#     vector.append(1 if user_inputs[1] > 0 else 0)
#     vector.append(1 if user_inputs[2] > 0 else 0)
#     vector.append(1 if user_inputs[3] == 1 else 0)
#     vector.append(1 if user_inputs[4] == 1 else 0)
#     vector.append(1 if user_inputs[5] > 0 and user_inputs[5] <= 5 else 0)
#     vector.append(1 if user_inputs[6] in ["red", "green", "blue", "purple", "yellow", "grey"] else 0)
#     return vector

# def is_door_open(env):
#     grid = env.unwrapped.grid.encode()
#     width, height, _ = grid.shape
#     for i in range(width):
#         for j in range(height):
#             cell = grid[i, j]
#             obj_idx, color_idx, state = cell
#             if obj_idx == 4:
#                 return state == 0
#     return False

# def get_key_color(env):
#     for x in range(env.grid.width):
#         for y in range(env.grid.height):
#             obj = env.grid.get(x, y)
#             if isinstance(obj, Door):
#                 return obj.color

# def convert_to_mp4(video_path):
#     clip = mp.VideoFileClip(str(video_path))
#     output_path = video_path.with_suffix(".mp4")
#     clip.write_videofile(str(output_path), codec="libx264")

# def extend_video(video_path, extension_factor):
#     original_clip = mp.VideoFileClip(str(video_path))
#     extended_clip = original_clip.fx(mp.vfx.time_symmetrize)
#     output_path = video_path.with_suffix(".extended.mp4")
#     extended_clip.write_videofile(str(output_path), codec="libx264")

# if __name__ == "__main__":
#     app.run(debug=True)


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

@app.route('/')
def index():
    return render_template('MAIN.html')

@app.route('/ui_system')
def ui_system():
    return render_template('UI_System.html')

@app.route('/unlock_env')
def unlock_env():
    return render_template('UnlockEnv.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/submit', methods=['POST'])
def submit():
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

            # Collect user inputs
            user_inputs = [min_duration, max_steps, min_steps, is_winner, hit_a_wall, door_position, key_color, steps_until_key]

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

    env = gym.make('MiniGrid-Unlock-v0', render_mode="rgb_array")
    env = FlatObsWrapper(env)
    env = gym.wrappers.RecordVideo(env, video_folder=str(video_dir), episode_trigger=lambda episode_id: True)

    model = PPO.load(path='model.zip', env=env)

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
