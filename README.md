# InfraScan – Intelligent Road Damage Reporting & Mapping System

InfraScan is an end-to-end web-based platform that automates road damage detection and reporting using machine learning. The system is capable of identifying potholes, cracks, and other road damages from images, visualizing the damage on a map, and (optionally) storing reports in a cloud database like Firebase. This application aims to help governments, municipalities, and citizens track and manage road infrastructure efficiently.

---

## 🚧 Problem Overview

Urban road infrastructure suffers due to delayed maintenance and inefficient manual reporting. Commuters experience frequent inconvenience and vehicle damage due to potholes and cracks. According to Indian Road Congress, poor roads contribute to thousands of accidents annually. 

**Gaps in current solutions:**
- Manual complaint-based systems are slow and underutilized.
- No unified visualization of damage hotspots.
- Lack of transparency and citizen feedback mechanisms.

---

## 💡 Solution Overview

InfraScan solves this by:
- Allowing users to **upload images** of roads via a web interface.
- Using **YOLOv5 deep learning** to detect road damage types in real-time.
- Storing location-tagged damage reports.
- Displaying all reports on an interactive map.

**Future upgrade:**
We plan to integrate a **Road Quality Heatmap**, where roads are color-coded based on report density (Green = good, Red = poor) to help commuters make safer decisions and promote transparency.

---

## ⚙️ Technical Stack & Workflow

- **Frontend**: HTML, CSS, Bootstrap, JavaScript, Leaflet.js
- **Backend**: Flask (Python)
- **Machine Learning**: YOLOv5 (PyTorch)
- **Storage**: Local file system (Firebase integration optional)
- **Mapping**: Leaflet.js for interactive visualization

### 🔁 System Flow:
1. User uploads an image with geolocation.
2. Image is processed by YOLOv5 model.
3. Damage type is predicted and results are stored.
4. Map shows pins with damage info, location, and predicted image.

---

## ✅ Features

- Real-time detection of **Potholes**, **Cracks**, and **Other Damages**.
- Simple **web-based interface** for both users and authorities.
- Interactive map to **view all reported damages**.
- Image comparison: Original vs Predicted (bounding boxes shown).
- Optional Firebase backend support (planned).
- Future support for **real-time road heatmaps**.

---

## 🌐 Real-World Applications

- Smart cities
- Urban governance & municipal corporations
- Public grievance redressal
- Highway safety & monitoring
- Citizen science & community reporting

---

## 💼 Business Potential

- Municipal bodies and road agencies can use InfraScan for data-driven planning.
- Public APIs can enable third-party apps to integrate live road condition feeds.
- Insurance and logistics firms can benefit from route risk mapping.

---

## 🧪 Current Progress

- ✅ Web UI with image upload and prediction.
- ✅ YOLOv5 integration for damage detection.
- ✅ Location capture via browser.
- ✅ Visualization of results on map.
- ✅ Class-wise prediction summary.
- 🔜 Firebase backend for scalable storage.
- 🔜 Road Heatmap based on crowd-reported data.

---


📄 License
This project is open-source and available under the MIT License.


