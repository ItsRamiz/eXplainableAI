import os
import subprocess
from flask import Flask, json, jsonify, render_template, request, redirect, url_for, flash
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
# Define the path to save the environment data file
env_data_path = os.path.join(app.root_path, 'environment.json')

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

@app.route('/CustomEnvPage')
def CustomEnvPage():
    return render_template('CustomEnv.html')


@app.route('/trainCustomEnvPage')
def trainCustomEnvPage():
    return render_template('trainCustomEnv.html')

# Ensure this route is defined only once in your entire application
@app.route('/save-environment', methods=['POST'])
def save_environment():
    data = request.json
    with open(env_data_path, 'w') as file:
        json.dump(data, file)

    return jsonify({"status": "success", "message": "Environment saved!"})

@app.route('/load-environment', methods=['GET'])
def load_environment():
    with open(env_data_path, 'r') as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
