import os
import subprocess
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from pathlib import Path

from environments.dynamic_obstacles_env import submit_DynamicObstaclesEnv
from environments.unlock_env import submit_unlock_env
from environments.crossing_lava_env import submit_crossing_env
from agents.visualizeModel import visualizeModelFunc, kill_process
from agents.trainingParameters import submit_training_agent, training_status_func
from agents.visulizationPage import getFolders, killDisplayFunc, visualizeModelFunction

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Required for flash messages

visualization_process = None  # Global variable to store the subprocess

# Main page
@app.route('/')
def index():
    return render_template('MAIN.html')

# XAI routes
@app.route('/XAI_system')
def XAI_system():
    return render_template('XAI_System.html')

@app.route('/XAI_system2')
def XAI_system2():
    return render_template('XAI_System_full.html')

@app.route('/unlock_env')
def unlock_env():
    return render_template('UnlockEnv.html')

@app.route('/submit_unlock', methods=['POST'])
def submit_unlock():
    return submit_unlock_env(request)

@app.route('/crossing_lava_env')
def crossing_lava_env():
    return render_template('CrossingEnv.html')

@app.route('/submit_crossinglava', methods=['POST'])
def submit_crossinglava():
    return submit_crossing_env(request)

@app.route('/dynamicObstacles_env')
def dynamicObstacles_env():
    return render_template('DynamicObstacles.html')

@app.route('/submit_DynamicObstacles', methods=['POST'])
def submit_DynamicObstacles():
    return submit_DynamicObstaclesEnv(request)

@app.route('/video')
def video():
    video_dir = Path("static/videos")
    video_files = [str(video.relative_to("static")) for video in video_dir.glob("*.mp4")]
    return render_template('video.html', videos=video_files)

@app.route('/get_videos', methods=['GET'])
def get_videos():
    video_path = 'static/videos'
    files = [name for name in os.listdir(video_path) if os.path.isfile(os.path.join(video_path, name)) and name.endswith('.mp4')]
    return jsonify(files)

# Loading route
@app.route('/loading')
def loading():
    return render_template('loading.html')

# Training routes
@app.route('/training')
def training():
    return render_template('modelTraining.html')

@app.route('/submit_training', methods=['POST'])
def submit_training():
    return submit_training_agent(request)

@app.route('/training_process')
def training_process():
    return render_template('trainingProcess.html')

@app.route('/training_status')
def training_status():
    return training_status_func()

@app.route('/visualize', methods=['POST'])
def visualize():
    return visualizeModelFunc(request)

@app.route('/kill_display', methods=['POST'])
def kill_display():
    return kill_process()

@app.route('/visualizePage')
def visualizePage():
    return render_template('visulize.html')

@app.route('/visualizeFunc', methods=['POST'])
def visualizeFunc():
    return visualizeModelFunction(request)

@app.route('/kill_display_func', methods=['POST'])
def kill_display_func():
    return killDisplayFunc()

@app.route('/get_folders', methods=['GET'])
def get_folders():
    return getFolders()

if __name__ == "__main__":
    app.run(debug=True)
