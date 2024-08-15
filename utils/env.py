from __future__ import annotations
import gymnasium as gym
from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Wall, Lava
from minigrid.manual_control import ManualControl
from minigrid.minigrid_env import MiniGridEnv

""""" This is original code's function
def make_env(env_key, seed=None, render_mode=None):
    env = gym.make(env_key, render_mode=render_mode)
    env.reset(seed=seed)
    return env
"""""


custom_Start_Pos = (1,1) # Player chooses the starting position
custom_Start_Dir = 0 # Player chooses the starting direction
custom_World_Width = 5 # Player chooses the size of the world (Size x Size)
custom_Walls = [] # Player chooses the walls positions
custom_Lava = [] # Player chooses the lava positions
custom_Doors = [] # Player chooses the doors positions, world can have multiple doors
custom_Keys = [] # Player chooses the keys positions, world can have multiple keys
custom_Goals = [] # Player chooses the goals positions, world can have multiple goals


class SimpleEnv(MiniGridEnv):
    def __init__(
            self,
            size=5,
            agent_start_pos= custom_Start_Pos,
            agent_start_dir=custom_Start_Dir,
            max_steps: int | None = None,
            **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size ** 2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "grand mission"

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Generate vertical separation wall
        for wall in custom_Walls: # Each wall is a position of a wall
            self.grid.set(wall, Wall())

        for lava in custom_Lava:
            self.grid.set(lava, Lava())

        for door in custom_Doors: # List of Doors , Each Door is ( X , Y , COLOR , IsLocked )
            self.grid.set((door[0],door[1]), Door(door[2], is_locked=door[3]))

        for key in custom_Keys: # List of Keys , Each Key is ( X , Y , COLOR )
            self.grid.set((key[0],key[1]), Key(key[2]))

        for goal in custom_Goals: # List of Goals , Each Goal is ( X , Y )
            self.put_obj(Goal(), goal[0], goal[1])

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "grand mission"

def createCustomEnv(isTrain):
    if(isTrain == 1):
        env = SimpleEnv() # FOR TRAINING
    else:
        env = SimpleEnv(render_mode="human") # FOR VISUALIZATION
    print("Loaded Custom Environment")
    return env



def make_env(env_key, seed=None, render_mode=None, customEnv = 0, isTrain = 0):

    if customEnv == 0:
        env = gym.make(env_key, render_mode=render_mode)
        env.reset(seed=seed)
        return env
    else:
        env = createCustomEnv(isTrain)
        env.reset(seed=seed)
        return env

def addWall(x,y):
    custom_Walls.append((x,y))

def addLava(x,y):
    custom_Lava.append((x,y))

def addDoor(x,y,color,isLocked):
    custom_Doors.append((x,y,color,isLocked))

def addKey(x,y,color):
    custom_Keys.append((x,y,color))

def removeWall(x,y):
    for wall in custom_Walls:
        if(wall[0] == x and wall[1] == y):
            custom_Walls.remove(wall)
            break

def removeLava(x,y):
    for lava in custom_Lava:
        if(lava[0] == x and lava[1] == y):
            custom_Lava.remove(lava)
            break

def removeDoor(x,y):
    for door in custom_Doors:
        if(door[0] == x and door[1] == y):
            custom_Doors.remove(door)
            break

def removeKey(x,y):
    for key in custom_Keys:
        if(key[0] == x and key[1] == y):
            custom_Keys.remove(key)
            break


