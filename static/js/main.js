class SpeedDetectionApp {
    constructor() {
        this.isRunning = false;
        this.init();
    }

    init() {
        this.initializeEventListeners();
        console.log("Speed Detection App Initialized");
    }

    initializeEventListeners() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startDetection());
        }
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopDetection());
        }
        
        const contactForm = document.getElementById('contactForm');
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => this.handleContactForm(e));
        }
    }

    async startDetection() {
        console.log("Start button clicked");
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        
        // Update UI immediately
        startBtn.disabled = true;
        startBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starting...';
        stopBtn.disabled = true;

        const videoSource = document.getElementById('videoSource') ? 
            document.getElementById('videoSource').value : 0;

        try {
            const response = await fetch('/start_detection', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ source: parseInt(videoSource) })
            });

            const data = await response.json();
            console.log("Start response:", data);
            
            if (data.status === 'success') {
                this.isRunning = true;
                this.updateUI();
                this.startVideoFeed();
                this.startSpeedUpdates();
                this.showAlert('Camera started successfully!', 'success');
            } else {
                this.showAlert('Error: ' + data.message, 'danger');
                this.resetButtons();
            }
        } catch (error) {
            console.error('Error starting detection:', error);
            this.showAlert('Failed to start camera', 'danger');
            this.resetButtons();
        }
    }

    async stopDetection() {
        console.log("Stop button clicked");
        
        try {
            const response = await fetch('/stop_detection', {
                method: 'POST'
            });

            const data = await response.json();
            console.log("Stop response:", data);
            
            this.isRunning = false;
            this.updateUI();
            this.showAlert('Camera stopped', 'info');
        } catch (error) {
            console.error('Error stopping detection:', error);
        }
    }

    resetButtons() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        
        if (startBtn) {
            startBtn.disabled = false;
            startBtn.innerHTML = '<i class="fas fa-play"></i> Start Detection';
        }
        if (stopBtn) {
            stopBtn.disabled = true;
        }
    }

    startVideoFeed() {
        const videoFeed = document.getElementById('videoFeed');
        const noVideo = document.getElementById('noVideo');
        
        if (videoFeed && noVideo) {
            videoFeed.style.display = 'block';
            noVideo.style.display = 'none';
            
            // Add timestamp to prevent caching
            videoFeed.src = '/video_feed?' + new Date().getTime();
            
            videoFeed.onload = () => {
                console.log("Video feed loaded successfully");
            };
            
            videoFeed.onerror = () => {
                console.error("Error loading video feed");
                this.showAlert('Error loading video feed', 'danger');
            };
        }
    }

    async startSpeedUpdates() {
        const updateSpeed = async () => {
            if (!this.isRunning) return;

            try {
                const response = await fetch('/get_speed_data');
                const data = await response.json();
                this.updateSpeedDisplay(data);
                setTimeout(updateSpeed, 1000);
            } catch (error) {
                console.error('Error updating speed:', error);
                setTimeout(updateSpeed, 2000);
            }
        };
        updateSpeed();
    }

    updateSpeedDisplay(data) {
        const currentSpeedElement = document.getElementById('currentSpeed');
        const avgSpeedElement = document.getElementById('avgSpeed');
        const maxSpeedElement = document.getElementById('maxSpeed');
        const statusElement = document.getElementById('detectionStatus');

        if (currentSpeedElement) {
            currentSpeedElement.textContent = data.current_speed.toFixed(2);
        }
        if (avgSpeedElement) avgSpeedElement.textContent = data.average_speed.toFixed(2) + ' m/s';
        if (maxSpeedElement) maxSpeedElement.textContent = data.max_speed.toFixed(2) + ' m/s';
        if (statusElement) {
            statusElement.textContent = data.status;
            statusElement.className = data.status === 'active' ? 'badge bg-success' : 
                                    data.status === 'monitoring' ? 'badge bg-warning' : 'badge bg-secondary';
        }
    }

    updateUI() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const videoFeed = document.getElementById('videoFeed');
        const noVideo = document.getElementById('noVideo');

        if (this.isRunning) {
            if (startBtn) {
                startBtn.disabled = true;
                startBtn.innerHTML = '<i class="fas fa-play"></i> Running...';
            }
            if (stopBtn) stopBtn.disabled = false;
        } else {
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.innerHTML = '<i class="fas fa-play"></i> Start Detection';
            }
            if (stopBtn) stopBtn.disabled = true;
            if (videoFeed) videoFeed.style.display = 'none';
            if (noVideo) noVideo.style.display = 'block';
        }
    }

    async handleContactForm(event) {
        event.preventDefault();
        // ... keep existing contact form code ...
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
        alertDiv.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
        document.body.appendChild(alertDiv);
        setTimeout(() => alertDiv.remove(), 5000);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    new SpeedDetectionApp();
});
// Date Time Display Function
function updateDateTime() {
    const now = new Date();
    
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    
    const dateTimeElement = document.getElementById('dateTime');
    if (dateTimeElement) {
        dateTimeElement.textContent = `${year}-${month}-${day} ${hours}:${minutes}`;
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Update date time
    updateDateTime();
    setInterval(updateDateTime, 60000);
    
    // Your existing app initialization
    new SpeedDetectionApp();
});