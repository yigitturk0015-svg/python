<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Yıldız Avcısı - 2D Atari Oyunu</title>
    <!-- Eğlenceli ve okunaklı Google Fontları -->
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-top: #1a103c;
            --bg-bottom: #3b1d6e;
            --primary: #ffbe0b;
            --secondary: #fb5607;
            --accent: #3a86ff;
            --danger: #ff006e;
            --text-light: #ffffff;
            --panel-bg: rgba(25, 16, 60, 0.85);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            -webkit-user-select: none;
            font-family: 'Fredoka', sans-serif;
        }

        body {
            background: radial-gradient(circle at center, #2b1954 0%, #0f0826 100%);
            color: var(--text-light);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 10px;
        }

        /* Ana Oyun Konteyneri */
        .game-wrapper {
            width: 100%;
            max-width: 540px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            align-items: center;
        }

        /* Üst Bilgi Paneli (Skor, Seviye, Canlar) */
        .hud-bar {
            width: 100%;
            background: var(--panel-bg);
            border: 2px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 10px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(8px);
        }

        .hud-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .hud-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #b8b8ff;
        }

        .hud-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--primary);
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }

        .lives-container {
            display: flex;
            gap: 4px;
            font-size: 1.4rem;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
        }

        .heart-lost {
            opacity: 0.25;
            filter: grayscale(100%);
            transform: scale(0.85);
            transition: all 0.3s ease;
        }

        /* Oyun Alanı ve Canvas Çerçevesi */
        .canvas-container {
            position: relative;
            width: 100%;
            height: 62vh;
            min-height: 380px;
            max-height: 580px;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), 0 0 0 4px rgba(255, 190, 11, 0.3);
            background: linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
            touch-action: none; /* Dokunmatik kaydırmayı engelle */
        }

        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }

        /* Arayüz Katmanları (Başlangıç ve Oyun Bitti Ekranları) */
        .overlay {
            position: absolute;
            inset: 0;
            background: rgba(18, 10, 44, 0.88);
            backdrop-filter: blur(6px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 24px;
            z-index: 10;
            transition: opacity 0.3s ease;
        }

        .hidden {
            display: none !important;
        }

        .game-title {
            font-size: 2.4rem;
            font-weight: 700;
            background: linear-gradient(45deg, #ffbe0b, #fb5607, #ff006e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));
        }

        .game-subtitle {
            font-size: 1rem;
            color: #e0e0ff;
            margin-bottom: 20px;
            line-height: 1.5;
            max-width: 360px;
        }

        /* Puan Rehberi Kartı */
        .legend-box {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 12px 20px;
            margin-bottom: 24px;
            display: flex;
            gap: 16px;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .legend-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.85rem;
            gap: 4px;
        }

        .legend-icon {
            font-size: 1.6rem;
        }

        /* Atari Butonları */
        .arcade-btn {
            background: linear-gradient(180deg, #ffbe0b 0%, #fb5607 100%);
            color: #fff;
            border: none;
            border-radius: 50px;
            padding: 14px 36px;
            font-size: 1.25rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 6px 0 #b83b00, 0 12px 20px rgba(251, 86, 7, 0.4);
            transition: transform 0.1s, box-shadow 0.1s;
            text-shadow: 0 2px 3px rgba(0,0,0,0.3);
            letter-spacing: 0.5px;
        }

        .arcade-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 0 #b83b00, 0 15px 25px rgba(251, 86, 7, 0.5);
        }

        .arcade-btn:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0 #b83b00, 0 5px 10px rgba(251, 86, 7, 0.4);
        }

        /* Alt Kontrol Çubuğu (Ses ve Mobil Yön Tuşları) */
        .controls-bar {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }

        .touch-btn {
            flex: 1;
            background: rgba(255, 255, 255, 0.12);
            border: 2px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 14px;
            border-radius: 16px;
            font-size: 1.4rem;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.15s, transform 0.1s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        .touch-btn:active, .touch-btn.active {
            background: rgba(255, 190, 11, 0.4);
            border-color: var(--primary);
            transform: scale(0.96);
        }

        .sound-btn {
            background: rgba(255, 255, 255, 0.12);
            border: 2px solid rgba(255, 255, 255, 0.2);
            color: white;
            width: 54px;
            height: 54px;
            border-radius: 16px;
            font-size: 1.3rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }

        .sound-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        /* Skor Özeti */
        .score-summary {
            background: rgba(0, 0, 0, 0.35);
            padding: 16px 28px;
            border-radius: 18px;
            margin-bottom: 22px;
            border: 1px solid rgba(255, 190, 11, 0.3);
        }

        .score-summary p {
            font-size: 1.1rem;
            margin: 6px 0;
        }

        .highlight-score {
            color: var(--primary);
            font-size: 1.5rem;
            font-weight: 700;
        }

        @media (max-width: 480px) {
            .game-title { font-size: 1.9rem; }
            .hud-value { font-size: 1.2rem; }
            .canvas-container { height: 58vh; }
        }
    </style>
</head>
<body>

<div class="game-wrapper">
    <!-- Üst Bilgi Çubuğu -->
    <div class="hud-bar">
        <div class="hud-item">
            <span class="hud-label">Skor</span>
            <span class="hud-value" id="scoreDisplay">0</span>
        </div>
        <div class="hud-item">
            <span class="hud-label">Seviye</span>
            <span class="hud-value" id="levelDisplay">1</span>
        </div>
        <div class="hud-item">
            <span class="hud-label">Rekor</span>
            <span class="hud-value" id="highScoreDisplay">0</span>
        </div>
        <div class="hud-item">
            <span class="hud-label">Canlar</span>
            <div class="lives-container" id="livesDisplay">
                <span>❤️</span><span>❤️</span><span>❤️</span>
            </div>
        </div>
    </div>

    <!-- Oyun Alanı -->
    <div class="canvas-container" id="canvasContainer">
        <canvas id="gameCanvas"></canvas>

        <!-- Başlangıç Ekranı -->
        <div class="overlay" id="startScreen">
            <h1 class="game-title">⭐ Yıldız Avcısı</h1>
            <p class="game-subtitle">Gökyüzünden düşen yıldızları ve altın elmaları yakala, bombalardan kaç!</p>
            
            <div class="legend-box">
                <div class="legend-item">
                    <span class="legend-icon">⭐</span>
                    <span>+10 Puan</span>
                </div>
                <div class="legend-item">
                    <span class="legend-icon">🍎</span>
                    <span>+30 Puan</span>
                </div>
                <div class="legend-item">
                    <span class="legend-icon">💣</span>
                    <span>-1 Can</span>
                </div>
            </div>

            <button class="arcade-btn" id="startBtn">OYUNA BAŞLA</button>
        </div>

        <!-- Oyun Bitti Ekranı -->
        <div class="overlay hidden" id="gameOverScreen">
            <h1 class="game-title">Oyun Bitti!</h1>
            <div class="score-summary">
                <p>Toplam Skorun: <span class="highlight-score" id="finalScore">0</span></p>
                <p>Ulaşılan Seviye: <strong id="finalLevel">1</strong></p>
                <p>En Yüksek Skor: <strong id="finalHighScore">0</strong></p>
            </div>
            <button class="arcade-btn" id="restartBtn">TEKRAR OYNA</button>
        </div>
    </div>

    <!-- Alt Kontrol Düğmeleri -->
    <div class="controls-bar">
        <button class="touch-btn" id="leftBtn" aria-label="Sola Git">⬅️ SOL</button>
        <button class="sound-btn" id="soundToggleBtn" title="Sesi Aç/Kapat">🔊</button>
        <button class="touch-btn" id="rightBtn" aria-label="Sağa Git">SAĞ ➡️</button>
    </div>
</div>

<script>
/**
 * YILDIZ AVCISI - 2D ATARİ OYUNU
 * Tek dosya içerisinde Web Audio API ses sentezi, parçacık efektleri ve responsive oyun motoru.
 */

// --- 1. SES MOTORU (Web Audio API) ---
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.muted = false;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    toggleMute() {
        this.muted = !this.muted;
        return this.muted;
    }

    // Yıldız yakalama sesi (Neşeli çınlama)
    playStar() {
        if (this.muted || !this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, now); // D5
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.12); // A5
        
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.start(now);
        osc.stop(now + 0.15);
    }

    // Altın Elma yakalama sesi (Çift harmonik)
    playApple() {
        if (this.muted || !this.ctx) return;
        const now = this.ctx.currentTime;
        const notes = [523.25, 659.25, 1046.50]; // C5, E5, C6
        
        notes.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now + idx * 0.05);
            
            gain.gain.setValueAtTime(0.22, now + idx * 0.05);
            gain.gain.exponentialRampToValueAtTime(0.01, now + idx * 0.05 + 0.2);
            
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + idx * 0.05);
            osc.stop(now + idx * 0.05 + 0.2);
        });
    }

    // Bomba patlama sesi (Bas gürültü ve düşüş)
    playBomb() {
        if (this.muted || !this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(160, now);
        osc.frequency.exponentialRampToValueAtTime(35, now + 0.35);
        
        gain.gain.setValueAtTime(0.35, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.38);
        
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.start(now);
        osc.stop(now + 0.38);
    }

    // Seviye atlama melodisi
    playLevelUp() {
        if (this.muted || !this.ctx) return;
        const now = this.ctx.currentTime;
        const melody = [440, 554.37, 659.25, 880]; // A4, C#5, E5, A5
        
        melody.forEach((freq, i) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + i * 0.08);
            
            gain.gain.setValueAtTime(0.2, now + i * 0.08);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.08 + 0.25);
            
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + i * 0.08);
            osc.stop(now + i * 0.08 + 0.25);
        });
    }

    // Oyun Bitti melodisi
    playGameOver() {
        if (this.muted || !this.ctx) return;
        const now = this.ctx.currentTime;
        const notes = [392.00, 349.23, 329.63, 261.63]; // G4, F4, E4, C4
        
        notes.forEach((freq, i) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now + i * 0.16);
            
            gain.gain.setValueAtTime(0.25, now + i * 0.16);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.16 + 0.3);
            
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + i * 0.16);
            osc.stop(now + i * 0.16 + 0.3);
        });
    }
}

