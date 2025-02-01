from picamera2 import Picamera2
import cv2
from flask import Flask, render_template, request, jsonify, Response


picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

app = Flask(__name__)

def generate_frames():
    while True:
        # Capture image from camera
        frame = picam2.capture_array()
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        # MJPEG streaming response
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
