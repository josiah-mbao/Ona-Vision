// Only run checkAuth on / route
async function checkAuth() {
    if (window.location.pathname !== '/') {
        // We're on login or signup—no check needed
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

// Main function to initialize video stream
async function initVideoStream() {
    if (window.location.pathname !== '/') {
        return;
    }

    const isAuthenticated = await checkAuth();
    if (!isAuthenticated) return;

    const videoElement = document.getElementById("video");
    if (!videoElement) {
        console.warn("No video element found on this page. Skipping video stream.");
        return;
    }

    const token = document.cookie.split('; ')
        .find(row => row.startsWith('access_token='))
        ?.split('=')[1];

    if (!token) {
        console.warn("No access token cookie found. Redirecting to /login.");
        window.location.href = '/login';
        return;
    }

    const ws = new WebSocket(`ws://${window.location.host}/ws/video`);

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        videoElement.src = `data:image/jpeg;base64,${data.frame}`;
        document.getElementById("model").textContent = data.stats.model;
        document.getElementById("fps").textContent = data.stats.fps;
        document.getElementById("detections").textContent = data.stats.detections;
    };

    ws.onopen = () => console.log("✅ WebSocket connected");
    ws.onerror = (e) => {
        console.error("❌ WebSocket error", e);
    };
    ws.onclose = () => {
        console.log("🔌 WebSocket closed");
        setTimeout(initVideoStream, 2000);
    };
}

// Logout setup
function setupLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                await fetch('/auth/logout', {
                    method: 'POST',
                    credentials: 'include'
                });
                window.location.href = '/login';
            } catch (err) {
                console.error('Logout error:', err);
            }
        });
    }
}

// Run only on relevant pages
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/') {
        initVideoStream();
    }
    setupLogout();
});