// --- 2. OYUN DEĞİŞKENLERİ VE DOM REFERANSLARI ---
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvasContainer');

const scoreDisplay = document.getElementById('scoreDisplay');
const levelDisplay = document.getElementById('levelDisplay');
const highScoreDisplay = document.getElementById('highScoreDisplay');
const livesDisplay = document.getElementById('livesDisplay');

const startScreen = document.getElementById('startScreen');
const gameOverScreen = document.getElementById('gameOverScreen');
const startBtn = document.getElementById('startBtn');
const restartBtn = document.getElementById('restartBtn');
const soundToggleBtn = document.getElementById('soundToggleBtn');
const leftBtn = document.getElementById('leftBtn');
const rightBtn = document.getElementById('rightBtn');

const sound = new SoundEngine();

let gameState = 'START'; // START, PLAYING, GAMEOVER
let score = 0;
let level = 1;
let lives = 3;
let highScore = parseInt(localStorage.getItem('yildizAvcisiRekor')) || 0;
highScoreDisplay.textContent = highScore;

let animationId = null;
let lastTime = 0;
let spawnTimer = 0;
let screenShake = 0;
let levelUpBannerTimer = 0;

// Arka plan yıldızları (Dekoratif)
let bgStars = [];

// Düşen nesneler, parçacıklar ve yüzen skor yazıları
let items = [];
let particles = [];
let floatingTexts = [];

