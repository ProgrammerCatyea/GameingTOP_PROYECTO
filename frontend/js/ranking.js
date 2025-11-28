const API_BASE_URL = "http://127.0.0.1:8000";
const RANKINGS_ENDPOINT = `${API_BASE_URL}/rankings`;
const GAMES_ENDPOINT = `${API_BASE_URL}/juegos`;
const USERS_ENDPOINT = `${API_BASE_URL}/usuarios`;
const rankingForm = document.getElementById("ranking-form");
const rankingIdInput = document.getElementById("ranking-id");
const rankingGameSelect = document.getElementById("ranking-game");
const rankingUserSelect = document.getElementById("ranking-user");
const rankingScoreInput = document.getElementById("ranking-score");
const rankingPositionInput = document.getElementById("ranking-position");
const rankingFormModeLabel = document.getElementById("ranking-form-mode-label");
const rankingFormToastContainer = document.getElementById("ranking-form-toast-container");
const rankingsTableBody = document.getElementById("rankings-table-body");
const rankingsEmptyText = document.getElementById("rankings-empty-text");
const btnReloadRankings = document.getElementById("btn-reload-rankings");
const btnClearFormRanking = document.getElementById("btn-clear-form-ranking");
const btnSubmitRanking = document.getElementById("btn-submit-ranking");

function showRankingToast(message, type = "success") {
  rankingFormToastContainer.innerHTML = "";

  const toast = document.createElement("div");
  toast.classList.add("toast");
  if (type === "success") toast.classList.add("toast-success");
  if (type === "error") toast.classList.add("toast-error");

  toast.textContent = message;
  rankingFormToastContainer.appendChild(toast);

  setTimeout(() => {
    if (rankingFormToastContainer.contains(toast)) {
      rankingFormToastContainer.removeChild(toast);
    }
  }, 3500);
}

function setRankingFormCreateMode() {
  rankingFormModeLabel.textContent = "Modo: creación";
  rankingFormModeLabel.classList.remove("badge-soft");
  rankingFormModeLabel.classList.add("badge-pill");
  btnSubmitRanking.textContent = "Guardar ranking";
  btnSubmitRanking.classList.remove("btn-edit-mode");
}

function setRankingFormEditMode() {
  rankingFormModeLabel.textContent = "Modo: edición";
  rankingFormModeLabel.classList.remove("badge-pill");
  rankingFormModeLabel.classList.add("badge-soft");
  btnSubmitRanking.textContent = "Actualizar ranking";
  btnSubmitRanking.classList.add("btn-edit-mode");
}

function clearRankingForm() {
  rankingIdInput.value = "";
  rankingGameSelect.value = "";
  rankingUserSelect.value = "";
  rankingScoreInput.value = "";
  rankingPositionInput.value = "";
  setRankingFormCreateMode();
}


async function fetchGamesForSelect() {
  try {
    const res = await fetch(GAMES_ENDPOINT);
    if (!res.ok) throw new Error("Error al obtener juegos");

    const games = await res.json();
    rankingGameSelect.innerHTML = "";

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Selecciona un juego...";
    rankingGameSelect.appendChild(placeholder);

    games.forEach((game) => {
      const opt = document.createElement("option");
      opt.value = game.id;
      opt.textContent = game.nombre || `Juego #${game.id}`;
      rankingGameSelect.appendChild(opt);
    });
  } catch (error) {
    console.error(error);
    showRankingToast("No se pudieron cargar los juegos.", "error");
  }
}

async function fetchUsersForSelect() {
  try {
    const res = await fetch(USERS_ENDPOINT);
    if (!res.ok) throw new Error("Error al obtener usuarios");

    const users = await res.json();
    rankingUserSelect.innerHTML = "";

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Selecciona un usuario...";
    rankingUserSelect.appendChild(placeholder);

    users.forEach((user) => {
      const opt = document.createElement("option");
      opt.value = user.id;
      const nick = user.nickname || `User #${user.id}`;
      opt.textContent = `${nick} (${user.pais ?? "Sin país"})`;
      rankingUserSelect.appendChild(opt);
    });
  } catch (error) {
    console.error(error);
    showRankingToast("No se pudieron cargar los usuarios.", "error");
  }
}

async function fetchRankings() {
  try {
    const res = await fetch(RANKINGS_ENDPOINT);
    if (!res.ok) throw new Error("Error al obtener rankings");

    const data = await res.json();
    renderRankings(data);
  } catch (error) {
    console.error(error);
    showRankingToast("No se pudo cargar la lista de rankings.", "error");
  }
}

