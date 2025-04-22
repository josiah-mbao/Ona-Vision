""" Client for receiving video stream from server
and displaying it with bounding boxes."""
import socket
import pickle
import struct
import time
import cv2


def recv_exact(sock, size):
    """Receive exactly 'size' bytes from the socket."""
    buffer = b""
    while len(buffer) < size:
        packet = sock.recv(size - len(buffer))
        if not packet:
            return None
        buffer += packet
    return buffer


# Retry logic for connecting to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

MAX_RETRIES = 10
RETRY_DELAY = 2  # seconds

for attempt in range(MAX_RETRIES):
    try:
        print(f"Attempt {attempt + 1} to connect to server...")
        client_socket.connect(("localhost", 8001))
        # Use DNS name "server" for Docker container
        print("Connected to server ✅")
        break
    except socket.gaierror:
        print("DNS resolution failed, retrying...")
        time.sleep(RETRY_DELAY)
    except ConnectionRefusedError:
        print("Server not ready, retrying...")
        time.sleep(RETRY_DELAY)
else:
    print("❌ Failed to connect after multiple attempts. Exiting.")
    exit(1)

# Proceed with receiving and displaying frames
DATA = b""
FRAME_COUNT = 0
start_time = time.time()

while True:
    packed_msg_size = recv_exact(client_socket, struct.calcsize("Q"))
    if not packed_msg_size:
        break
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    frame_data = recv_exact(client_socket, msg_size)
    if not frame_data:
        break

    # Deserialize frame
    frame = pickle.loads(frame_data)

    # Show the video with bounding boxes
    cv2.imshow("Ona Vision - Live Object Detection", frame)

    # Calculate FPS
    FRAME_COUNT += 1
    elapsed_time = time.time() - start_time

    if elapsed_time > 1:  # Update FPS every second
        fps = FRAME_COUNT / elapsed_time
        print(f"Client Streaming FPS: {fps:.2f}")
        FRAME_COUNT = 0
        start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

client_socket.close()
cv2.destroyAllWindows()