// Oyuncu (Sevimli Sepet Karakteri)
const player = {
    x: 0,
    y: 0,
    width: 84,
    height: 48,
    speed: 480, // piksel/saniye
    vx: 0,
    bounce: 0,
    expression: 'happy' // 'happy', 'catch', 'hurt'
};

// Kontrol durumları
const keys = {
    left: false,
    right: false
};

// --- 3. EKRAN BOYUTLANDIRMA (RESPONSIVE CANVAS) ---
function resizeCanvas() {
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    // Oyuncuyu alt ortaya konumlandır
    player.width = Math.max(70, Math.min(95, canvas.width * 0.18));
    player.height = player.width * 0.56;
    player.y = canvas.height - player.height - 16;
    if (player.x === 0 || player.x > canvas.width - player.width) {
        player.x = (canvas.width - player.width) / 2;
    }

    // Arka plan yıldızlarını oluştur
    bgStars = [];
    for (let i = 0; i < 45; i++) {
        bgStars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2.2 + 0.8,
            alpha: Math.random() * 0.7 + 0.2,
            twinkleSpeed: Math.random() * 2 + 1
        });
    }
}

window.addEventListener('resize', resizeCanvas);

// --- 4. OYUN YÖNETİM FONKSİYONLARI ---
function startGame() {
    sound.init();
    score = 0;
    level = 1;
    lives = 3;
    items = [];
    particles = [];
    floatingTexts = [];
    spawnTimer = 0;
    screenShake = 0;
    levelUpBannerTimer = 0;
    player.expression = 'happy';
    player.x = (canvas.width - player.width) / 2;

    updateHUD();
    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    gameState = 'PLAYING';

    lastTime = performance.now();
    if (animationId) cancelAnimationFrame(animationId);
    animationId = requestAnimationFrame(gameLoop);
}

