/* ─── Transcript History (rolling 3 lines) ─────────────────── */
const transcriptHistory = [];

function pushTranscript(text) {
    if (!text || text === transcriptHistory[transcriptHistory.length - 1]) return;
    transcriptHistory.push(text);
    if (transcriptHistory.length > 3) transcriptHistory.shift();

    const lines = [
        document.getElementById('tlog-2'),
        document.getElementById('tlog-1'),
        document.getElementById('tlog-0'),
    ];

    const padded = ['', '', ...transcriptHistory].slice(-3);
    padded.forEach((msg, i) => { if (lines[i]) lines[i].textContent = msg; });
}

/* ─── Stat Bar Updater ─────────────────────────────────────── */
function setBar(barId, valId, rawValue) {
    const bar = document.getElementById(barId);
    const lbl = document.getElementById(valId);
    const num = parseFloat(rawValue) || 0;

    if (lbl) lbl.textContent = rawValue || '—';
    if (!bar) return;

    bar.style.width = Math.min(num, 100) + '%';
    bar.classList.remove('warn', 'danger');
    if (num >= 90) bar.classList.add('danger');
    else if (num >= 70) bar.classList.add('warn');
}

/* ─── Uptime Counter ───────────────────────────────────────── */
const startTime = Date.now();
function updateUptime() {
    const el = document.getElementById('uptime-display');
    if (!el) return;
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const h = String(Math.floor(elapsed / 3600)).padStart(2, '0');
    const m = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
    const s = String(elapsed % 60).padStart(2, '0');
    el.textContent = `${h}:${m}:${s}`;
}
setInterval(updateUptime, 1000);

/* ─── Date String ──────────────────────────────────────────── */
function updateDate() {
    const el = document.getElementById('date-stat');
    if (!el) return;
    const now = new Date();
    el.textContent = now.toLocaleDateString('en-GB', {
        weekday: 'short', day: '2-digit', month: 'short', year: 'numeric'
    }).toUpperCase();
}
updateDate();

/* ─── HUD State Sync ───────────────────────────────────────── */
let lastStatus = '';

async function updateHUD() {
    try {
        const res   = await fetch('/state');
        const state = await res.json();

        /* Status text + class */
        const container  = document.getElementById('hud-container');
        const statusText = document.getElementById('status-text');
        const headerStat = document.getElementById('header-status');
        const status     = (state.status || 'idle').toLowerCase();

        if (status !== lastStatus) {
            container.classList.remove('listening', 'speaking', 'recognizing');
            if (status !== 'idle') container.classList.add(status);
            lastStatus = status;
        }

        const label = status.charAt(0).toUpperCase() + status.slice(1);
        if (statusText) statusText.textContent = label.toUpperCase();
        if (headerStat) headerStat.textContent = status === 'idle' ? 'STANDBY' : label.toUpperCase();

        /* Transcript */
        if (state.text) pushTranscript(state.text);

        /* Stats */
        if (state.stats) {
            const cpuRaw  = String(state.stats.cpu  || '0%').replace('%', '');
            const ramRaw  = String(state.stats.ram  || '0%').replace('%', '');
            const tempRaw = state.stats.temp || '—';

            setBar('cpu-bar', 'cpu-val', state.stats.cpu  || '—');
            setBar('ram-bar', 'ram-val', state.stats.ram  || '—');

            const tempEl = document.getElementById('temp-val');
            if (tempEl) tempEl.textContent = tempRaw;

            const coreEl = document.getElementById('core-temp');
            if (coreEl) coreEl.textContent = `CORE TEMP: ${tempRaw}`;

            const batEl = document.getElementById('battery-val');
            if (batEl) batEl.textContent = state.stats.battery || '—';
        }

        /* Environment */
        if (state.env) {
            const timeEl    = document.getElementById('time-stat');
            const weatherEl = document.getElementById('weather-stat');
            if (timeEl)    timeEl.textContent    = state.env.time    || '—';
            if (weatherEl) weatherEl.textContent = (state.env.weather || 'UNKNOWN').toUpperCase();
        }

    } catch (err) {
        console.error('HUD Sync Error:', err);
    }
}

/* ─── Init ─────────────────────────────────────────────────── */
updateHUD();
setInterval(updateHUD, 1000);
