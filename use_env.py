from custom_environment_test import SimpleEnv
from minigrid.manual_control import ManualControl


def main():
    # Initialize the custom environment
    env = SimpleEnv(render_mode="human")

    # Use the environment (for example, with manual control)
    manual_control = ManualControl(env, seed=42)
    manual_control.start()


if __name__ == "__main__":
    main()