function endGame() {
    gameState = 'GAMEOVER';
    sound.playGameOver();

    if (score > highScore) {
        highScore = score;
        localStorage.setItem('yildizAvcisiRekor', highScore);
        highScoreDisplay.textContent = highScore;
    }

    document.getElementById('finalScore').textContent = score;
    document.getElementById('finalLevel').textContent = level;
    document.getElementById('finalHighScore').textContent = highScore;
    gameOverScreen.classList.remove('hidden');
}

function updateHUD() {
    scoreDisplay.textContent = score;
    levelDisplay.textContent = level;
    highScoreDisplay.textContent = Math.max(score, highScore);

    // Can ikonlarını güncelle
    const hearts = livesDisplay.querySelectorAll('span');
    hearts.forEach((heart, index) => {
        if (index < lives) {
            heart.classList.remove('heart-lost');
        } else {
            heart.classList.add('heart-lost');
        }
    });
}

// --- 5. NESNE OLUŞTURMA VE EFEKTLER ---
function spawnItem() {
    const rand = Math.random();
    let type = 'star'; // %65 Yıldız
    if (rand > 0.82) {
        type = 'apple'; // %18 Altın Elma
    } else if (rand > 0.62) {
        type = 'bomb'; // %20 Bomba
    }

    // Seviye arttıkça bomba olasılığı hafifçe artar (en fazla %35)
    const bombChance = Math.min(0.35, 0.20 + (level - 1) * 0.025);
    if (rand < bombChance) {
        type = 'bomb';
    } else if (rand < bombChance + 0.18) {
        type = 'apple';
    } else {
        type = 'star';
    }

    const radius = type === 'apple' ? 20 : 19;
    const baseSpeed = 190 + (level - 1) * 38; // Her seviyede hızlanma
    const speedVariation = Math.random() * 70;

    items.push({
        x: radius + Math.random() * (canvas.width - radius * 2),
        y: -radius * 2,
        radius: radius,
        type: type,
        speed: baseSpeed + speedVariation,
        rotation: Math.random() * Math.PI * 2,
        rotSpeed: (Math.random() - 0.5) * 4
    });
}

function createParticles(x, y, color, count = 14) {
    for (let i = 0; i < count; i++) {
        const angle = (Math.PI * 2 * i) / count + Math.random() * 0.4;
        const speed = Math.random() * 180 + 60;
        particles.push({
            x: x,
            y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            size: Math.random() * 5 + 3,
            color: color,
            life: 1.0
        });
    }
}

function addFloatingText(x, y, text, color) {
    floatingTexts.push({
        x: x,
        y: y,
        text: text,
        color: color,
        life: 1.0
    });
}

