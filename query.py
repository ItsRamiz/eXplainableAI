# # # Define the query as a vector
# # def query_func(user_inputs):
# #     vector = []
# #     vector.append(1 if user_inputs[0] > 0 and user_inputs[0] <= 5 else 0)
# #     vector.append(1 if user_inputs[1] > 0 else 0)
# #     vector.append(1 if user_inputs[2] > 0 else 0)
# #     vector.append(1 if user_inputs[3] == 1 else 0)
# #     vector.append(1 if user_inputs[4] == 1 else 0)
# #     vector.append(1 if user_inputs[5] > 0 and user_inputs[5] <= 5 else 0)
# #     vector.append(1 if user_inputs[6] in ["red", "green", "blue", "purple", "yellow", "grey"] else 0)
# #     return vector


# # def main():
# #     user_inputs = []
# #     user_inputs.append(int(input("Enter min time of video (in seconds): ")))
# #     user_inputs.append(int(input("Enter max number of steps: ")))
# #     user_inputs.append(int(input("Enter min number of steps: ")))
# #     user_inputs.append(int(input("Enter 1 if you want agent to win this game, 0 otherwise: ")))
# #     user_inputs.append(int(input("Enter 1 if you want agent to get stuck on the wall, 0 otherwise: "))) # currently this condition isn't relevant
# #     user_inputs.append(int(input("Enter positsion of the door (choose 1-5):")))
# #     user_inputs.append(str(input("Enter color of the door (red, green, blue, purple, yellow, grey):")))
# #     return query_func(user_inputs)

# # # Get user inputs
# # if __name__ == "__main__":
# #     main()

# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__, template_folder='templates')


# @app.route('/')
# def index():
#     return render_template('UnlockEnv.html')

# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         # Get form data
#         min_duration = int(request.form['minDuration'])
#         max_steps = int(request.form['maxSteps'])
#         min_steps = int(request.form['minSteps'])
#         is_winner = 1 if 'isWinner' in request.form else 0
#         hit_a_wall = 1 if 'hitAWall' in request.form else 0
#         door_position = int(request.form['doorPosition'])
#         key_color = request.form['keyColor']

#         # Process the data (example: print to console)
#         print(f"Min Duration: {min_duration}")
#         print(f"Max Steps: {max_steps}")
#         print(f"Min Steps: {min_steps}")
#         print(f"Is Winner: {is_winner}")
#         print(f"Hit A Wall: {hit_a_wall}")
#         print(f"Door Position: {door_position}")
#         print(f"Key Color: {key_color}")

#         # Redirect to a success page or do further processing
#         return redirect(url_for('success'))

# @app.route('/success')
# def success():
#     return "Form successfully submitted!"

# if __name__ == '__main__':
#     app.run(debug=False)


from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    print("hi index")
    return render_template('UnlockEnv.html')

@app.route('/submit', methods=['POST'])
def submit():
    print("got here!")
    if request.method == 'POST':
        # Get form data
        min_duration = int(request.form['minDuration'])
        max_steps = int(request.form['maxSteps'])
        min_steps = int(request.form['minSteps'])
        is_winner = 1 if 'isWinner' in request.form else 0
        hit_a_wall = 1 if 'hitAWall' in request.form else 0
        door_position = int(request.form['doorPosition'])
        key_color = request.form['keyColor']
        steps_until_key = int(request.form['stepsUntilKey'])

        # Process the data (example: print to console)
        print(f"Min Duration: {min_duration}")
        print(f"Max Steps: {max_steps}")
        print(f"Min Steps: {min_steps}")
        print(f"Is Winner: {is_winner}")
        print(f"Hit A Wall: {hit_a_wall}")
        print(f"Door Position: {door_position}")
        print(f"Key Color: {key_color}")
        print(f"Steps Until Last Picked Key: {steps_until_key}")

        # Redirect to video.html page
        return redirect(url_for('video'))
    else:
        print("Request method is not POST")

@app.route('/video.html')
def video():
    # Render the video.html template
    return render_template('video.html')

if __name__ == '__main__':
    print("Running the app...")
    app.run(debug=True)
