import os
import subprocess
import threading
from flask import Flask, request, jsonify, send_from_directory, render_template
import platform

app = Flask(__name__)

# Define the folder where images will be stored
UPLOAD_FOLDER = 'uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Make sure the uploaded folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to handle image file uploads
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'status': 'failure', 'message': 'No file part'}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({'status': 'failure', 'message': 'No selected file'}), 400

    # Ensure the file is an image (optional, you can skip or modify this part)
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return jsonify({'status': 'failure', 'message': 'Invalid file type'}), 400

    # Save the file with the same name (overwrite if file exists)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({'status': 'success', 'message': f'File uploaded successfully: {file.filename}', 'file_path': file_path})


# Route to view an uploaded file
@app.route('/uploaded/<filename>', methods=['GET'])
def uploaded_file(filename):
    # Check if the file exists
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({'status': 'failure', 'message': 'File not found'}), 404


# Function to execute git commands in the background
def execute_git_commands():
    try:
        # Determine the correct directory based on the OS
        if platform.system() == "Windows":
            os.chdir('C:\\Users\\YourUsername\\Projects\\roadmapv2_LRM')  # Replace with your actual path
        else:
            os.chdir('/home/roadmapv2_LRM')  # For Linux-based systems

        # Execute git commands
        # subprocess.run(['git', 'restore', '.'], check=True)
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

