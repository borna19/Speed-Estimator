import cv2
import numpy as np
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt

class Utils:
    @staticmethod
    def preprocess_frame(frame):
        """Preprocess frame for motion detection"""
        # Resize frame
        frame = cv2.resize(frame, (640, 480))
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)
        
        return gray, blurred
    
    @staticmethod
    def calculate_centroid(contour):
        """Calculate centroid of a contour"""
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
        return None
    
    @staticmethod
    def calculate_distance(point1, point2):
        """Calculate Euclidean distance between two points"""
        return dist.euclidean(point1, point2)
    
    @staticmethod
    def draw_motion_info(frame, centroid, speed, contour):
        """Draw motion information on frame"""
        if centroid:
            # Draw centroid
            cv2.circle(frame, centroid, 5, (0, 0, 255), -1)
            
            # Draw bounding box
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display speed
            cv2.putText(frame, f"Speed: {speed:.2f} m/s", 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display centroid coordinates
            cv2.putText(frame, f"Position: {centroid}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    @staticmethod
    def create_background_subtractor():
        """Create background subtractor"""
        return cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)