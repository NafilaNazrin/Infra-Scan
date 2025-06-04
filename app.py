import pathlib
import sys

# Fix: Make PosixPath map to WindowsPath if running on Windows
if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath

from flask import Flask, render_template, request, jsonify
import os, json, glob
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import sys

# Add yolov5 to Python path
sys.path.append('yolov5')
from detect import run  # YOLOv5 detect function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PREDICT_FOLDER'] = 'static/predictions'
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['PREDICT_FOLDER']).mkdir(parents=True, exist_ok=True)

REPORTS_FILE = 'reports.json'
WEIGHTS_PATH = 'best.pt'  # Your YOLO model

def save_report(data):
    if not os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, 'w') as f:
            json.dump([], f)
    with open(REPORTS_FILE, 'r') as f:
        reports = json.load(f)
    reports.append(data)
    with open(REPORTS_FILE, 'w') as f:
        json.dump(reports, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    lat = request.form.get('latitude')
    lon = request.form.get('longitude')

    if not lat or not lon:
        return jsonify({'error': 'Location not provided or denied by browser'}), 400

    # Save uploaded image
    filename = datetime.now().strftime("%Y%m%d%H%M%S_") + secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    # Clean old prediction folders if needed (optional)
    # for f in glob.glob(os.path.join(app.config['PREDICT_FOLDER'], 'exp*')):
    #     shutil.rmtree(f)

    # Run detection
    run(
        weights=WEIGHTS_PATH,
        source=image_path,
        project=app.config['PREDICT_FOLDER'],
        name='exp',            # Will save in static/predictions/exp/
        exist_ok=True,
        save_txt=False,
        save_conf=True,
        save_crop=False,
        # save_img=True         # Critical: save output image
    )

    # Find the detected image path
    output_folder = os.path.join(app.config['PREDICT_FOLDER'], 'exp')
    predicted_image_path = os.path.join(output_folder, filename)

    # Check if YOLO saved the result image
    if not os.path.exists(predicted_image_path):
        return jsonify({'error': 'Detection failed or no objects found'}), 500

    # Save report
    report = {
        "image": filename,
        "prediction": "Detected",  # Can be improved to actual class
        "latitude": lat,
        "longitude": lon,
        "predicted_image": predicted_image_path.replace('\\', '/')
    }
    save_report(report)

    return jsonify(report)

@app.route('/reports')
def reports():
    if not os.path.exists(REPORTS_FILE):
        return jsonify([])
    with open(REPORTS_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