function renderRankings(rankings) {
  rankingsTableBody.innerHTML = "";

  if (!rankings || rankings.length === 0) {
    rankingsEmptyText.style.display = "block";
    return;
  }

  rankingsEmptyText.style.display = "none";

  rankings.forEach((rk) => {
    const {
      id,
      puntaje,
      posicion,
      game,
      user,
    } = rk;

    const gameName = game?.nombre ?? `Juego #${rk.game_id ?? "-"}`;
    const userName = user?.nickname ?? `User #${rk.user_id ?? "-"}`;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${id ?? "-"}</td>
      <td>${gameName}</td>
      <td>${userName}</td>
      <td>${puntaje ?? "-"}</td>
      <td>${posicion ?? "-"}</td>
      <td>
        <div class="table-actions">
          <button class="btn btn-sm btn-outline" data-action="edit-ranking" data-id="${id}">
            Editar
          </button>
          <button class="btn btn-sm btn-ghost" data-action="delete-ranking" data-id="${id}">
            Eliminar
          </button>
        </div>
      </td>
    `;
    rankingsTableBody.appendChild(tr);
  });
}

function buildRankingPayload() {
  const gameId = rankingGameSelect.value ? Number(rankingGameSelect.value) : null;
  const userId = rankingUserSelect.value ? Number(rankingUserSelect.value) : null;

  return {
    game_id: gameId,
    user_id: userId,
    puntaje: rankingScoreInput.value ? Number(rankingScoreInput.value) : null,
    posicion: rankingPositionInput.value ? Number(rankingPositionInput.value) : null,
  };
}

async function createRanking(payload) {
  const res = await fetch(RANKINGS_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al crear el ranking.");
  }
  return res.json();
}

async function updateRanking(id, payload) {
  const url = `${RANKINGS_ENDPOINT}/${id}`;
  const res = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al actualizar el ranking.");
  }
  return res.json();
}

async function deleteRanking(id) {
  const url = `${RANKINGS_ENDPOINT}/${id}`;
  const res = await fetch(url, { method: "DELETE" });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al eliminar el ranking.");
  }
  return true;
}


rankingForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = rankingIdInput.value || null;
  const payload = buildRankingPayload();

  if (!payload.game_id || !payload.user_id) {
    showRankingToast("Juego y usuario son obligatorios.", "error");
    return;
  }

  btnSubmitRanking.disabled = true;

  try {
    if (id) {
      await updateRanking(id, payload);
      showRankingToast("Ranking actualizado correctamente.");
    } else {
      await createRanking(payload);
      showRankingToast("Ranking creado correctamente.");
    }

    await fetchRankings();
    clearRankingForm();
  } catch (error) {
    console.error(error);
    showRankingToast(error.message || "Ocurrió un error en el ranking.", "error");
  } finally {
    btnSubmitRanking.disabled = false;
  }
});

btnReloadRankings.addEventListener("click", () => {
  fetchRankings();
});

btnClearFormRanking.addEventListener("click", () => {
  clearRankingForm();
});


rankingsTableBody.addEventListener("click", async (e) => {
  const button = e.target.closest("button");
  if (!button) return;

  const action = button.dataset.action;
  const id = button.dataset.id;

  if (!action || !id) return;

  if (action === "edit-ranking") {
    handleEditRankingClick(id);
  }

  if (action === "delete-ranking") {
    const confirmed = confirm("¿Seguro que deseas eliminar este ranking?");
    if (!confirmed) return;

    try {
      await deleteRanking(id);
      showRankingToast("Ranking eliminado correctamente.");
      await fetchRankings();
    } catch (error) {
      console.error(error);
      showRankingToast(error.message || "No se pudo eliminar el ranking.", "error");
    }
  }
});

async function handleEditRankingClick(id) {
  try {
    const res = await fetch(`${RANKINGS_ENDPOINT}/${id}`);
    if (!res.ok) {
      throw new Error("No se pudo cargar la información del ranking.");
    }

    const rk = await res.json();
    rankingIdInput.value = rk.id ?? "";
    if (rk.game_id) rankingGameSelect.value = rk.game_id;
    if (rk.user_id) rankingUserSelect.value = rk.user_id;
    if (!rankingGameSelect.value && rk.game?.id) {
      rankingGameSelect.value = rk.game.id;
    }
    if (!rankingUserSelect.value && rk.user?.id) {
      rankingUserSelect.value = rk.user.id;
    }

    rankingScoreInput.value = rk.puntaje ?? "";
    rankingPositionInput.value = rk.posicion ?? "";

    setRankingFormEditMode();
    showRankingToast("Editando ranking. Modifica los campos y guarda.");
  } catch (error) {
    console.error(error);
    showRankingToast(error.message || "No se pudo cargar el ranking.", "error");
  }
}


document.addEventListener("DOMContentLoaded", async () => {
  clearRankingForm();
  await Promise.all([fetchGamesForSelect(), fetchUsersForSelect()]);
  await fetchRankings();
});