// --- 6. GÜNCELLEME MANTIĞI (UPDATE) ---
function update(dt) {
    // Ekran titremesi azaltma
    if (screenShake > 0) {
        screenShake = Math.max(0, screenShake - dt * 30);
    }

    // Seviye atlama yazısı sayacı
    if (levelUpBannerTimer > 0) {
        levelUpBannerTimer = Math.max(0, levelUpBannerTimer - dt);
    }

    // Sepet zıplama animasyonu sönümleme
    if (player.bounce > 0) {
        player.bounce = Math.max(0, player.bounce - dt * 25);
    }

    // Klavye / Tuş hareketleri
    player.vx = 0;
    if (keys.left) player.vx -= player.speed;
    if (keys.right) player.vx += player.speed;

    player.x += player.vx * dt;

    // Ekran sınırları içinde tutma
    if (player.x < 6) player.x = 6;
    if (player.x + player.width > canvas.width - 6) {
        player.x = canvas.width - player.width - 6;
    }

    // Yeni nesne oluşturma zamanlayıcısı (seviyeye göre hızlanır)
    const spawnInterval = Math.max(0.32, 0.95 - (level - 1) * 0.08);
    spawnTimer += dt;
    if (spawnTimer >= spawnInterval) {
        spawnItem();
        spawnTimer = 0;
    }

    // Düşen nesneleri güncelle
    for (let i = items.length - 1; i >= 0; i--) {
        const item = items[i];
        item.y += item.speed * dt;
        item.rotation += item.rotSpeed * dt;

        // Çarpışma Kontrolü (Daire - Dikdörtgen yaklaşımı)
        const closestX = Math.max(player.x, Math.min(item.x, player.x + player.width));
        const closestY = Math.max(player.y, Math.min(item.y, player.y + player.height));
        const dx = item.x - closestX;
        const dy = item.y - closestY;
        const distanceSquared = dx * dx + dy * dy;

        if (distanceSquared < (item.radius * 0.9) * (item.radius * 0.9)) {
            // Yakalandı!
            if (item.type === 'star') {
                score += 10;
                sound.playStar();
                createParticles(item.x, item.y, '#ffbe0b', 12);
                addFloatingText(item.x, item.y - 10, '+10', '#ffbe0b');
                player.bounce = 6;
                player.expression = 'catch';
            } else if (item.type === 'apple') {
                score += 30;
                sound.playApple();
                createParticles(item.x, item.y, '#ff4d6d', 18);
                addFloatingText(item.x, item.y - 10, '+30 🍎', '#ff758f');
                player.bounce = 9;
                player.expression = 'catch';
            } else if (item.type === 'bomb') {
                lives--;
                sound.playBomb();
                createParticles(item.x, item.y, '#ff006e', 24);
                addFloatingText(item.x, item.y - 10, 'BOM! -1 ❤️', '#ff006e');
                screenShake = 12;
                player.expression = 'hurt';
            }

            // İfade sıfırlama zamanlayıcısı
            setTimeout(() => {
                if (gameState === 'PLAYING') player.expression = 'happy';
            }, 350);

            // Seviye kontrolü (Her 150 puanda bir yeni seviye)
            const newLevel = Math.floor(score / 150) + 1;
            if (newLevel > level) {
                level = newLevel;
                sound.playLevelUp();
                levelUpBannerTimer = 1.8;
            }

            updateHUD();
            items.splice(i, 1);

            if (lives <= 0) {
                endGame();
                return;
            }
            continue;
        }

        // Ekrandan çıkan nesneleri temizle
        if (item.y - item.radius > canvas.height) {
            items.splice(i, 1);
        }
    }

    // Parçacıkları güncelle
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.vy += 220 * dt; // Hafif yerçekimi
        p.life -= dt * 2.2;
        if (p.life <= 0) particles.splice(i, 1);
    }

    // Yüzen skor yazılarını güncelle
    for (let i = floatingTexts.length - 1; i >= 0; i--) {
        const ft = floatingTexts[i];
        ft.y -= 45 * dt;
        ft.life -= dt * 1.4;
        if (ft.life <= 0) floatingTexts.splice(i, 1);
    }
}

