async function updateHUD() {
    try {
        const response = await fetch('/state');
        const state = await response.json();

        // Update Status
        const statusText = document.getElementById('status-text');
        const container = document.getElementById('hud-container');
        
        statusText.innerText = `SYSTEM: ${state.status.toUpperCase()}`;
        
        // Remove old classes
        container.classList.remove('listening', 'speaking', 'recognizing');
        
        // Add new class based on status
        if (state.status !== 'idle') {
            container.classList.add(state.status);
        }

        // Update Transcript
        const transcriptText = document.getElementById('transcript-text');
        if (state.text) {
            transcriptText.innerText = state.text;
        }

        // Update Real Stats from Backend
        if (state.stats) {
            document.getElementById('cpu-stat').innerText = `CPU: ${state.stats.cpu}`;
            document.getElementById('ram-stat').innerText = `RAM: ${state.stats.ram}`;
            document.getElementById('core-temp').innerText = `CORE TEMP: ${state.stats.temp}`;
        }
        
        if (state.env) {
            document.getElementById('weather-stat').innerText = state.env.weather.toUpperCase();
            document.getElementById('time-stat').innerText = state.env.time;
        }

    } catch (error) {
        console.error("HUD Sync Error:", error);
    }
}

// Initial update and interval
updateHUD();
setInterval(updateHUD, 1000);

// Optional: Dynamic Particles could be added here or kept in particles.js
