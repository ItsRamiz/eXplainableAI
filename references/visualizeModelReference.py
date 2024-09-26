# The code begins by importing the necessary modules.


# The first module imported
# is subprocess, which is
# part of the Python Standard Library.


# Subprocess allows for spawning
# new processes, connecting to
# their input/output/error pipes,
# and obtaining their return codes.


# It provides powerful tools to work
# with system processes and is commonly
# used to run external commands within Python code.


# In this specific case, subprocess
# will be used to run external scripts or commands.


# Next, we import certain functions
# from the Flask framework.


# Flask is a lightweight web framework
# in Python that is commonly used to build
# web applications and APIs.


# We specifically import three things
# from Flask: request, jsonify, and Response.


# 1. request: This object is used
# to handle incoming requests from the client
# (i.e., HTTP requests).


# It contains data about the request,
# such as the form data, URL parameters,
# headers, and more.


# 2. jsonify: This function is used
# to convert Python dictionaries
# into JSON format, which is commonly
# used for API responses.


# Flask makes it easy to convert Python
# objects to JSON strings, which are
# sent back to the client in a structured format.


# 3. Response: This is used to return
# a custom HTTP response to the client.


# You can control aspects such as the
# data being sent, the status code,
# and the content type (or mimetype).


# Next, the code defines a global
# variable called visualization_process.


# This is initialized as None,
# and it is used to store the reference
# to the subprocess that will be
# spawned later in the code.


# The purpose of this global variable
# is to keep track of the process that visualizes
# the model, so that it can be controlled
# (started, monitored, or terminated) later.


# Since visualization_process is declared globally,
# it can be accessed and modified by any of the functions
# in this module.


# The first function defined is visualizeModelFunc,
# which takes a request as an input parameter.


# This function is responsible for initiating
# the visualization process based on user input.


# The function interacts with the global
# visualization_process variable and handles
# the spawning of a new subprocess.


# The request parameter is expected to be a Flask
# request object, which contains data
# from an HTTP request made by a client.


# Inside the visualizeModelFunc function,
# the global keyword is used to specify that
# the global visualization_process variable
# will be modified within this function.


# This allows the function to update the global state
# of the visualization process.


# Next, the environment and model values
# are extracted from the request object using
# the request.form.get() method.


# This method retrieves data sent
# through a POST request’s form.


# The environment variable will hold
# the name of the environment chosen
# by the user, while the model variable
# will contain the name of the model
# to be visualized.


# For instance, the environment could be
# a specific scenario within the MiniGrid simulation,
# while the model could refer to a machine learning model
# trained to act in that environment.


# The function prints the extracted environment
# and model values for debugging purposes.


# This print statement can help during
# development or troubleshooting, allowing
# developers to see the values passed by the client.


# The next part of the function determines
# which environment to use based on the
# value of the environment variable.


# If the environment is 'CrossingLava',
# the env_name is set to 'MiniGrid-LavaCrossingS9N1-v0'.


# This is likely a specific scenario
# or challenge within the MiniGrid environment,
# which is commonly used in reinforcement
# learning tasks.


# If the environment is anything else,
# the env_name is set to 'MiniGrid-Unlock-v0',
# which is another common MiniGrid environment scenario.


# This is done using a simple if-else
# conditional, which ensures that the
# correct environment is selected for
# the visualization process.


# Once the environment is determined,
# the command that will be run by the subprocess
# is constructed as a list.


# This command is a Python command
# that will execute a module (scripts.visualize),
# passing in the environment and the model as arguments.


# The command consists of several components:


# 1. 'python': This specifies that the Python interpreter
# should be used to run the script.


# 2. '-m': This flag tells Python to run a module
# as a script. In this case, the module being run
# is 'scripts.visualize'.


# 3. '--env': This is a flag that indicates
# the environment name will follow as the next argument.


# 4. '--model': This is a flag that indicates
# the model name will follow as the next argument.


# The values for the environment and model
# are dynamically inserted into the command
# based on the user's input.


# This command will initiate the visualization
# process in the appropriate environment
# with the chosen model.


# The command to be executed is printed
# to the console for debugging purposes.


# This can help developers ensure that the correct
# command is being constructed and executed.


# Next, a nested function called run_command
# is defined within visualizeModelFunc.


# This function is responsible for actually
# running the command using subprocess
# and handling the output.


# It takes the command (which was defined earlier)
# as an argument.


# Inside the run_command function,
# the global keyword is again used to access
# and modify the global visualization_process variable.


# The subprocess.Popen method is used to spawn
# a new process, running the command provided as an argument.


# subprocess.Popen allows for more advanced
# use of subprocesses compared to subprocess.run,
# as it doesn't wait for the process to finish.


# Instead, it runs asynchronously, allowing
# the main program to continue executing
# while the subprocess runs in the background.


# The stdout (standard output) and stderr
# (standard error) of the process are captured using subprocess.PIPE.


# This allows the output from the command
# to be read and processed by the Python code.


# For instance, if the command produces any output
# (such as logging information or errors),
# this output can be captured and sent to the client.


# The for loop reads the output line
# by line from the process’s stdout.


# iter(visualization_process.stdout.readline, b"")
# continuously reads lines from the subprocess output
# until there is no more data.


# Each line of output is yielded, allowing
# the function to stream the output
# to the client in real-time.


# yield is used here to return the output incrementally,
# rather than waiting for the entire process
# to finish before sending the response.


# This can be particularly useful in long-running processes,
# as it allows the client to receive updates
# while the process is still running.


# After the output has been fully read,
# the stdout is closed using visualization_process.stdout.close().


# The return code of the subprocess is then captured
# using visualization_process.wait(), which blocks
# until the process completes.


# If the return code indicates an error
# (i.e., the process didn't exit cleanly),
# a CalledProcessError is raised.


# This exception is caught in the except block,
# and the error message is printed and yielded to the client.


# If the run_command function successfully completes,
# it returns a Response object, streaming the command's output to the client.


# The mimetype is set to 'text/plain', which indicates
# that the output is plain text, making it easy
# to read on the client-side.


# The next function defined is kill_process,
# which is responsible for terminating
# the running visualization process.


# This function interacts with the global visualization_process
# variable, allowing the main Flask application
# to manage the lifecycle of the visualization process.


# The kill_process function first checks if
# there is an active visualization process
# by checking if visualization_process is not None.


# If a process is running, it is terminated using
# the terminate() method, which sends a signal
# to the process asking it to terminate.


# After terminating the process, visualization_process
# is set to None to indicate that no process
# is currently running.


# If a process was successfully terminated,
# the function returns a JSON response using jsonify.


# This response includes a success flag set to True
# and a message indicating that the visualization process was terminated.


# If no process is running (i.e., visualization_process
# is already None), the function returns a JSON response
# with success set to False and a message indicating
# that no process is currently running.


# This ensures that the client receives appropriate
# feedback depending on whether or not a process was actually running.


# In summary, this code provides two key functionalities
# for visualizing machine learning models:


# 1. visualizeModelFunc allows the user to start
# a visualization process for a specific environment and model.


# It uses subprocess to spawn an external process
# that runs a Python script and streams the output back to the client in real-time.


# 2. kill_process provides a way to terminate
# the running visualization process, ensuring that
# the system is not burdened by long-running or stuck processes.


# Together, these functions form the basis of a web interface
# that allows users to visualize machine learning models
# in different environments and control the execution
# of the underlying processes.
