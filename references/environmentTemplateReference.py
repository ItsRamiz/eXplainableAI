# Define the is_door_open function
# to check if any door in the
# environment is open.


# This function takes an environment
# object as input.

# It retrieves the encoded version
# of the grid using env.unwrapped.grid.encode().

# The grid's width and height are stored
# in width and height variables.

# A nested loop is used to iterate
# over the grid's cells.

# Each cell is examined to check
# if it contains a door (object index 4).

# If a door is found, its state is checked
# (state == 0 indicates the door is open).

# The function returns True if
# an open door is found.

# If no doors are open, it returns
# False.


# Define the get_key_color function
# to retrieve the color of a key
# associated with any door in the environment.


# The function loops through the
# grid dimensions to check for
# Door objects.

# If a door is found, the color
# of the door is returned.


# Define the submit_unlock_env function,
# which handles form submissions from
# a web interface.


# This function processes a POST request
# to gather input data for unlocking
# the environment.

# The method checks whether the request
# is POST. If not, it returns a message
# indicating that the request method
# is not POST.

# Input data is sanitized and default
# values are set for missing or empty
# fields.

# Several form fields are processed,
# including minDuration, maxSteps,
# minSteps, doorPosition, and stepsUntilKey.

# Boolean values like isWinner and hitAWall
# are checked based on whether the corresponding
# checkboxes were ticked.

# The selected agent is extracted from
# the form and checked for existence
# in the file system.

# If the agent's model file is not
# found, an error message is returned.

# All the user inputs are stored in
# a list for further processing.

# The process_videos_unlock function is
# called to process videos according to
# user inputs and the agent's model path.

# If input data is invalid
# (e.g., non-numeric values), a ValueError
# is caught and an error message is returned.

# If the function executes successfully,
# it redirects to a video.html page where
# processed videos are displayed.


# Define the checkGameState function,
# which checks if the current game
# state matches the user's conditions.


# The function compares several
# game state variables, such as
# numberSteps, isWinner, isHitWall,
# KeyColor, and MaxStepUntilKey,
# with the user inputs.

# If all conditions are met
# (e.g., number of steps within the
# allowed range, correct key color),
# it returns True.

# Otherwise, it returns False.


# Define the process_videos_unlock
# function to process videos
# according to user inputs and
# the selected agent model path.


# The function begins by creating a
# directory called "static/videos"
# for saving processed videos.

# Any existing videos in the directory
# are deleted to ensure only the latest
# videos are stored.

# The environment is created using
# MiniGrid-Unlock-v0 with seed set to
# 0 for reproducibility.

# An agent is created using utils.Agent,
# passing in the observation space,
# action space, and agent model path.

# The environment is wrapped with RecordVideo
# to record videos of the agent's performance.

# The function runs through several episodes,
# resetting the environment at the start
# of each episode.

# The agent performs actions in each episode,
# interacting with the environment
# through its policy.

# During each episode, important events
# are tracked, such as picking up a key
# or winning the episode.

# If the episode ends (either through
# termination or truncation), the game state
# is checked using the checkGameState function.

# If the game state matches the user's conditions,
# the episode is marked for video extraction.

# After processing the episodes,
# the environment is closed.

# Videos are then saved based on
# the episodes that met the user's conditions.


# The function begins by identifying
# which videos should be kept
# based on the processed episodes.

# It then loops through the directory
# of saved videos and deletes any videos
# that do not match the conditions.

# Video durations are checked to ensure
# they meet the user's minimum
# duration requirement.

# If a video is too short, it is deleted
# along with its corresponding
# metadata file.

# This ensures that only relevant
# and valid videos remain
# in the directory.


# The code follows standard reinforcement
# learning practices by using
# the MiniGrid-Unlock-v0 environment,
# agent-based action selection, and
# video recording for performance evaluation.


# The combination of Flask for handling
# web requests and MoviePy for processing
# videos enables an interactive interface
# where users can specify conditions
# for processing videos.


# The utility functions like is_door_open
# and get_key_color simplify the extraction
# of specific information from the environment.


