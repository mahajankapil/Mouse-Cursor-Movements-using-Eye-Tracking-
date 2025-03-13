from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import voicecmd  # Import the voicecmd module
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/run_another_script', methods=['POST'])
def run_another_script():
    try:
        # Use subprocess to run another Python script
        subprocess.run(['python', 'eye_controlled_mouse.py'])
        return "Successfully ran another Python script."
    except Exception as e:
        return f"Error running script: {str(e)}"
@app.route('/run_another_script1', methods=['POST'])
def run_another_script1():
    try:
        command = voicecmd.take_command()  # Capture the returned command
        return jsonify(command=command)  # Return the command in the response
    except Exception as e:
        return jsonify(error=str(e))
@app.route('/run_another_script2', methods=['POST'])
def run_another_script2():
    try:
        # Use subprocess to run another Python script
        subprocess.run(['python', 'handgesture.py'])
        return "Successfully ran another Python script."
    except Exception as e:
        return f"Error running script: {str(e)}"
if __name__ == '__main__':
    app.run(debug=True)
