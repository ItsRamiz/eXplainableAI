from custom_environment_test import SimpleEnv
from minigrid.manual_control import ManualControl
import gym

import gymnasium as gym


def make_env(env_key, seed=None, render_mode=None):
    env = gym.make(env_key, render_mode=render_mode)
    env.reset(seed=seed)
    return env

def main():
    # Initialize the custom environment
    env = make_env("CartPole-v0", 42, render_mode="human")

    # Use the environment (for example, with manual control)
    manual_control = ManualControl(env, seed=42)
    manual_control.start()


if __name__ == "__main__":
    env_names = list(gym.envs.registry.keys())
    print(env_names)

    main()