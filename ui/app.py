from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
import base64
import time
from auth.routes import router as auth_router

app = FastAPI()
app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

cap = cv2.VideoCapture(0)  # or your video file


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/video")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    prev_time = time.time()
    while True:
        success, frame = cap.read()
        if not success:
            continue

        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame_b64 = base64.b64encode(buffer).decode('utf-8')

        # FPS calculation
        curr_time = time.time()
        fps = round(1 / (curr_time - prev_time), 2)
        prev_time = curr_time

        # Example stats
        payload = {
            "frame": frame_b64,
            "stats": {
                "model": "OnaNet v1.0",
                "fps": fps,
                "detections": "None"  # Replace with real detections later
            }
        }

        await websocket.send_json(payload)
