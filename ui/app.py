from fastapi import FastAPI, WebSocket, Request, Depends, HTTPException, Cookie
from fastapi import FastAPI, WebSocket, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from auth.auth import decode_access_token
from auth.schemas import User
import cv2
import base64
import time
from auth.routes import router as auth_router
from typing import Optional
from auth.dependencies import get_current_user

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

cap = cv2.VideoCapture(0)  # or your video file


@app.get("/", response_class=HTMLResponse)
async def get(request: Request, current_user: Optional[User] = Depends(get_current_user)):
    if not current_user:
        return templates.TemplateResponse("login.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/video")
async def video_stream(websocket: WebSocket, token: Optional[str] = None):
    # Simple token check for WebSocket
    if token:
        user = decode_access_token(token)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    
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
                "model": "OnaVision v1.0",
                "fps": fps,
                "detections": "None"  # Replace with real detections later
            }
        }

        await websocket.send_json(payload)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response