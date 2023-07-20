from subs.Camera import Camera
from flask import Flask, Response, render_template
import av
import cv2


camera = Camera()

camera.initCamera()

app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    return Response(stream_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream_frames():
    while True:
        camera.getData()
        image = camera.image
        # image_bytes = cv2.imencode('.jpg', image)[1].tobytes()  # Convert to JPEG byte array
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')