// --- 7. ÇİZİM FONKSİYONLARI (RENDER) ---
function draw() {
    ctx.save();

    // Bomba patladığında ekran titremesi uygula
    if (screenShake > 0) {
        const shakeX = (Math.random() - 0.5) * screenShake;
        const shakeY = (Math.random() - 0.5) * screenShake;
        ctx.translate(shakeX, shakeY);
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Arka Plan Parlayan Yıldızlar
    const now = performance.now() / 1000;
    bgStars.forEach(s => {
        const alpha = s.alpha * (0.6 + 0.4 * Math.sin(now * s.twinkleSpeed));
        ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
        ctx.fill();
    });

    // 2. Zemin Çizgisi (Yumuşak ışıklı şerit)
    const groundGrad = ctx.createLinearGradient(0, canvas.height - 20, 0, canvas.height);
    groundGrad.addColorStop(0, 'rgba(255, 190, 11, 0)');
    groundGrad.addColorStop(1, 'rgba(255, 190, 11, 0.22)');
    ctx.fillStyle = groundGrad;
    ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

    // 3. Sevimli Sepet Karakterini Çiz
    drawPlayer();

    // 4. Düşen Nesneleri Çiz
    items.forEach(item => {
        ctx.save();
        ctx.translate(item.x, item.y);
        ctx.rotate(item.rotation);

        if (item.type === 'star') {
            drawStarShape(0, 0, 5, item.radius, item.radius * 0.48);
        } else if (item.type === 'apple') {
            drawGoldenApple(0, 0, item.radius);
        } else if (item.type === 'bomb') {
            drawBomb(0, 0, item.radius);
        }
        ctx.restore();
    });

    // 5. Parçacık Efektleri
    particles.forEach(p => {
        ctx.save();
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    });

    // 6. Yüzen Puan Yazıları
    floatingTexts.forEach(ft => {
        ctx.save();
        ctx.globalAlpha = Math.max(0, ft.life);
        ctx.font = 'bold 20px Fredoka, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillStyle = ft.color;
        ctx.shadowColor = 'rgba(0,0,0,0.7)';
        ctx.shadowBlur = 4;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.restore();
    });

    // 7. Seviye Atlama Bildirimi
    if (levelUpBannerTimer > 0) {
        ctx.save();
        ctx.globalAlpha = Math.min(1, levelUpBannerTimer);
        ctx.font = 'bold 30px Fredoka, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillStyle = '#ffbe0b';
        ctx.shadowColor = '#fb5607';
        ctx.shadowBlur = 12;
        ctx.fillText(`🚀 SEVİYE ${level}!`, canvas.width / 2, canvas.height * 0.35);
        ctx.restore();
    }

    ctx.restore();
}

// Sevimli Yüzlü Sepet Çizimi
function drawPlayer() {
    const px = player.x;
    const py = player.y + player.bounce;
    const pw = player.width;
    const ph = player.height;

    ctx.save();

    // Sepet Gövdesi (Yamuk formda yuvarlatılmış sepet)
    const grad = ctx.createLinearGradient(px, py, px, py + ph);
    grad.addColorStop(0, '#ff9f1c');
    grad.addColorStop(1, '#e76f51');

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(px + 4, py + 8);
    ctx.lineTo(px + pw - 4, py + 8);
    ctx.lineTo(px + pw - 14, py + ph);
    ctx.quadraticCurveTo(px + pw / 2, py + ph + 5, px + 14, py + ph);
    ctx.closePath();
    ctx.fill();

    // Sepet Üst Kenarlığı (Ağız kısmı)
    ctx.fillStyle = '#ffbf69';
    ctx.beginPath();
    ctx.roundRect(px, py, pw, 12, 8);
    ctx.fill();
    ctx.strokeStyle = '#d65a31';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Sevimli Gözler ve Ağız
    const centerX = px + pw / 2;
    const eyeY = py + ph * 0.54;
    const eyeOffset = pw * 0.18;

    if (player.expression === 'hurt') {
        // Çarpı gözler (X X)
        ctx.strokeStyle = '#2b1954';
        ctx.lineWidth = 2.5;
        [-eyeOffset, eyeOffset].forEach(offset => {
            ctx.beginPath();
            ctx.moveTo(centerX + offset - 4, eyeY - 4);
            ctx.lineTo(centerX + offset + 4, eyeY + 4);
            ctx.moveTo(centerX + offset + 4, eyeY - 4);
            ctx.lineTo(centerX + offset - 4, eyeY + 4);
            ctx.stroke();
        });
    } else {
        // Parlak sevimli gözler
        ctx.fillStyle = '#1a103c';
        ctx.beginPath();
        ctx.arc(centerX - eyeOffset, eyeY, 4.5, 0, Math.PI * 2);
        ctx.arc(centerX + eyeOffset, eyeY, 4.5, 0, Math.PI * 2);
        ctx.fill();

        // Göz parıltısı
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(centerX - eyeOffset - 1.5, eyeY - 1.5, 1.6, 0, Math.PI * 2);
        ctx.arc(centerX + eyeOffset - 1.5, eyeY - 1.5, 1.6, 0, Math.PI * 2);
        ctx.fill();
    }

    // Yanak pembelikleri
    ctx.fillStyle = 'rgba(255, 0, 110, 0.35)';
    ctx.beginPath();
    ctx.arc(centerX - eyeOffset - 6, eyeY + 5, 4, 0, Math.PI * 2);
    ctx.arc(centerX + eyeOffset + 6, eyeY + 5, 4, 0, Math.PI * 2);
    ctx.fill();

    // Gülümseme
    ctx.strokeStyle = '#1a103c';
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    if (player.expression === 'catch') {
        ctx.arc(centerX, eyeY + 4, 6, 0, Math.PI, false);
        ctx.fillStyle = '#ff006e';
        ctx.fill();
    } else if (player.expression === 'hurt') {
        ctx.arc(centerX, eyeY + 10, 5, Math.PI, 0, false);
    } else {
        ctx.arc(centerX, eyeY + 3, 5, 0.1 * Math.PI, 0.9 * Math.PI, false);
    }
    ctx.stroke();

    ctx.restore();
}

// Parlak Altın Yıldız Çizimi
function drawStarShape(cx, cy, spikes, outerRadius, innerRadius) {
    let rot = (Math.PI / 2) * 3;
    let x = cx;
    let y = cy;
    const step = Math.PI / spikes;

    ctx.shadowColor = '#ffbe0b';
    ctx.shadowBlur = 12;
    ctx.fillStyle = '#ffd166';
    ctx.strokeStyle = '#f77f00';
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(cx, cy - outerRadius);
    for (let i = 0; i < spikes; i++) {
        x = cx + Math.cos(rot) * outerRadius;
        y = cy + Math.sin(rot) * outerRadius;
        ctx.lineTo(x, y);
        rot += step;

        x = cx + Math.cos(rot) * innerRadius;
        y = cy + Math.sin(rot) * innerRadius;
        ctx.lineTo(x, y);
        rot += step;
    }
    ctx.lineTo(cx, cy - outerRadius);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
}

// Parlayan Altın Elma Çizimi
function drawGoldenApple(cx, cy, r) {
    ctx.shadowColor = '#ff4d6d';
    ctx.shadowBlur = 14;

    // Elma gövdesi
    const grad = ctx.createRadialGradient(cx - 4, cy - 4, 2, cx, cy, r);
    grad.addColorStop(0, '#ffe66d');
    grad.addColorStop(0.6, '#ff9f1c');
    grad.addColorStop(1, '#ff4d6d');

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(cx, cy + 2, r * 0.88, 0, Math.PI * 2);
    ctx.fill();

    // Sap ve Yaprak
    ctx.shadowBlur = 0;
    ctx.strokeStyle = '#6f4e37';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(cx, cy - r * 0.7);
    ctx.lineTo(cx + 2, cy - r * 1.15);
    ctx.stroke();

    ctx.fillStyle = '#06d6a0';
    ctx.beginPath();
    ctx.ellipse(cx + 7, cy - r * 0.95, 6, 3.5, -0.4, 0, Math.PI * 2);
    ctx.fill();
}

// Tehlikeli Bomba Çizimi
function drawBomb(cx, cy, r) {
    // Bomba gövdesi
    const grad = ctx.createRadialGradient(cx - 5, cy - 5, 2, cx, cy, r);
    grad.addColorStop(0, '#4a4e69');
    grad.addColorStop(1, '#14141f');

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(cx, cy + 2, r * 0.88, 0, Math.PI * 2);
    ctx.fill();

    // Fitil başlığı
    ctx.fillStyle = '#9a8c98';
    ctx.fillRect(cx - 4, cy - r * 0.95, 8, 5);

    // Kıvılcım saçan fitil
    ctx.strokeStyle = '#f4a261';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(cx, cy - r * 0.95);
    ctx.quadraticCurveTo(cx + 6, cy - r * 1.3, cx + 10, cy - r * 1.15);
    ctx.stroke();

    // Yanıp sönen ateş kıvılcımı
    ctx.fillStyle = Math.random() > 0.5 ? '#ff006e' : '#ffbe0b';
    ctx.beginPath();
    ctx.arc(cx + 10, cy - r * 1.15, 4.5, 0, Math.PI * 2);
    ctx.fill();
}

// --- 8. ANA OYUN DÖNGÜSÜ ---
function gameLoop(timestamp) {
    if (gameState !== 'PLAYING') return;

    const dt = Math.min((timestamp - lastTime) / 1000, 0.1); // Sekme değişiminde sıçramayı önle
    lastTime = timestamp;

    update(dt);
    draw();

    animationId = requestAnimationFrame(gameLoop);
}

// --- 9. KONTROLLER (KLAVYE, FARE VE DOKUNMATİK) ---
window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
        keys.left = true;
        leftBtn.classList.add('active');
    }
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
        keys.right = true;
        rightBtn.classList.add('active');
    }
});

