const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
const statusText = document.getElementById('status-text');
const transcriptText = document.getElementById('transcript-text');
const container = document.body;

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particlesArray = [];
let status = 'idle';

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1;
        this.speedX = Math.random() * 3 - 1.5;
        this.speedY = Math.random() * 3 - 1.5;
        this.color = 'rgba(0, 210, 255, 0.8)';
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.size > 0.2) this.size -= 0.01;
        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }
    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function init() {
    for (let i = 0; i < 100; i++) {
        particlesArray.push(new Particle());
    }
}

function handleParticles() {
    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
        particlesArray[i].draw();

        if (particlesArray[i].size <= 0.3) {
            particlesArray.splice(i, 1);
            i--;
            particlesArray.push(new Particle());
        }
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Aesthetic connections
    ctx.strokeStyle = status === 'listening' ? 'rgba(255, 60, 0, 0.1)' :
        status === 'speaking' ? 'rgba(0, 255, 136, 0.1)' :
            'rgba(0, 210, 255, 0.1)';
    ctx.lineWidth = 1;
    for (let i = 0; i < particlesArray.length; i++) {
        for (let j = i; j < particlesArray.length; j++) {
            let dx = particlesArray[i].x - particlesArray[j].x;
            let dy = particlesArray[i].y - particlesArray[j].y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < 100) {
                ctx.beginPath();
                ctx.moveTo(particlesArray[i].x, particlesArray[i].y);
                ctx.lineTo(particlesArray[j].x, particlesArray[j].y);
                ctx.stroke();
            }
        }
    }

    handleParticles();
    requestAnimationFrame(animate);
}

// State polling
async function updateState() {
    try {
        const response = await fetch('/state');
        const data = await response.json();

        if (data.status !== status) {
            status = data.status;
            container.className = status;
            statusText.innerText = 'SYSTEM: ' + status.toUpperCase();

            // React particles to status
            if (status === 'listening') {
                particlesArray.forEach(p => p.color = 'rgba(255, 60, 0, 0.8)');
            } else if (status === 'speaking') {
                particlesArray.forEach(p => p.color = 'rgba(0, 255, 136, 0.8)');
            } else {
                particlesArray.forEach(p => p.color = 'rgba(0, 210, 255, 0.8)');
            }
        }

        transcriptText.innerText = data.text || '';
    } catch (err) {
        console.error('State sync failed', err);
    }
}

init();
animate();
setInterval(updateState, 500);

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
