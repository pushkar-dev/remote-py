from flask import Flask, render_template, request, redirect
import os
import datetime
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_entries():
    entries = []
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            entries.append(os.path.join(root, file)[len(UPLOAD_FOLDER) + 1:])
    return entries


def get_current_date_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

@app.route('/')
def index():
    entries = get_entries()
    return render_template('index.html', entries=entries)

def run_cat_command(file_path):
    try:
        result = subprocess.run(['python',  'D:\Projects\code-train\model\train.py', os.path.join(UPLOAD_FOLDER, file_path)], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except FileNotFoundError:
        return f"File not found: {file_path}"

@app.route('/get_path', methods=['POST'])
def get_path():
    file_path = request.form.get('file_path')
    full_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, file_path)
    file_contents = run_cat_command(full_path)
    print(file_contents)
    return render_template('index.html', entries=get_entries())

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Get the current date and time for the folder name
        folder_name = os.path.join(app.config['UPLOAD_FOLDER'], get_current_date_time())
        os.makedirs(folder_name, exist_ok=True)

        # Save the file in the new folder with its original name
        file_path = os.path.join(folder_name, file.filename)
        file.save(file_path)

        return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
