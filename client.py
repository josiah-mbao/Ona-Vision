import cv2
import socket
import pickle
import struct

# Connect to the server (adjust IP and port if necessary)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8000))  # Change IP if needed
data = b""

while True:
    # Receive data from server
    while len(data) < struct.calcsize("Q"):
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet

    packed_msg_size = data[: struct.calcsize("Q")]
    data = data[struct.calcsize("Q"):]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize frame
    frame = pickle.loads(frame_data)

    # Show the video with bounding boxes
    cv2.imshow("Ona Vision - Live Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

client_socket.close()
cv2.destroyAllWindows()

