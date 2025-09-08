import os
import subprocess
import threading
from flask import Flask, render_template, jsonify
import platform

app = Flask(__name__)

# Function to execute git commands in the background
def execute_git_commands():
    try:
        # Determine the correct directory based on the OS
        if platform.system() == "Windows":
            os.chdir('C:\\Users\\YourUsername\\Projects\\roadmapv2_LRM')  # Replace with your actual path
        else:
            os.chdir('/home/roadmapv2_LRM')  # For Linux-based systems

        # Execute git commands
        subprocess.run(['git', 'restore', '.'], check=True)
        subprocess.run(['git', 'pull'], check=True)
        # print("hello")
        return "success"
    except FileNotFoundError as e:
        return f"failure: Directory not found ({str(e)})"
    except subprocess.CalledProcessError as e:
        return f"failure: Git command failed ({str(e)})"
    except Exception as e:
        return f"failure: Unexpected error ({str(e)})"

# Route to render the page
@app.route('/pull')
def pull():
    return render_template('index.html')

# API route to handle the pull request
@app.route('/execute_pull', methods=['POST'])
def execute_pull():
    # result_message = []
    result_message = ""

    # Define the background task
    def task():
        try:
            result = execute_git_commands()  # Get the result from the git commands
            result_message = result
            print(result)
        except Exception as e:
            result_message.append(f"Error in task execution: {str(e)}")

    # Start the background task in a separate thread
    thread = threading.Thread(target=task)
    thread.start()
    thread.join()  # Wait for the task to complete

    # After the task completes, return the result message
    return jsonify({'status': 'done', 'message': result_message})

if __name__ == "__main__":
    app.run(debug=True)
