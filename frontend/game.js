const statusNode = document.querySelector("#run-status");
const scoreNode = document.querySelector("#current-score");
const leaderboardStatusNode = document.querySelector("#leaderboard-status");
const leaderboardListNode = document.querySelector("#leaderboard-list");
const startButton = document.querySelector("#start-button");
const canvas = document.querySelector("#game-canvas");

const context = canvas.getContext("2d");

function drawPlaceholder() {
  context.clearRect(0, 0, canvas.width, canvas.height);

  context.fillStyle = "#123256";
  context.fillRect(0, canvas.height - 120, canvas.width, 120);

  context.fillStyle = "#5ff2c6";
  context.fillRect(110, canvas.height - 190, 52, 70);

  context.fillStyle = "#ffc857";
  context.fillRect(canvas.width - 180, canvas.height - 175, 42, 55);

  context.fillStyle = "#e8f1ff";
  context.font = '24px "Trebuchet MS", sans-serif';
  context.fillText("Gameplay scaffold", 40, 48);
}

function boot() {
  drawPlaceholder();
  statusNode.textContent = "Scaffold ready";
  scoreNode.textContent = "0";
  leaderboardStatusNode.textContent = "Waiting for backend";
  leaderboardListNode.innerHTML = "<li>Connect the live feed in the next step.</li>";

  startButton.addEventListener("click", () => {
    statusNode.textContent = "Gameplay not implemented yet";
  });
}

boot();
