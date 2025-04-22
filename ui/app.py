"""
This script sets up a Flask web application that streams video frames
from a socket connection. It connects to a server, receives video frames,
and serves them over HTTP. It also provides an endpoint to fetch statistics
like FPS and detection count."""
import struct
import socket
import pickle
import cv2
import requests
from flask import Flask, Response, render_template, jsonify

app = Flask(__name__)

# Socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8001))


def recv_exact(sock, size):
    """Receive exactly 'size' bytes from the socket."""
    buffer = b""
    while len(buffer) < size:
        try:
            packet = sock.recv(size - len(buffer))
            if not packet:
                return None
            buffer += packet
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None
    return buffer


def generate_video():
    """Generate video frames from the socket connection."""
    while True:
        try:
            # Receive the message size
            packed_msg_size = recv_exact(client_socket, struct.calcsize("Q"))
            if not packed_msg_size:
                print("No data received, closing connection.")
                break

            # Unpack the message size
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            frame_data = recv_exact(client_socket, msg_size)
            if not frame_data:
                print("No frame data received, closing connection.")
                break

            # Deserialize the frame
            frame = pickle.loads(frame_data)

            # Convert the frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                print("Failed to encode frame to JPEG.")
                continue

            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        except Exception as e:
            print(f"Error in video generation: {e}")
            break


@app.route('/video_feed')
def video_feed():
    """This is the video feed route."""
    return Response(generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/stats")
def stats():
    """Fetch and return the FPS and detection count from the server."""
    try:
        response = requests.get("http://localhost:8000/metrics")
        metrics = response.text

        fps = detections = None
        for line in metrics.splitlines():
            if line.startswith("fps "):
                fps = float(line.split()[1])
            elif line.startswith("detected_objects "):
                detections = int(float(line.split()[1]))

        return jsonify({
            "fps": round(fps, 2) if fps else "--",
            "detections": detections if detections is not None else "--"
        })
    except requests.exceptions.RequestException:
        return jsonify({"fps": "--", "detections": "--"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True, threaded=True)
