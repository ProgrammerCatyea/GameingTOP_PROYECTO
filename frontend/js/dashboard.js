

const API_BASE_URL = "http://127.0.0.1:8000";

const GAMES_ENDPOINT = `${API_BASE_URL}/juegos`;
const USERS_ENDPOINT = `${API_BASE_URL}/usuarios`;
const RANKINGS_ENDPOINT = `${API_BASE_URL}/rankings`;


const kpiTotalGames = document.getElementById("kpi-total-games");
const kpiTotalUsers = document.getElementById("kpi-total-users");
const kpiTotalRankings = document.getElementById("kpi-total-rankings");
const kpiTopGenre = document.getElementById("kpi-top-genre");
const btnDashboardReload = document.getElementById("btn-dashboard-reload");
const dashboardToastContainer = document.getElementById("dashboard-toast-container");
const chartGamesPlatformCanvas = document.getElementById("chart-games-platform");
const chartGamesPlatformEmpty = document.getElementById("chart-games-platform-empty");
const chartGamesGenreCanvas = document.getElementById("chart-games-genre");
const chartGamesGenreEmpty = document.getElementById("chart-games-genre-empty");
const chartRankingsTypeCanvas = document.getElementById("chart-rankings-type");
const chartRankingsTypeEmpty = document.getElementById("chart-rankings-type-empty");
let chartGamesPlatform = null;
let chartGamesGenre = null;
let chartRankingsType = null;


function showDashboardToast(message, type = "success") {
  dashboardToastContainer.innerHTML = "";

  const toast = document.createElement("div");
  toast.classList.add("toast");
  if (type === "success") toast.classList.add("toast-success");
  if (type === "error") toast.classList.add("toast-error");

  toast.textContent = message;
  dashboardToastContainer.appendChild(toast);

  setTimeout(() => {
    if (dashboardToastContainer.contains(toast)) {
      dashboardToastContainer.removeChild(toast);
    }
  }, 3500);
}


async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Error al consultar ${url}: ${res.status}`);
  }
  return res.json();
}

async function loadDashboardData() {
  btnDashboardReload.disabled = true;

  try {

    const [games, users, rankings] = await Promise.all([
      fetchJSON(GAMES_ENDPOINT),
      fetchJSON(USERS_ENDPOINT),
      fetchJSON(RANKINGS_ENDPOINT),
    ]);

    updateKPIs(games, users, rankings);
    updateCharts(games, rankings);

    showDashboardToast("Dashboard actualizado correctamente.");
  } catch (error) {
    console.error(error);
    showDashboardToast(
      error.message || "No se pudieron cargar los datos del dashboard.",
      "error"
    );
  } finally {
    btnDashboardReload.disabled = false;
  }
}


function updateKPIs(games, users, rankings) {
  // Totales
  kpiTotalGames.textContent = games.length ?? 0;
  kpiTotalUsers.textContent = users.length ?? 0;
  kpiTotalRankings.textContent = rankings.length ?? 0;

  const genreCounts = {};
  games.forEach((game) => {
    const genre = (game.genero_principal || "").trim();
    if (!genre) return;
    if (!genreCounts[genre]) genreCounts[genre] = 0;
    genreCounts[genre]++;
  });

  if (Object.keys(genreCounts).length === 0) {
    kpiTopGenre.textContent = "-";
    return;
  }

  const topGenre = Object.entries(genreCounts).sort((a, b) => b[1] - a[1])[0][0];
  kpiTopGenre.textContent = topGenre;
}


function updateCharts(games, rankings) {
  const platformCounts = {};
  games.forEach((game) => {
    const platform = (game.plataforma || "Sin plataforma").trim();
    if (!platformCounts[platform]) platformCounts[platform] = 0;
    platformCounts[platform]++;
  });

  const platforms = Object.keys(platformCounts);
  const platformValues = Object.values(platformCounts);

  if (chartGamesPlatform) chartGamesPlatform.destroy();

  if (platforms.length === 0) {
    chartGamesPlatformEmpty.style.display = "block";
  } else {
    chartGamesPlatformEmpty.style.display = "none";
    chartGamesPlatform = new Chart(chartGamesPlatformCanvas, {
      type: "bar",
      data: {
        labels: platforms,
        datasets: [
          {
            label: "Juegos por plataforma",
            data: platformValues,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: { color: "#ffffff99" },
          },
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, color: "#ffffff99" },
          },
        },
      },
    });
  }

  const genreCounts = {};
  games.forEach((game) => {
    const genre = (game.genero_principal || "Sin género").trim();
    if (!genreCounts[genre]) genreCounts[genre] = 0;
    genreCounts[genre]++;
  });

  const genres = Object.keys(genreCounts);
  const genreValues = Object.values(genreCounts);

  if (chartGamesGenre) chartGamesGenre.destroy();

  if (genres.length === 0) {
    chartGamesGenreEmpty.style.display = "block";
  } else {
    chartGamesGenreEmpty.style.display = "none";
    chartGamesGenre = new Chart(chartGamesGenreCanvas, {
      type: "bar",
      data: {
        labels: genres,
        datasets: [
          {
            label: "Juegos por género",
            data: genreValues,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: { color: "#ffffff99" },
          },
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, color: "#ffffff99" },
          },
        },
      },
    });
  }

  const typeCounts = {};
  rankings.forEach((rk) => {
    const type = (rk.tipo || "sin tipo").trim().toLowerCase();
    if (!typeCounts[type]) typeCounts[type] = 0;
    typeCounts[type]++;
  });

  const types = Object.keys(typeCounts);
  const typeValues = Object.values(typeCounts);

  if (chartRankingsType) chartRankingsType.destroy();

  if (types.length === 0) {
    chartRankingsTypeEmpty.style.display = "block";
  } else {
    chartRankingsTypeEmpty.style.display = "none";
    chartRankingsType = new Chart(chartRankingsTypeCanvas, {
      type: "bar",
      data: {
        labels: types,
        datasets: [
          {
            label: "Rankings por tipo",
            data: typeValues,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: { color: "#ffffff99" },
          },
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, color: "#ffffff99" },
          },
        },
      },
    });
  }
}


btnDashboardReload.addEventListener("click", () => {
  loadDashboardData();
});


document.addEventListener("DOMContentLoaded", () => {
  loadDashboardData();
});
