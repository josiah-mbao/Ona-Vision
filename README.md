# Real-Time Object Detection with YOLOv8 and Video Streaming
<img width="954" alt="library demo" src="https://github.com/user-attachments/assets/44bb0021-983a-4e7a-82d2-acc6acae964a" />

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

```bash
python download-model.py
```

## How It Works
1. The **server** captures frames from the webcam and runs YOLOv8 for object detection.
2. Bounding boxes and labels are added to the frame.
3. The processed frame is serialized and sent to the **client** over a socket connection.
4. The **client** receives and displays the video in real-time.

## Demo
![Real-Time Detection Example]

https://github.com/user-attachments/assets/8246bf73-b810-48b7-9b8b-a855f730fb1f


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