window.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
        keys.left = false;
        leftBtn.classList.remove('active');
    }
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
        keys.right = false;
        rightBtn.classList.remove('active');
    }
});

// Ekran üzerindeki dokunmatik butonlar
const bindTouchButton = (btn, dir) => {
    const press = (e) => {
        e.preventDefault();
        keys[dir] = true;
        btn.classList.add('active');
    };
    const release = (e) => {
        e.preventDefault();
        keys[dir] = false;
        btn.classList.remove('active');
    };
    btn.addEventListener('mousedown', press);
    btn.addEventListener('mouseup', release);
    btn.addEventListener('mouseleave', release);
    btn.addEventListener('touchstart', press, { passive: false });
    btn.addEventListener('touchend', release, { passive: false });
};

bindTouchButton(leftBtn, 'left');
bindTouchButton(rightBtn, 'right');

// Canvas üzerinde doğrudan fare veya parmakla sürükleme kontrolü
function movePlayerToPointer(clientX) {
    if (gameState !== 'PLAYING') return;
    const rect = canvas.getBoundingClientRect();
    const pointerX = clientX - rect.left;
    player.x = pointerX - player.width / 2;

    if (player.x < 6) player.x = 6;
    if (player.x + player.width > canvas.width - 6) {
        player.x = canvas.width - player.width - 6;
    }
}

canvas.addEventListener('mousemove', (e) => {
    if (e.buttons === 1) movePlayerToPointer(e.clientX);
});

canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    if (e.touches.length > 0) {
        movePlayerToPointer(e.touches[0].clientX);
    }
}, { passive: false });

canvas.addEventListener('touchstart', (e) => {
    if (e.touches.length > 0) {
        movePlayerToPointer(e.touches[0].clientX);
    }
}, { passive: true });

// Buton Olayları
startBtn.addEventListener('click', startGame);
restartBtn.addEventListener('click', startGame);

soundToggleBtn.addEventListener('click', () => {
    sound.init();
    const isMuted = sound.toggleMute();
    soundToggleBtn.textContent = isMuted ? '🔇' : '🔊';
});

// Sayfa yüklendiğinde canvas boyutunu ayarla ve ilk sahneyi çiz
window.onload = () => {
    resizeCanvas();
    draw();
};
</script>
</body>
</html>