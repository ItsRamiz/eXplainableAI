# Project Overview

This project is a collaborative effort between The Technion and University of Haifa, aimed at developing a unique interactive tool for predicting and analyzing agent behavior in both virtual and real-world environments. The tool is designed to assist researchers and users by providing video outputs that match specific behavioral scenarios described through textual queries. By simulating temporal behaviors or events, the tool enhances research capabilities in fields such as reinforcement learning, artificial intelligence, and agent behavior prediction.

## Feature 1: Customizable Agent Training with Reinforcement Learning

The tool provides users the ability to train reinforcement learning agents using either predefined or fully customizable parameters, allowing for fine-tuned control over the training process. Users can adjust the following parameters:

- **Seed**: Initialize the training with a specific seed for reproducibility.
- **Number of Processes**: Specify the number of parallel processes for faster training.
- **Number of Frames**: Set the total number of frames used during training.
- **Epochs**: Define how many full passes the model makes over the training data.
- **Batch Size**: Control the number of samples processed before updating the model.
- **Discount Factor**: Set the discount rate for future rewards (γ).
- **Learning Rate**: Specify the step size for gradient updates.
- **Entropy Coefficient**: Adjust the exploration-exploitation tradeoff.
- **Adam Optimizer Epsilon**: Set the epsilon parameter for stability in the Adam optimizer.
- **RMSprop Optimizer Alpha**: Control the smoothing factor for the RMSprop optimizer.
- **Number of Backsteps to Propagate**: Set how many steps back in time the algorithm looks when updating the agent's actions.
- **Max Norm of Gradient**: Prevent gradient explosion by setting a maximum allowable norm for gradients.

This flexibility allows researchers to simulate and analyze a wide range of agent behaviors, adapting to various scenarios and environments efficiently.

## Feature 2: Graphical Visualization of Agent Behavior

In addition to customizable training, the project offers a graphical interface that provides detailed visualizations of the agent's behavior across different environments. This feature enables users to observe and analyze how agents respond to various stimuli, environments, and tasks in real-time or post-training.

The visualizations allow researchers to:

- **Track Agent Movements**: Observe agent paths and decision-making processes over time.
- **Monitor Interactions**: Visualize how agents interact with objects, obstacles, and other agents in the environment.
- **Behavioral Insights**: Gain insights into key moments, such as when agents learn optimal strategies, fail, or adapt their behavior in response to changes.
- **Real-time and Post-training Visualization**: Users can either view the behavior of agents as it unfolds in real-time or analyze recorded behaviors after training has concluded.

This graphical visualization tool is crucial for better understanding agent behaviors in complex scenarios and helps bridge the gap between theoretical training data and real-world applications.
