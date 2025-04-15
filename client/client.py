import cv2
import socket
import pickle
import struct
import time

def recv_exact(sock, size):
    buffer = b""
    while len(buffer) < size:
        packet = sock.recv(size - len(buffer))
        if not packet:
            return None
        buffer += packet
    return buffer

# Retry logic for connecting to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

max_retries = 10
retry_delay = 2  # seconds

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt + 1} to connect to server...")
        client_socket.connect(("server", 8001))  # Use Docker service name
        print("Connected to server ✅")
        break
    except socket.gaierror:
        print("DNS resolution failed, retrying...")
        time.sleep(retry_delay)
    except ConnectionRefusedError:
        print("Server not ready, retrying...")
        time.sleep(retry_delay)
else:
    print("❌ Failed to connect after multiple attempts. Exiting.")
    exit(1)

# Proceed with receiving and displaying frames
data = b""
frame_count = 0
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
    frame_count += 1
    elapsed_time = time.time() - start_time

    if elapsed_time > 1:  # Update FPS every second
        fps = frame_count / elapsed_time
        print(f"Client Streaming FPS: {fps:.2f}")
        frame_count = 0
        start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

client_socket.close()
cv2.destroyAllWindows()
