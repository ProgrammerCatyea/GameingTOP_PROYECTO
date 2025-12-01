const API_BASE_URL = "http://127.0.0.1:8000";
const RANKINGS_ENDPOINT = `${API_BASE_URL}/rankings`;
const USERS_ENDPOINT = `${API_BASE_URL}/usuarios`;
const rankingForm = document.getElementById("ranking-form");
const rankingIdInput = document.getElementById("ranking-id");
const rankingNombreInput = document.getElementById("ranking-nombre");
const rankingDescripcionInput = document.getElementById("ranking-descripcion");
const rankingTipoSelect = document.getElementById("ranking-tipo");
const rankingUserSelect = document.getElementById("ranking-user");
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
  rankingNombreInput.value = "";
  rankingDescripcionInput.value = "";
  rankingTipoSelect.value = "global";
  rankingUserSelect.value = "";
  setRankingFormCreateMode();
}


async function fetchUsersForSelect() {
  try {
    const res = await fetch(USERS_ENDPOINT);
    if (!res.ok) throw new Error("Error al obtener usuarios");

    const users = await res.json();
    rankingUserSelect.innerHTML = "";

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Seleccione un usuario (opcional)";
    rankingUserSelect.appendChild(placeholder);

    users.forEach((user) => {
      const opt = document.createElement("option");
      opt.value = user.id;
      const nick = user.nickname || user.nombre || `Usuario #${user.id}`;
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
      nombre,
      tipo,
      user_id,
      games,
    } = rk;

    const numGames = Array.isArray(games) ? games.length : 0;

    let userLabel = "-";
    if (rk.user?.nickname || rk.user?.nombre) {
      userLabel = rk.user.nickname ?? rk.user.nombre;
    } else if (user_id) {
      userLabel = `Usuario #${user_id}`;
    }

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${id ?? "-"}</td>
      <td>${nombre ?? "-"}</td>
      <td>${tipo ?? "-"}</td>
      <td>${userLabel}</td>
      <td>${numGames}</td>
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
  const nombre = rankingNombreInput.value.trim();
  const descripcion = rankingDescripcionInput.value.trim() || null;
  const tipo = rankingTipoSelect.value || "global";
  const userId = rankingUserSelect.value ? Number(rankingUserSelect.value) : null;

  return {
    nombre,
    descripcion,
    tipo,
    user_id: userId,
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

  if (!rankingNombreInput.value.trim()) {
    showRankingToast("El nombre del ranking es obligatorio.", "error");
    return;
  }

  const payload = buildRankingPayload();
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
    rankingNombreInput.value = rk.nombre ?? "";
    rankingDescripcionInput.value = rk.descripcion ?? "";
    rankingTipoSelect.value = rk.tipo ?? "global";

    if (rk.user_id) {
      rankingUserSelect.value = rk.user_id.toString();
    } else {
      rankingUserSelect.value = "";
    }

    setRankingFormEditMode();
    showRankingToast("Editando ranking. Modifica los campos y guarda.");
  } catch (error) {
    console.error(error);
    showRankingToast(error.message || "No se pudo cargar el ranking.", "error");
  }
}


document.addEventListener("DOMContentLoaded", async () => {
  clearRankingForm();
  await fetchUsersForSelect();
  await fetchRankings();
});
