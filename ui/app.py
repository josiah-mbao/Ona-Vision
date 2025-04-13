from flask import Flask, Response, render_template
import cv2
import time

app = Flask(__name__)

# Open the webcam or video feed (you can replace this with your own video source)
cap = cv2.VideoCapture(0)  # This is the default webcam; replace with video feed if needed

def generate_video():
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break
        
        # Convert the frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame.")
            continue

        # Yield the frame as a byte stream for Flask
        frame_data = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

        # Control the frame rate (e.g., 30 FPS)
        time.sleep(1/30)  # Sleep to control FPS

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
