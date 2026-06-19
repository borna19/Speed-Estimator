import cv2
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Video Test</h1>
            <img src="/video" width="640" height="480">
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5001)