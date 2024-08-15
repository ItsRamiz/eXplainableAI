from minigrid.core.grid import Grid
from minigrid.core.world_object import Wall
from gym_minigrid.envs import UnlockEnv

class CustomUnlockEnv(UnlockEnv):
    def __init__(self, size=7):
        super().__init__(size=size)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a wall at a specific location
        # For example, add a wall at (2, 2)
        self.grid.set(2, 2, Wall())

        # Place the agent in the environment
        self.agent_pos = (1, 1)
        self.agent_dir = 0

        # Place the door and key as in the original environment
        self.grid.set(3, 1, Wall())
        self.grid.set(4, 2, Wall())
        self.put_obj(Wall(), 5, 5)

        # Set mission objective
        self.mission = "open the door"

# Create an instance of the custom environment
env = CustomUnlockEnv()
env.reset()
env.render()