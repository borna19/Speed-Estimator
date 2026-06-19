import cv2

class Config:
    # Video input settings
    VIDEO_SOURCE = 0  # 0 for webcam, or path to video file
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    # Motion detection settings
    MIN_CONTOUR_AREA = 500
    BLUR_KERNEL_SIZE = (21, 21)
    THRESHOLD_VALUE = 25
    MAX_THRESHOLD = 255
    
    # Speed estimation settings
    PIXELS_PER_METER = 100  # Calibration value - adjust based on your setup
    FPS = 30  # Frames per second
    
    # Display settings
    DISPLAY_SCALE = 1.0
    SHOW_CONTOURS = True
    SHOW_MOTION_AREA = True
    
    # Colors (BGR format)
    COLOR_RED = (0, 0, 255)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (255, 0, 0)
    COLOR_WHITE = (255, 255, 255)