import numpy as np
from collections import deque
from utils import Utils
from config import Config

class SpeedEstimator:
    def __init__(self, max_history=10):
        self.position_history = deque(maxlen=max_history)
        self.time_history = deque(maxlen=max_history)
        self.frame_count = 0
        self.speeds = []
        
    def update_position(self, position, timestamp):
        """Update position history"""
        if position:
            self.position_history.append(position)
            self.time_history.append(timestamp)
            self.frame_count += 1
    
    def calculate_speed(self):
        """Calculate speed based on position history"""
        if len(self.position_history) < 2:
            return 0.0
        
        # Get the most recent positions and times
        current_pos = self.position_history[-1]
        previous_pos = self.position_history[0]
        
        current_time = self.time_history[-1]
        previous_time = self.time_history[0]
        
        # Calculate distance in pixels
        pixel_distance = Utils.calculate_distance(current_pos, previous_pos)
        
        # Calculate time difference
        time_diff = current_time - previous_time
        
        if time_diff == 0:
            return 0.0
        
        # Calculate speed in pixels per second
        pixel_speed = pixel_distance / time_diff
        
        # Convert to meters per second
        real_speed = pixel_speed / Config.PIXELS_PER_METER
        
        return real_speed
    
    def smooth_speed(self, current_speed, alpha=0.7):
        """Apply exponential smoothing to speed readings"""
        if not self.speeds:
            self.speeds.append(current_speed)
            return current_speed
        
        smoothed_speed = alpha * current_speed + (1 - alpha) * self.speeds[-1]
        self.speeds.append(smoothed_speed)
        
        return smoothed_speed
    
    def get_speed_statistics(self):
        """Get speed statistics"""
        if not self.speeds:
            return {"average": 0, "max": 0, "min": 0}
        
        return {
            "average": np.mean(self.speeds),
            "max": np.max(self.speeds),
            "min": np.min(self.speeds)
        }