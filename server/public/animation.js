const background = document.getElementById("flower");

let backgroundWidth = background.width = background.clientWidth;
let backgroundHeight = background.height = background.clientHeight;

const backgroundCtx = background.getContext("2d");

const petals = {
    speed: 1,
    size: 100,
    radius: 70,
    elements: [],
    x: 0,
    y: 0
};

const petal = (x, y, z, color) => ({
    homeX: x,
    homeY: y,
    homeZ: z,
    phase: Math.random() * Math.PI * 2,
    color
});

function colorFor(index, n) {
    const hue = (index * 360) / n;
    return `hsl(${hue} 100% 50% / 0.4)`;
}

function initPetals(count) {
    petals.x = backgroundWidth / 2;
    petals.y = backgroundHeight / 2;

    petals.elements = [];

    for (let i = 0; i < count; i++) {
        const phi = Math.random() * Math.PI * 2;

        const z = Math.random() * 2 - 1;
        const r = Math.sqrt(1 - z * z);

        const x = r * Math.cos(phi);
        const y = r * Math.sin(phi);

        petals.elements.push(
            petal(x, y, z, colorFor(i, count))
        );
    }
}

function drawAurora(t) {
    backgroundCtx.save();
    backgroundCtx.globalCompositeOperation = "screen";
    for (let i = 0; i < 3; i++) {
        const gradient = backgroundCtx.createLinearGradient(
            0,
            0,
            backgroundWidth,
            backgroundHeight
        );

        const hue = (performance.now() * 0.01) % 360;

        gradient.addColorStop(0, `hsla(${hue}, 100%, 60%, 0.001)`);
        gradient.addColorStop(0.5, `hsla(${hue}, 100%, 60%, 0.2)`);
        gradient.addColorStop(1, `hsla(${hue}, 100%, 60%, 0.001)`);

        backgroundCtx.fillStyle = gradient;

        backgroundCtx.beginPath();

        backgroundCtx.moveTo(0, backgroundHeight);

        for (let x = 0; x <= backgroundWidth; x += 20) {
            const y =
                backgroundHeight * 0.3 +
                Math.sin(x * 0.003 + t + i) * 60 +
                Math.sin(x * 0.001 + t * 0.5) * 40;

            backgroundCtx.lineTo(x, y);
        }

        backgroundCtx.lineTo(backgroundWidth, backgroundHeight);
        backgroundCtx.closePath();

        backgroundCtx.fill();
    }

    backgroundCtx.restore();
}

function draw() {
    backgroundCtx.clearRect(0, 0, backgroundWidth, backgroundHeight);

    const t = performance.now() * 0.001 * petals.speed;

    drawAurora(t);

    const drawPetals = petals.elements.map(e => {
        const angle = t * 0.5;

        const x =
            e.homeX * Math.cos(angle) -
            e.homeZ * Math.sin(angle);

        const z =
            e.homeX * Math.sin(angle) +
            e.homeZ * Math.cos(angle);

        const y =
            e.homeY +
            Math.sin(t + e.phase) * 0.05;

        return {
            color: e.color,
            drawX: x,
            drawY: y,
            drawZ: z
        };
    });

    drawPetals.sort((a, b) => a.drawZ - b.drawZ);

    drawPetals.forEach(e => {
        const depth = (e.drawZ + 1) / 2;

        const size = 4 + depth * petals.radius;

        backgroundCtx.beginPath();
        backgroundCtx.fillStyle = e.color;

        backgroundCtx.arc(
            petals.x + e.drawX * petals.size,
            petals.y + e.drawY * petals.size,
            size,
            0,
            Math.PI * 2
        );

        backgroundCtx.fill();
    });

    requestAnimationFrame(draw);
}

function resize() {
    backgroundWidth = background.width = background.clientWidth;
    backgroundHeight = background.height = background.clientHeight;

    petals.x = backgroundWidth / 2;
    petals.y = backgroundHeight / 2;
}

function init() {
    window.addEventListener("resize", resize);

    initPetals(40);
    draw();
}

init();