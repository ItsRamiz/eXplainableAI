# ---------------------------------------------------------------------------------

# MiniGrid Environment Class

#

# This class defines the core logic for a 2D grid-world environment. It is built

# using the OpenAI Gym framework and can be used to simulate various grid-based

# reinforcement learning tasks.

#

# The environment consists of a grid made up of different objects such as walls,

# doors, keys, and agents, with a goal for the agent to reach while avoiding

# obstacles such as lava.

#

# The MiniGridEnv class handles initialization, resets, stepping through the environment,

# and rendering the grid, and agent actions.

#

# ---------------------------------------------------------------------------------

# Class MiniGridEnv:

#

# This is the main environment class for the MiniGrid environment.

#

# It inherits from the OpenAI Gym's gym.Env class and serves as the base environment

# for grid-based reinforcement learning tasks.

#

# The environment is a 2D grid where each cell can contain a different object

# (walls, doors, keys, etc.) and the agent can navigate around by taking actions.

#

# Key attributes include:

#

# - `metadata`: Stores rendering modes and frames per second (FPS) settings.

#

# - `mission_space`: The range of possible mission types for the agent.

#

# - `grid_size`, `width`, `height`: The grid dimensions for the environment.

#

# - `max_steps`: Maximum number of steps before an episode ends.

#

# - `agent_view_size`: Specifies the size of the agent's view window.

#

# - `see_through_walls`: Boolean to indicate whether the agent can see through

#   walls.

#

# - `action_space`: Defines the possible discrete actions an agent can take.

#

# - `observation_space`: The observation space that contains the image of the

#   environment, agent direction, and the mission as text.

#

# - `step_count`: Tracks the number of steps taken during an episode.

#

# - `agent_pos`, `agent_dir`: The agent's current position and direction in the

#   grid.

#

# ---------------------------------------------------------------------------------

# __init__ Method:

#

# The initialization method for the MiniGridEnv class takes various parameters

# such as mission_space, grid_size, width, height, max_steps, and several rendering

# options.

#

# It handles setting up the environment, including initializing the grid, setting

# the agent's starting position, and configuring the observation and action

# spaces.

#

# Notable features:

#

# - `mission_space`: The space of possible missions that the agent has to complete.

#   This is sampled each time an episode starts.

#

# - `grid_size`, `width`, and `height`: Defines the grid dimensions. Either a single

#   grid_size can be provided, or width and height can be given separately.

#

# - `action_space`: Configured using the `Actions` enumeration class, which defines

#   all possible discrete actions (such as moving left, right, forward, etc.)

#

# - `observation_space`: The observation space is a dictionary containing an image of

#   the agent's partial view of the environment and the agent's current direction.

#   This is used to describe the current state of the environment.

#

# ---------------------------------------------------------------------------------

# reset Method:

#

# This method resets the environment to its initial state, ready for a new episode.

#

# It samples a new mission, reinitializes the agent's position, and generates a new

# random grid at the start of each episode.

#

# It also checks for any conflicts between the agent's initial position and the grid

# objects (such as overlapping the agent with an object), ensuring valid positions.

#

# - `self.mission`: A new mission is sampled from the mission space.

#

# - `self._gen_grid`: Generates the new grid for the environment at the start of

#   each episode.

#

# - `obs`: The method returns the first observation after the environment is reset.

#   This observation includes the agent's current view of the environment.

#

# ---------------------------------------------------------------------------------

# hash Method:

#

# This method generates a unique hash for the current state of the environment.

#

# It is useful for cases where we want to uniquely identify the environment's

# state, such as for memorizing past states in certain reinforcement learning

# algorithms.

#

# The hash is computed based on the grid layout, agent's position, and the direction

# it is facing.

#

# It uses SHA-256 hashing algorithm to produce the hash and truncates it to a specified

# length (default is 16).

#

# ---------------------------------------------------------------------------------

# steps_remaining Property:

#

# A convenience property that returns the number of steps remaining before the

# episode is truncated.

#

# It is calculated as the difference between the maximum steps and the current

# step count.

#

# ---------------------------------------------------------------------------------

# __str__ Method:

#

# This method returns a string representation of the grid world environment.

#

# Each cell in the grid is represented by a two-character string, with the first

# character denoting the object type and the second character denoting the color

# of the object.

#

# The agent is represented using a directional arrow (">", "V", "<", "^").

#

# This method is helpful for debugging, logging, or human-readable visualization

# of the grid layout.

#

# ---------------------------------------------------------------------------------

# _gen_grid Abstract Method:

#

# This is an abstract method that must be implemented by subclasses of MiniGridEnv.

#

