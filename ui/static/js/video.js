const videoElement = document.getElementById("video");
const ws = new WebSocket(`ws://${window.location.host}/ws/video`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    videoElement.src = `data:image/jpeg;base64,${data.frame}`;
    document.getElementById("model").textContent = data.stats.model;
    document.getElementById("fps").textContent = data.stats.fps;
    document.getElementById("detections").textContent = data.stats.detections;
};

ws.onopen = () => console.log("✅ WebSocket connected");
ws.onerror = (e) => console.error("❌ WebSocket error", e);
ws.onclose = () => console.log("🔌 WebSocket closed");