let ws = null; // global reference to the WebSocket

async function checkAuth() {
    if (window.location.pathname !== '/') {
        return true;
    }
    try {
        const response = await fetch('/auth/me', {
            credentials: 'include'
        });
        if (!response.ok) {
            console.warn("Auth check failed. Redirecting to /login.");
            window.location.href = '/login';
            return false;
        }
        return true;
    } catch (err) {
        console.error('Auth check failed:', err);
        window.location.href = '/login';
        return false;
    }
}

async function initVideoStream() {
    if (window.location.pathname !== '/') {
        return;
    }

    // Don't open multiple connections
    if (ws && ws.readyState === WebSocket.OPEN) {
        console.warn("WebSocket already open.");
        return;
    }

    const isAuthenticated = await checkAuth();
    if (!isAuthenticated) return;

    const videoElement = document.getElementById("video");
    if (!videoElement) {
        console.warn("No video element found on this page.");
        return;
    }

    ws = new WebSocket(`ws://${window.location.host}/ws/video`);
    
    ws.onopen = () => console.log("✅ WebSocket connected");
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        videoElement.src = `data:image/jpeg;base64,${data.frame}`;
        document.getElementById("model").textContent = data.stats.model;
        document.getElementById("fps").textContent = data.stats.fps;
        document.getElementById("detections").textContent = data.stats.detections;
    };

    ws.onerror = (e) => {
        console.error("❌ WebSocket error", e);
    };

    ws.onclose = () => {
        console.log("🔌 WebSocket closed");
    };
}

function setupLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                if (ws) {
                    ws.close();
                    ws = null;
                }
                await fetch('/logout', {
                    method: 'GET',
                    credentials: 'include'
                });
                window.location.href = '/login';
            } catch (err) {
                console.error('Logout error:', err);
            }
        });
    }
}

// Optional toggle button logic
function setupToggleStream() {
    const toggleBtn = document.getElementById('toggleStreamBtn');
    if (!toggleBtn) return;

    let isStreaming = true;

    toggleBtn.addEventListener('click', () => {
        if (isStreaming) {
            ws?.close();
            isStreaming = false;
            toggleBtn.textContent = 'Start Stream';
        } else {
            initVideoStream();
            isStreaming = true;
            toggleBtn.textContent = 'Stop Stream';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/') {
        initVideoStream();
    }
    setupLogout();
    setupToggleStream();
});