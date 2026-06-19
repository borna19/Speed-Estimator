import cv2
import numpy as np
from config import Config
from utils import Utils

class MotionDetector:
    def __init__(self):
        self.background_subtractor = Utils.create_background_subtractor()
        self.previous_frame = None
        self.motion_history = []
        
    def detect_motion_frame_diff(self, current_frame):
        """Detect motion using frame difference method"""
        if self.previous_frame is None:
            self.previous_frame = current_frame
            return None, None
        
        # Compute absolute difference between current and previous frame
        frame_diff = cv2.absdiff(self.previous_frame, current_frame)
        
        # Apply threshold
        _, thresh = cv2.threshold(frame_diff, Config.THRESHOLD_VALUE, Config.MAX_THRESHOLD, cv2.THRESH_BINARY)
        
        # Apply morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
        thresh = cv2.erode(thresh, kernel, iterations=1)
        
        self.previous_frame = current_frame
        
        return thresh, frame_diff
    
    def detect_motion_bg_subtraction(self, frame):
        """Detect motion using background subtraction"""
        # Apply background subtraction
        fg_mask = self.background_subtractor.apply(frame)
        
        # Apply threshold to get binary image
        _, thresh = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
        
        # Apply morphological operations
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return thresh
    
    def get_motion_contours(self, motion_mask):
        """Extract contours from motion mask"""
        contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area
        significant_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > Config.MIN_CONTOUR_AREA:
                significant_contours.append(contour)
        
        return significant_contours
    
    def get_largest_motion_region(self, motion_mask):
        """Get the largest motion region"""
        contours = self.get_motion_contours(motion_mask)
        
        if not contours:
            return None, None
        
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        centroid = Utils.calculate_centroid(largest_contour)
        
        return largest_contour, centroid