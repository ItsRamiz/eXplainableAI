import subprocess
import sys

# Get the path of the current Python interpreter
python_interpreter_path = sys.executable

# Print the path for verification
print("Current Python interpreter path:", python_interpreter_path)

# Define the command and arguments
command = [
    python_interpreter_path, '-m', 'scripts.visualize',
    '--env', 'MiniGrid-LavaCrossingS9N1-v0',
    '--model', 'LavaCrossing'
]

# Run the command
subprocess.run(command)