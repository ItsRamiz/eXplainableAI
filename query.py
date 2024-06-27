# Define the query as a vector
def query_func(user_inputs):
    vector = []
    vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
    vector.append(1 if user_inputs[1] > 0 else 0)
    vector.append(1 if user_inputs[2] > 0 else 0)
    vector.append(1 if user_inputs[3] == 1 else 0)
    vector.append(1 if user_inputs[4] == 1 else 0)
    return vector


def main():
    user_inputs = []
    user_inputs.append(int(input("Enter min time of video (in seconds): ")))
    user_inputs.append(int(input("Enter max number of steps: ")))
    user_inputs.append(int(input("Enter min number of steps: ")))
    user_inputs.append(int(input("Enter 1 if you want agent to win this game, 0 otherwise: ")))
    user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall, 0 otherwise: "))) # currently this condition isn't relevant
    return query_func(user_inputs)

# Get user inputs
if __name__ == "__main__":
    main()