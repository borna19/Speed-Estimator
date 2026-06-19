from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
import time
import threading

# Import your speed estimator modules
from motion_detector import MotionDetector
from speed_estimator import SpeedEstimator
from utils import Utils
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global variables
current_speed = 0.0
speed_history = []
camera = None
is_running = False

class Camera:
    def __init__(self):
        self.cap = None
        self.motion_detector = MotionDetector()
        self.speed_estimator = SpeedEstimator()
        self.start_time = 0
        self.frame_count = 0

    def start(self, source=0):
        try:
            self.cap = cv2.VideoCapture(source)
            if not self.cap.isOpened():
                return False
            self.start_time = time.time()
            self.frame_count = 0
            return True
        except Exception as e:
            print(f"Camera error: {e}")
            return False

    def stop(self):
        if self.cap:
            self.cap.release()
            self.cap = None

    def get_frame(self):
        global current_speed, speed_history
        
        if not self.cap:
            return None, 0.0

        ret, frame = self.cap.read()
        if not ret:
            return None, 0.0

        self.frame_count += 1
        
        # Process frame
        gray, blurred = Utils.preprocess_frame(frame)
        motion_mask = self.motion_detector.detect_motion_bg_subtraction(blurred)
        contour, centroid = self.motion_detector.get_largest_motion_region(motion_mask)
        
        # Calculate speed
        speed = 0.0
        if centroid:
            current_time = time.time() - self.start_time
            self.speed_estimator.update_position(centroid, current_time)
            raw_speed = self.speed_estimator.calculate_speed()
            speed = self.speed_estimator.smooth_speed(raw_speed)
            Utils.draw_motion_info(frame, centroid, speed, contour)
            
            print(f"Motion detected! Speed: {speed:.2f} m/s")

        current_speed = speed
        if speed > 0:
            speed_history.append(speed)
            if len(speed_history) > 50:
                speed_history.pop(0)

        # Add status text
        cv2.putText(frame, f"Frames: {self.frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Status: {'RUNNING' if is_running else 'STOPPED'}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            return None, 0.0
            
        return buffer.tobytes(), speed

# Global camera instance
camera = Camera()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global is_running, camera
    try:
        source = int(request.json.get('source', 0))
        print(f"Starting camera with source {source}")
        
        if camera.start(source):
            is_running = True
            return jsonify({'status': 'success', 'message': 'Camera started!'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to start camera'})
    except Exception as e:
        print(f"Start error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global is_running, camera
    is_running = False
    camera.stop()
    return jsonify({'status': 'success', 'message': 'Camera stopped'})

@app.route('/video_feed')
def video_feed():
    def generate():
        while is_running:
            frame_bytes, speed = camera.get_frame()
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.033)  # ~30 FPS
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_speed_data')
def get_speed_data():
    global current_speed, speed_history, is_running
    
    status = 'inactive'
    if is_running:
        status = 'active' if current_speed > 0 else 'monitoring'
    
    return jsonify({
        'current_speed': current_speed,
        'average_speed': np.mean(speed_history) if speed_history else 0,
        'max_speed': np.max(speed_history) if speed_history else 0,
        'status': status
    })

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Contact: {name}, {email}, {message}")
        return jsonify({'status': 'success', 'message': 'Message received!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Speed Estimator...")
    print("📹 Open http://localhost:5000/detection")
    print("💡 Click 'Start Detection' and wave your hand in front of camera")
    app.run(debug=True, port=5000)