# The checkGameState function plays a
# crucial role in determining whether
# the current game state matches
# user expectations.


# The process_videos_unlock function
# is highly modular, taking in
# user inputs and the agent model
# path to process videos according to
# predefined rules.


# Overall, the script leverages multiple
# Python libraries to provide a complete
# solution for training agents,
# processing video recordings,
# and interacting with users through a
# web interface.


# The use of video processing libraries
# ensures that users can easily
# access, convert, and extend videos
# as needed, making the tool flexible
# and user-friendly.


# Video processing is done by first
# capturing the agent's performance
# during episodes, storing the videos,
# and then filtering out irrelevant
# or invalid videos based on
# user-defined criteria.


# Agent performance is evaluated based
# on various conditions, such as
# whether the agent successfully
# completes the episode, picks up keys,
# or avoids obstacles.


# If the agent meets the conditions,
# its performance is captured
# in a video and saved for further
# analysis.


# The codebase is designed for users
# who want to experiment with reinforcement
# learning, agent behaviors,
# and video-based evaluations.


# Through the use of Flask, the script
# allows for dynamic input from users,
# making it easy to set specific conditions
# for video extraction and evaluation.


# The use of RecordVideo from the Gym library
# ensures that the agent's behavior can be
# visually captured, which is useful for
# analyzing the training process and results.


# Key functionality like ffmpeg_extract_subclip
# and convert_to_mp4 make it easy to
# manipulate and transform videos, ensuring
# that the final output meets user requirements.


# By combining reinforcement learning with
# video processing and web-based interfaces,
# this script creates a comprehensive tool
# for evaluating and refining agent behavior
# in interactive environments.


# The PPO algorithm from stable_baselines3
# is used as the primary learning method
# for training agents in this script.


# PPO is a popular choice for reinforcement
# learning tasks as it balances performance
# with stability and can be easily applied
# to a wide range of environments,
# including MiniGrid.


# The use of numpy and other standard
# Python libraries ensures that the script
# is efficient and can handle large datasets,
# which is important for reinforcement learning
# and video processing tasks.


# The Path object from pathlib is used
# to handle filesystem paths in an object-oriented
# way, making the script compatible
# with various operating systems.


# The Door object from the MiniGrid library
# represents a key object in this script,
# as the agent's ability to interact
# with doors and keys is crucial
# for completing the environment's tasks.


# The utility functions in utils are
# likely essential for managing environment
# creation, agent behavior, and other
# helper tasks that simplify the code.


# The Flask framework provides an easy-to-use
# platform for web development, enabling users
# to interact with the script through a web
# interface, submit forms, and view results.


# The use of device from utils suggests
# that the script is designed to work
# efficiently across different devices,
# including CPUs and GPUs, optimizing performance
# for training and video processing.


# ffmpeg_extract_subclip is a powerful tool
# for extracting portions of video clips,
# making it easy to trim and manage video content
# based on user inputs.


# convert_to_mp4 ensures that the final
# video output is in a widely accepted format,
# making it compatible with most media
# players and web browsers.


# extend_video can be used to modify video
# durations, adding flexibility to how
# videos are processed and displayed.


# The final videos are likely stored
# in the static/videos directory,
# a typical location for static files
# in a Flask application.


# Overall, this script provides a complete
# framework for reinforcement learning,
# video processing, and web-based interaction,
# combining several powerful Python libraries
# to deliver a flexible and efficient tool.


# The modular design allows for easy
# customization and expansion, enabling users
# to add new features, environments, or agents
# as needed.


# Flask's routing and request handling
# make it simple to integrate new web-based
# functionalities, allowing users to interact
# with the script in a user-friendly way.


# The use of MoviePy for video processing
# ensures high-quality output and flexible
# video manipulation, making it suitable
# for a wide range of applications.


# The code's reliance on standard Python libraries
# and frameworks makes it accessible to
# a broad audience, from beginner to advanced
# users interested in reinforcement learning
# and video processing.
