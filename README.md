# Real-Time Object Detection with YOLOv8 and Video Streaming

## Overview
This project implements **real-time object detection** using **YOLOv8** and streams the processed video over a network. The server captures video from a webcam, performs object detection, and sends the processed frames to a client for display.

## Features
- Uses **YOLOv8** for state-of-the-art object detection
- **Real-time video processing** with OpenCV
- **Network streaming** using Python sockets
- **Bounding box rendering** with object labels

## Technologies Used
- Python
- OpenCV
- PyTorch
- Ultralytics YOLOv8
- Socket Programming

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/josiah-mbao/realtime-object-detection.git
cd realtime-object-detection
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download YOLOv8 Model
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

### 5. Run the Server
```bash
python main.py
```

### 6. Run the Client
```bash
python client.py
```

## How It Works
1. The **server** captures frames from the webcam and runs YOLOv8 for object detection.
2. Bounding boxes and labels are added to the frame.
3. The processed frame is serialized and sent to the **client** over a socket connection.
4. The **client** receives and displays the video in real-time.

## Demo
![Real-Time Detection Example](demo.gif)

## Potential Improvements
- **Multi-object tracking** using DeepSORT
- **Edge deployment** on a Raspberry Pi or Jetson Nano
- **Cloud integration** to store detection data
- **Web-based visualization** using Flask or FastAPI

## License
This project is open-source under the MIT License.

## Author
**Josiah Mbao**  
🔗 [GitHub](https://github.com/josiah-mbao)  |  ✉️ josiahmbaomc@gmail.com


