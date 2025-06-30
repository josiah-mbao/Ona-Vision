<p align="center">
<img width="500" height="395" alt="logo" src="https://github.com/user-attachments/assets/ad7173d1-7dee-471d-8a2e-cc707cf3306c" />
</p>

# Ona Vision 🎯 — Real-Time Object Detection & Monitoring with YOLOv8, DeepSORT, and MLOps
[![GitHub stars](https://img.shields.io/github/stars/josiah-mbao/ona-vision?style=social)](https://github.com/josiah-mbao/ona-vision/stargazers)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-black?style=for-the-badge&logo=opencv&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-623CE4?style=for-the-badge&logo=terraform&logoColor=white)

## Tech Stack

- 🐍 Python 3.10
- 🧠 YOLOv8 (Ultralytics)
- 🔍 DeepSORT
- 📦 Docker
- ☸️ Kubernetes
- 📊 Prometheus
- 🧪 FastAPI (for Web UI)
- 🧱 Terraform (for infra-as-code)

## Table of Contents
- [Overview](#overview)
- [The Inspiration](#the-inspiration)
- [Features](#features)
- [Web UI](#web-ui)
- [Multi-Object Tracking (MOT) with DeepSORT](#multi-object-tracking-mot-with-deepsort)
- [Setup Instructions](#setup-instructions)
- [How It Works](#how-it-works)
- [Observability Metrics](#observability-metrics)
- [Potential Improvements](#potential-improvements)
- [License](#license)
- [Author](#author)


## Overview

This project implements real-time object detection using YOLOv8 and streams the processed video over a network. The server captures video from a webcam, performs object detection, and sends the processed frames to a client for display. Additionally, it integrates observability features using Prometheus to monitor system performance and model inference metrics.

Ona Vision is a full MLOps pipeline, covering the complete lifecycle of a machine learning model, from training to deployment, monitoring, and scaling. It leverages Docker, Kubernetes, and GitOps to ensure a scalable and reliable production system for object detection and monitoring.
  

<p align="center">
  <img width="700" alt="demo" src="https://github.com/user-attachments/assets/2263076d-61f8-4ba1-9986-2fc40656acb4" />
</p>



### The Inspiration

Ona Vision was born out of a frustrating and unfortunate experience I had. I lost — or possibly had my AirPods stolen — at my university library. In an attempt to recover them, I spent nearly an hour in the CCTV office scrubbing through days of footage, trying to figure out what time I was at the library and if the AirPods could be spotted in any frame.

The process was slow and inefficient—like looking for a needle in a haystack. Unfortunately, I never found my AirPods, but I walked away with an idea.

**Ona Vision** is my attempt to ensure others don’t have to go through that same helpless process. With object detection and tracking built in, this system can help people and institutions monitor and trace specific objects in real-time or recorded video streams. It’s my hope that this technology can make environments a little safer, and surveillance systems a lot smarter.


## Features
- Uses **YOLOv8** for state-of-the-art object detection
- **Real-time video processing** with OpenCV
- **Network streaming** using Python sockets
- **Bounding box rendering** with object labels
- **Observability integration** with Prometheus for:
  - FPS (Frames Per Second)
  - Inference time
  - CPU and memory usage
  - Detection confidence and per-class object count

## Web UI
You can now launch the detection system and view results from your browser using FastAPI.

<img width="1440" alt="Screenshot 2025-06-26 at 01 32 37" src="https://github.com/user-attachments/assets/029088ab-e3cd-4b42-aa75-ff9d30643e2b" />



### To Run the Web UI:
```bash
cd ui
uvicorn app:app --reload
```
Then visit [http://localhost:8000](http://localhost:8000) in your browser.


## Multi-Object Tracking (MOT) with DeepSORT

### What is DeepSORT?
DeepSORT (Deep Simple Online and Realtime Tracker) is an advanced object tracking algorithm that extends the original SORT tracker by adding deep learning-based appearance descriptors. This helps improve object re-identification across frames, making tracking more reliable in crowded or fast-moving scenes.

### Why Use DeepSORT?
- **Tracks multiple objects across frames** with consistent IDs.
- **Handles occlusions** (when objects overlap or disappear temporarily).
- **Re-identifies objects** even if they leave and re-enter the scene.
- **More accurate tracking** compared to basic object detection.

### How It Works in Ona Vision
1. **YOLOv8 detects objects** in each frame.
2. **DeepSORT assigns unique IDs** to detected objects.
3. **Tracks objects over time**, even if they move, overlap, or briefly disappear.
4. **Outputs tracking results** with bounding boxes and IDs.

### Performance Impact
- Adds a **small processing overhead** (~5-10% FPS drop).
- More stable tracking compared to detection-only mode.
- Ideal for **surveillance, traffic monitoring, and sports analytics**.


## Setup Instructions

Install Libraries from requirements.txt
```bash
pip install -r requirements.txt
```

Start the server which processes frames from webcam or other source
```bash
python main.py
```

Display real-time video in web UI (at localhost:8000)
```bash
cd ui
uvicorn app:app --reload
```

## How It Works
1. The **server** captures frames from the webcam and runs YOLOv8 for object detection.
2. Bounding boxes and labels are added to the frame.
3. The processed frame is serialized and sent to the **client** over a socket connection.
4. The **client** receives and displays the video in real-time.
5. **Prometheus metrics** are collected in the background, tracking performance and inference statistics.

## Observability Metrics
| Metric | Description |
|--------|-------------|
| **FPS** | Frames per second for performance monitoring |
| **Inference Time** | Time taken for YOLOv8 inference per frame |
| **CPU Usage** | System CPU utilization during processing |
| **Memory Usage** | System memory consumption during processing |
| **Detection Confidence** | Average confidence of detected objects per frame |
| **Class-wise Object Count** | Tracks the number of detected objects per class |


## Potential Improvements
- **Edge deployment** on a Raspberry Pi or Jetson Nano
- **Cloud integration** to store detection data
- **Web-based visualization** using FastAPI

## Contributing
Contributions are welcome! If you find a bug or want to add a feature, feel free to open an issue or submit a pull request.

Please make sure to discuss big changes in an issue first to ensure alignment.

## License
This project is open-source under the **Apache 2.0 License**.
- You are free to use, modify, and distribute the code under the terms of the Apache 2.0 License.

## Author
Josiah Mbao – Software Engineer | MLOps Developer  
🔗 GitHub | ✉️ josiahmbaomc@gmail.com

---
If you found this project useful, please ⭐ the repo to support the work!
