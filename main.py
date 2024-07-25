from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

from environments.unlock_env import submit_unlock_env
from environments.crossing_lava_env import submit_crossing_env

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('MAIN.html')

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

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/video')
def video():
    video_dir = Path("static/videos")
    video_files = [str(video.relative_to("static")) for video in video_dir.glob("*.mp4")]
    return render_template('video.html', videos=video_files)

if __name__ == "__main__":
    app.run(debug=True)
