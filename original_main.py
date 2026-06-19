import cv2
import time
import argparse
from motion_detector import MotionDetector
from speed_estimator import SpeedEstimator
from utils import Utils
from config import Config
import numpy as np

class SpeedMotionDetectorApp:
    def __init__(self, video_source=Config.VIDEO_SOURCE):
        self.video_source = video_source
        self.cap = None
        self.motion_detector = MotionDetector()
        self.speed_estimator = SpeedEstimator()
        self.running = False
        self.start_time = time.time()
        
    def initialize_video_capture(self):
        """Initialize video capture"""
        self.cap = cv2.VideoCapture(self.video_source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
        
        if not self.cap.isOpened():
            print("Error: Could not open video source")
            return False
        return True
    
    def process_frame(self, frame):
        """Process a single frame for motion detection and speed estimation"""
        # Preprocess frame
        gray, blurred = Utils.preprocess_frame(frame)
        
        # Detect motion using background subtraction
        motion_mask = self.motion_detector.detect_motion_bg_subtraction(blurred)
        
        # Get largest motion region
        contour, centroid = self.motion_detector.get_largest_motion_region(motion_mask)
        
        # Calculate speed if motion detected
        speed = 0.0
        if centroid:
            current_time = time.time() - self.start_time
            self.speed_estimator.update_position(centroid, current_time)
            raw_speed = self.speed_estimator.calculate_speed()
            speed = self.speed_estimator.smooth_speed(raw_speed)
            
            # Draw motion information
            Utils.draw_motion_info(frame, centroid, speed, contour)
        
        # Display motion mask
        motion_display = cv2.cvtColor(motion_mask, cv2.COLOR_GRAY2BGR)
        
        # Combine original frame and motion mask
        combined = np.hstack([frame, motion_display])
        
        # Add FPS information
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(combined, f"FPS: {fps:.1f}", (10, combined.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return combined, speed
    
    def run(self):
        """Main application loop"""
        if not self.initialize_video_capture():
            return
        
        self.running = True
        print("Speed Motion Detector Started!")
        print("Press 'q' to quit, 'r' to reset statistics")
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("End of video stream")
                    break
                
                # Process frame
                processed_frame, speed = self.process_frame(frame)
                
                # Display result
                cv2.imshow('Speed Motion Detector', processed_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.speed_estimator = SpeedEstimator()
                    print("Statistics reset!")
                
                # Print speed information
                if speed > 0:
                    print(f"Current Speed: {speed:.2f} m/s")
        
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        # Print final statistics
        stats = self.speed_estimator.get_speed_statistics()
        print("\n=== Final Statistics ===")
        print(f"Average Speed: {stats['average']:.2f} m/s")
        print(f"Maximum Speed: {stats['max']:.2f} m/s")
        print(f"Minimum Speed: {stats['min']:.2f} m/s")

def main():
    parser = argparse.ArgumentParser(description='Speed Motion Detector')
    parser.add_argument('--video', type=str, default=Config.VIDEO_SOURCE,
                       help='Video source (0 for webcam, or path to video file)')
    parser.add_argument('--pixels_per_meter', type=float, default=Config.PIXELS_PER_METER,
                       help='Pixels per meter for calibration')
    
    args = parser.parse_args()
    
    # Update configuration
    Config.VIDEO_SOURCE = args.video
    Config.PIXELS_PER_METER = args.pixels_per_meter
    
    # Create and run application
    app = SpeedMotionDetectorApp(args.video)
    app.run()

if __name__ == "__main__":
    main()