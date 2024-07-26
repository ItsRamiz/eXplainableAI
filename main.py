from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

from environments.unlock_env import submit_unlock_env
from environments.crossing_lava_env import submit_crossing_env
from training.visualizeModel import visualizeModelFunc, kill_process
from training.trainingParameters import submit_training_agent, training_status_func

app = Flask(__name__, template_folder='templates')

# main page
@app.route('/')
def index():
    return render_template('MAIN.html')

# XAI routes
@app.route('/XAI_system')
def XAI_system():
    return render_template('XAI_System.html')

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

@app.route('/video')
def video():
    video_dir = Path("static/videos")
    video_files = [str(video.relative_to("static")) for video in video_dir.glob("*.mp4")]
    return render_template('video.html', videos=video_files)

# loading route
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

if __name__ == "__main__":
    app.run(debug=True)
