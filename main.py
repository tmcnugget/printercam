from picamera2 import Picamera2
from flask import Flask, render_template, request, jsonify, Response
from PIL import Image
import io

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

app = Flask(__name__)

def generate_frames():
    while True:
        # Capture image from camera as a numpy array
        frame = picam2.capture_array()
        # Convert the array to a PIL Image
        img = Image.fromarray(frame).convert("RGB")
        # Save image to an in-memory bytes buffer as JPEG
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        frame_bytes = buffer.getvalue()
        # Yield the frame in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
