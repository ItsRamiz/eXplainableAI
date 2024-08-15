from minigrid.manual_control import ManualControl
import gym
from minigrid.core import world_object
import gymnasium as gym


def make_env(env_key, seed=None, render_mode=None):
    env = gym.make(env_key, render_mode=render_mode)
    env.reset(seed=seed)
    return env

def main():
    # Initialize the custom environment
    env = make_env("MiniGrid-Unlock-v0", render_mode="human")

    # Use the environment (for example, with manual control)
    manual_control = ManualControl(env)
    manual_control.start()


if __name__ == "__main__":
    #env_names = list(gym.envs.registry.keys())
    #print(env_names)
    available_objects = dir(world_object)
    print(available_objects)
    main()