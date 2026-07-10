const statusNode = document.querySelector("#run-status");
const scoreNode = document.querySelector("#current-score");
const leaderboardStatusNode = document.querySelector("#leaderboard-status");
const leaderboardListNode = document.querySelector("#leaderboard-list");
const playerNameInput = document.querySelector("#player-name");
const startButton = document.querySelector("#start-button");
const canvas = document.querySelector("#game-canvas");

const context = canvas.getContext("2d");

const world = {
  gravity: 1800,
  groundHeight: 120,
  scrollSpeed: 320,
};

const player = {
  width: 52,
  height: 70,
  x: 110,
  y: 0,
  velocityY: 0,
  jumpForce: 720,
  jumps: 0,
  maxJumps: 2,
};

const gameState = {
  animationFrame: 0,
  lastTime: 0,
  running: false,
  distance: 0,
  floorOffset: 0,
};

function getGroundY() {
  return canvas.height - world.groundHeight;
}

function resetPlayer() {
  player.y = getGroundY() - player.height;
  player.velocityY = 0;
  player.jumps = 0;
}

function resetGame() {
  resetPlayer();
  gameState.distance = 0;
  gameState.floorOffset = 0;
  gameState.lastTime = 0;
  scoreNode.textContent = "0";
}

function drawScene() {
  context.clearRect(0, 0, canvas.width, canvas.height);

  const gradient = context.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#17345a");
  gradient.addColorStop(1, "#08111f");
  context.fillStyle = gradient;
  context.fillRect(0, 0, canvas.width, canvas.height);

  context.fillStyle = "#123256";
  context.fillRect(0, getGroundY(), canvas.width, world.groundHeight);

  context.strokeStyle = "rgba(255, 255, 255, 0.08)";
  context.lineWidth = 2;
  for (let x = -80 + gameState.floorOffset; x < canvas.width + 80; x += 80) {
    context.beginPath();
    context.moveTo(x, getGroundY());
    context.lineTo(x + 30, canvas.height);
    context.stroke();
  }

  context.fillStyle = "#5ff2c6";
  context.fillRect(player.x, player.y, player.width, player.height);

  context.fillStyle = "#e8f1ff";
  context.font = '24px "Trebuchet MS", sans-serif';
  context.fillText("Runner training zone", 40, 48);
}

function update(deltaSeconds) {
  player.velocityY += world.gravity * deltaSeconds;
  player.y += player.velocityY * deltaSeconds;

  const groundLevel = getGroundY() - player.height;
  if (player.y >= groundLevel) {
    player.y = groundLevel;
    player.velocityY = 0;
    player.jumps = 0;
  }

  gameState.distance += world.scrollSpeed * deltaSeconds;
  gameState.floorOffset = (gameState.floorOffset - world.scrollSpeed * deltaSeconds) % 80;
  scoreNode.textContent = String(Math.floor(gameState.distance / 10));
}

function loop(timestamp) {
  if (!gameState.running) {
    return;
  }

  if (!gameState.lastTime) {
    gameState.lastTime = timestamp;
  }

  const deltaSeconds = Math.min((timestamp - gameState.lastTime) / 1000, 0.033);
  gameState.lastTime = timestamp;

  update(deltaSeconds);
  drawScene();
  gameState.animationFrame = window.requestAnimationFrame(loop);
}

function jump() {
  if (!gameState.running || player.jumps >= player.maxJumps) {
    return;
  }

  player.velocityY = -player.jumpForce;
  player.jumps += 1;
}

function startRun() {
  resetGame();
  gameState.running = true;
  statusNode.textContent = `Running: ${playerNameInput.value.trim() || "Anonymous"}`;
  window.cancelAnimationFrame(gameState.animationFrame);
  gameState.animationFrame = window.requestAnimationFrame(loop);
}

function boot() {
  resetGame();
  drawScene();
  statusNode.textContent = "Scaffold ready";
  leaderboardStatusNode.textContent = "Waiting for backend";
  leaderboardListNode.innerHTML = "<li>Connect the live feed in the next step.</li>";

  startButton.addEventListener("click", () => {
    startRun();
  });

  window.addEventListener("keydown", (event) => {
    if (event.code === "Space" || event.code === "ArrowUp") {
      event.preventDefault();
      jump();
    }
  });
}

boot();
