import cv2
import time
import numpy as np
from motion_detector import MotionDetector
from speed_estimator import SpeedEstimator
from utils import Utils

def test_with_sample_video():
    """Test with a sample video or webcam"""
    print("Testing Motion Detector...")
    
    # Initialize components
    motion_detector = MotionDetector()
    speed_estimator = SpeedEstimator()
    
    # Use webcam or sample video
    cap = cv2.VideoCapture(0)  # Change to video file path if needed
    
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Preprocess frame
        gray, blurred = Utils.preprocess_frame(frame)
        
        # Detect motion
        motion_mask = motion_detector.detect_motion_bg_subtraction(blurred)
        contour, centroid = motion_detector.get_largest_motion_region(motion_mask)
        
        # Calculate speed
        current_time = time.time() - start_time
        speed = 0.0
        
        if centroid:
            speed_estimator.update_position(centroid, current_time)
            speed = speed_estimator.calculate_speed()
            
            # Draw information
            Utils.draw_motion_info(frame, centroid, speed, contour)
            print(f"Motion detected at {centroid}, Speed: {speed:.2f} m/s")
        
        # Display
        cv2.imshow('Test - Motion Detection', frame)
        cv2.imshow('Test - Motion Mask', motion_mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def test_calibration():
    """Test calibration with known distances"""
    print("Testing calibration...")
    
    # Create a synthetic test - move an object a known distance
    test_positions = [(100, 100), (200, 100)]  # 100 pixel movement
    speed_estimator = SpeedEstimator()
    
    start_time = time.time()
    for i, pos in enumerate(test_positions):
        speed_estimator.update_position(pos, start_time + i * 0.1)
    
    calculated_speed = speed_estimator.calculate_speed()
    expected_speed = 100 / 100 / 0.1  # pixels/meter / time
    
    print(f"Expected speed: {expected_speed:.2f} m/s")
    print(f"Calculated speed: {calculated_speed:.2f} m/s")
    print(f"Calibration accuracy: {abs(expected_speed - calculated_speed)/expected_speed * 100:.1f}%")

if __name__ == "__main__":
    print("=== Motion Detector Tests ===")
    test_calibration()
    print("\n=== Real-time Test ===")
    test_with_sample_video()