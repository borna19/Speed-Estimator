# 🚗 Speed Estimator

## Project Overview

Speed Estimator is a computer vision-based application that detects moving vehicles and estimates their speed in real time using video processing techniques. The system analyzes video frames, tracks object movement, calculates speed, and displays live monitoring data through a web-based dashboard.

Built using Python, Flask, OpenCV, and NumPy, this project demonstrates the practical application of motion detection, object tracking, and real-time analytics for intelligent transportation and traffic monitoring systems.

---

## Features

* Real-Time Vehicle Speed Estimation
* Live Video Streaming
* Motion Detection and Tracking
* Vehicle Monitoring Dashboard
* Speed History Tracking
* Real-Time Data Updates
* Computer Vision-Based Analysis
* Web-Based User Interface
* Lightweight and Fast Processing
* Easy Configuration and Deployment

---

## Technologies Used

* Python
* Flask
* OpenCV
* NumPy
* HTML
* CSS
* JavaScript
* Computer Vision

---

## Project Structure

```text
speed_estimator/

├── static/
│   ├── css
│   ├── js
│   └── images
│
├── templates/
│   └── HTML Templates
│
├── tests/
│   └── Test Files
│
├── app.py
├── config.py
├── motion_detector.py
├── speed_estimator.py
├── utils.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Speed-Estimator.git

cd Speed-Estimator
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

### 6. Open in Browser

```text
http://127.0.0.1:5000
```

---

## System Workflow

### Video Processing

* Capture live video feed.
* Process video frames continuously.
* Detect moving objects in the scene.
* Extract motion-related information.

### Vehicle Tracking

* Identify moving vehicles.
* Track vehicle movement across frames.
* Measure travel distance between frames.
* Maintain tracking history.

### Speed Calculation

* Analyze movement patterns.
* Calculate estimated speed.
* Update speed records in real time.
* Store speed history for monitoring.

### Dashboard Monitoring

* Display live video stream.
* Show current vehicle speed.
* Track monitoring status.
* Present real-time analytics.

---

## Core Modules

### Motion Detection Module

* Object Detection
* Motion Analysis
* Frame Processing
* Movement Tracking

### Speed Estimation Module

* Distance Calculation
* Speed Computation
* Real-Time Monitoring
* Data Processing

### Flask Web Application

* Dashboard Interface
* Live Video Feed
* API Endpoints
* Data Visualization

### Utility Module

* Helper Functions
* Configuration Management
* Data Formatting
* System Support

---

## Requirements

```text
Flask
OpenCV-Python
NumPy
Matplotlib
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Future Enhancements

* Multi-Vehicle Tracking
* Deep Learning-Based Vehicle Detection
* Traffic Density Analysis
* Vehicle Classification
* Speed Violation Alerts
* Data Export and Reporting
* Cloud-Based Monitoring
* Advanced Dashboard Analytics

---

## Author

Developed by: Barnali Bhowmik

---

## License

This project is created for educational and learning purposes. Feel free to modify and improve it as needed.

⭐ If you find this project useful, please give it a star.
