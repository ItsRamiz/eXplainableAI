import os
import subprocess
import json
from flask import jsonify, request

def process_training_request(form_data):
    data = {
        'environment': form_data.get('EnvName') or 'Unlock',
        'agentName': form_data.get('agentName') or 'default_agent',
        'seed': form_data.get('seed') or 1,
        'processes': form_data.get('processes') or 16,
        'frames': form_data.get('frames') or 1,
        'epochs': form_data.get('epochs') or 4,
        'batchSize': form_data.get('batchSize') or 256,
        'discount': form_data.get('discount') or 0.99,
        'learningRate': form_data.get('learningRate') or 0.001,
        'entropyCoef': form_data.get('entropyCoef') or 0.01,
        'adamEpsilon': form_data.get('adamEpsilon') or 1e-8,
        'rmspropOptimizer': form_data.get('rmspropOptimizer') or 0.99,
        'timeSteps': form_data.get('timeSteps') or 1,
        'maxNorm': form_data.get('maxNorm') or 0.5,
        'customCommand': form_data.get('customCommand') or None
    }

    # Convert to appropriate data types
    data['seed'] = int(data['seed'])
    data['processes'] = int(data['processes'])
    data['frames'] = int(data['frames'])
    data['epochs'] = int(data['epochs'])
    data['batchSize'] = int(data['batchSize'])
    data['discount'] = float(data['discount'])
    data['learningRate'] = float(data['learningRate'])
    data['entropyCoef'] = float(data['entropyCoef'])
    data['adamEpsilon'] = float(data['adamEpsilon'])
    data['rmspropOptimizer'] = float(data['rmspropOptimizer'])
    data['timeSteps'] = int(data['timeSteps'])
    data['maxNorm'] = float(data['maxNorm'])

    command = [
        'python', '-m', 'scripts.train',
        '--algo', 'ppo',
        '--env', data['environment'],
        '--model', data['agentName'],
        '--save-interval', '100',
        '--frames', str(data['frames']),
        '--lr', str(data['learningRate']),
        '--batch-size', str(data['batchSize']),
        '--epochs', str(data['epochs']),
        '--frames-per-proc', '128',
        '--discount', str(data['discount']),
        '--gae-lambda', '0.95',
        '--entropy-coef', str(data['entropyCoef']),
        '--value-loss-coef', '0.5',
        '--max-grad-norm', str(data['maxNorm']),
        '--clip-eps', '0.2',
        '--procs', str(data['processes']),
        '--custom', '1'
    ]

    if data['customCommand']:
        command.extend(data['customCommand'].split())

    print(f"Executing command: {' '.join(command)}")  # Debugging print

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        print(f"Command stdout: {stdout.decode()}")  # Debugging print
        print(f"Command stderr: {stderr.decode()}")  # Debugging print

        if process.returncode == 0:
            return {"status": "success", "message": "Training started successfully."}
        else:
            error_message = stderr.decode().strip()
            return {"status": "error", "message": error_message}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}


def execute_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return 0
        else:
            error_message = stderr.decode()
            print(f"Error: {error_message}")  # Log the error for debugging
            return error_message
    except subprocess.CalledProcessError as e:
        return str(e)