# The purpose of this method is to generate the layout of the grid, including the

# objects that populate the grid.

#

# The layout generation could vary depending on the specific task being solved.

#

# ---------------------------------------------------------------------------------

# _reward Method:

#

# This method computes the reward to be given to the agent upon successfully

# completing a task.

#

# The reward decreases as the agent takes more steps, ensuring that faster solutions

# are incentivized.

#

# The exact formula for the reward is `1 - 0.9 * (self.step_count / self.max_steps)`,

# which means that as the number of steps approaches `max_steps`, the reward decreases.

#

# ---------------------------------------------------------------------------------

# Helper Methods:

#

# Several utility methods are provided in this class to facilitate random sampling,

# such as `_rand_int`, `_rand_float`, `_rand_bool`, `_rand_elem`, and `_rand_subset`.

#

# These methods are helpful when generating random grid layouts or initializing

# random agent positions.

#

# - `_rand_int`: Samples a random integer within a specified range.

#

# - `_rand_float`: Samples a random floating-point number within a specified range.

#

# - `_rand_bool`: Samples a random boolean value (True or False).

#

# - `_rand_elem`: Samples a random element from a given iterable.

#

# - `_rand_subset`: Samples a random subset of distinct elements from a given

#   iterable.

#

# - `_rand_color`: Samples a random color from a predefined list of colors.

#

# ---------------------------------------------------------------------------------

# place_obj and put_obj Methods:

#

# These methods are used to place objects on the grid at specific or random positions.

#

# - `place_obj`: Places an object at a random empty position in the grid. It can

#   also take optional arguments like `top`, `size`, and `reject_fn` to control

#   where the object is placed and to reject invalid positions.

#

# - `put_obj`: Places an object at a specific position in the grid.

#

# ---------------------------------------------------------------------------------

# place_agent Method:

#

# This method sets the agent's starting position at an empty location in the grid.

#

# It uses the `place_obj` method to find an empty location for the agent.

#

# The agent's direction can also be set randomly if `rand_dir` is set to True.

#

# ---------------------------------------------------------------------------------

# Properties:

#

# Several properties are defined in the MiniGridEnv class to compute the agent's

# direction, the position of the cell in front of the agent, and the right-hand

# direction relative to the agent's facing direction.

#

# - `dir_vec`: Returns the vector for the agent's forward direction.

#

# - `right_vec`: Returns the vector pointing to the agent's right-hand side.

#

# - `front_pos`: Returns the coordinates of the cell directly in front of the agent.

#

# ---------------------------------------------------------------------------------

# get_view_coords, get_view_exts, relative_coords, and in_view Methods:

#

# These methods are related to the agent's partially observable view of the

# environment.

#

# Since the agent can only see a portion of the grid (depending on `agent_view_size`),

# these methods compute how the agent's view maps to the grid.

#

# - `get_view_coords`: Translates absolute grid coordinates to the agent's local

#   view.

#

# - `get_view_exts`: Computes the extents of the agent's field of view.

#

# - `relative_coords`: Converts grid positions to the agent's local coordinate

#   system.

#

# - `in_view`: Checks if a particular position in the grid is visible to the agent.

#

# ---------------------------------------------------------------------------------

# step Method:

#

# The step method is the core logic that handles how the environment responds to

# the agent's actions.

#

# It takes an action as input, updates the agent's position and direction, checks

# for collisions with objects, computes rewards, and determines if the episode has

# terminated.

#

# Actions include:

#

# - Rotating left (action == self.actions.left)

#

# - Rotating right (action == self.actions.right)

#

# - Moving forward (action == self.actions.forward)

#

# - Picking up an object (action == self.actions.pickup)

#

# - Dropping an object (action == self.actions.drop)

#

# - Toggling an object (action == self.actions.toggle)

#

# The step method also increments the step count and checks if the maximum number

# of steps has been reached, in which case the episode is truncated.

#

# ---------------------------------------------------------------------------------

# Rendering:

#

# The environment can be rendered in two modes:

#

# - `human`: Displays the grid and agent in a graphical window using pygame.

#

# - `rgb_array`: Returns an RGB array representation of the grid.

#

# The rendering code uses pygame for visualization.

#

# It shows the grid with objects and highlights the agent's field of view.

#

# It also overlays the mission description on the screen to help users understand

# the agent's objective.

#

# The `get_pov_render` method handles rendering the agent's point of view (POV),

# and the `get_full_render` method renders the entire grid with visibility masking.

#

# ---------------------------------------------------------------------------------

# close Method:

#

# This method closes the rendering window and quits pygame if it has been initialized.

#
print("Read the comments for understanding the code.")