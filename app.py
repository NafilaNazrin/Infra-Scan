from flask import Flask, render_template, request, jsonify
import pathlib
import sys
import os, json
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime

# Fix path compatibility for Windows
if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath

# Append YOLO path
sys.path.append('yolov5')


from detect import run  # Assuming your yolov5/detect.py is correct

# Flask App Setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PREDICT_FOLDER'] = 'static/predicted'
REPORTS_FILE = 'reports.json'
WEIGHTS_PATH = 'best.pt'
CLASS_NAMES = ["Pothole", "Crack", "Other Damage"]

# Ensure folders exist
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['PREDICT_FOLDER']).mkdir(parents=True, exist_ok=True)

# Save report data locally
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

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    lat = request.form.get('latitude')
    lon = request.form.get('longitude')

    if not lat or not lon:
        return jsonify({'error': 'Location not provided or denied by browser'}), 400

    # Save original image
    filename = datetime.now().strftime("%Y%m%d%H%M%S_") + secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    # Run YOLOv5
    run(
        weights=WEIGHTS_PATH,
        source=image_path,
        project=app.config['PREDICT_FOLDER'],
        name='exp',
        exist_ok=True,
        save_txt=True,
        save_conf=True,
        save_crop=False,
    )

    # Find prediction result image
    exp_folder = os.path.join(app.config['PREDICT_FOLDER'], 'exp')
    predicted_image_path = os.path.join(exp_folder, filename)

    # Get labels from TXT file
    label_file = os.path.join(exp_folder, 'labels', os.path.splitext(filename)[0] + '.txt')
    detected_classes = []

    if os.path.exists(label_file):
        with open(label_file, 'r') as f:
            for line in f:
                class_id = int(line.strip().split()[0])
                class_name = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else f"Class {class_id}"
                detected_classes.append(class_name)

    detected_str = ', '.join(sorted(set(detected_classes))) if detected_classes else "No Damage Detected"

    # Build report
    report = {
        "image": filename,
        "prediction": detected_str,
        "latitude": float(lat),
        "longitude": float(lon),
        "predicted_image": f"predicted/exp/{filename}"
    }

    save_report(report)
    return jsonify(report)

@app.route('/reports')
def reports():
    if not os.path.exists(REPORTS_FILE):
        return jsonify([])
    with open(REPORTS_FILE, 'r') as f:
        return jsonify(json.load(f))



if __name__ == "__main__":
    port = int(os.environ["PORT"])  # <-- no default here!
    app.run(host="0.0.0.0", port=port, debug=True)
