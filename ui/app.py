from flask import Flask, Response, render_template
import cv2
import time
import os  # <-- Added this line

app = Flask(__name__)

# Open the video file from the same directory as app.py
video_path = os.path.join(os.path.dirname(__file__), "crowd_demo.mp4")
cap = cv2.VideoCapture(video_path)

def generate_video():
    while True:
        ret, frame = cap.read()
        if not ret:
            # Restart the video if it ends
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Convert the frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Yield the frame as a byte stream for Flask
        frame_data = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

        # Control the frame rate (30 FPS)
        time.sleep(1/30)

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
