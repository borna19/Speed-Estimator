import cv2

def test_camera():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return False
    
    ret, frame = cap.read()
    if ret:
        print("Camera is working! Frame shape:", frame.shape)
        cap.release()
        return True
    else:
        print("Error: Could not read frame from camera")
        cap.release()
        return False

if __name__ == "__main__":
    test_camera()