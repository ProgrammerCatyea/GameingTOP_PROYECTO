const API_BASE_URL = "http://127.0.0.1:8000";
const GAMES_ENDPOINT = `${API_BASE_URL}/juegos`;
const gameForm = document.getElementById("game-form");
const gameIdInput = document.getElementById("game-id");
const nombreInput = document.getElementById("nombre");
const plataformaInput = document.getElementById("plataforma");
const desarrolladorInput = document.getElementById("desarrollador");
const generoPrincipalInput = document.getElementById("genero-principal");
const categoriasIdsInput = document.getElementById("categorias-ids");
const userIdInput = document.getElementById("user-id");
const formModeLabel = document.getElementById("form-mode-label");
const formToastContainer = document.getElementById("form-toast-container");
const gamesTableBody = document.getElementById("games-table-body");
const gamesEmptyText = document.getElementById("games-empty-text");
const btnReload = document.getElementById("btn-reload");
const btnClearForm = document.getElementById("btn-clear-form");
const btnSubmit = document.getElementById("btn-submit");


function showToast(message, type = "success", container = formToastContainer) {
  container.innerHTML = "";

  const toast = document.createElement("div");
  toast.classList.add("toast");
  if (type === "success") toast.classList.add("toast-success");
  if (type === "error") toast.classList.add("toast-error");

  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    if (container.contains(toast)) {
      container.removeChild(toast);
    }
  }, 3500);
}

function clearForm() {
  gameIdInput.value = "";
  nombreInput.value = "";
  plataformaInput.value = "";
  desarrolladorInput.value = "";
  generoPrincipalInput.value = "";
  categoriasIdsInput.value = "";
  userIdInput.value = "";

  formModeLabel.textContent = "Modo: creación";
  formModeLabel.classList.remove("badge-soft");
  formModeLabel.classList.add("badge-pill");
  btnSubmit.textContent = "Guardar juego";
}


async function fetchGames() {
  try {
    const res = await fetch(GAMES_ENDPOINT);
    if (!res.ok) {
      throw new Error(`Error al obtener juegos: ${res.status}`);
    }
    const data = await res.json();
    renderGames(data);
  } catch (error) {
    console.error(error);
    showToast("No se pudo cargar la lista de juegos.", "error");
  }
}

function renderGames(games) {
  gamesTableBody.innerHTML = "";

  if (!games || games.length === 0) {
    gamesEmptyText.style.display = "block";
    return;
  }

  gamesEmptyText.style.display = "none";

  games.forEach((game) => {
    const {
      id,
      appid,
      nombre,
      plataforma,
      desarrollador,
      genero_principal,
      categorias,
      user_id,
    } = game;

    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${id ?? "-"}</td>
      <td>${appid ?? "-"}</td>
      <td>${nombre ?? "-"}</td>
      <td>${plataforma ?? "-"}</td>
      <td>${desarrollador ?? "-"}</td>
      <td>${genero_principal ?? "-"}</td>
      <td>
        ${
          Array.isArray(categorias) && categorias.length > 0
            ? `<div class="tag-list">${categorias
                .map(
                  (c) =>
                    `<span class="tag-pill">${c.id != null ? `#${c.id} - ` : ""}${
                      c.nombre ?? c.name ?? ""
                    }</span>`
                )
                .join("")}</div>`
            : "-"
        }
      </td>
      <td>${user_id ?? "-"}</td>
      <td>
        <div class="table-actions">
          <button class="btn btn-sm btn-outline" data-action="edit" data-id="${id}">
            Editar
          </button>
          <button class="btn btn-sm btn-ghost" data-action="delete" data-id="${id}">
            Eliminar
          </button>
        </div>
      </td>
    `;

    gamesTableBody.appendChild(tr);
  });
}


function buildGamePayload() {
  const categoriasIds = categoriasIdsInput.value
    ? categoriasIdsInput.value
        .split(",")
        .map((v) => v.trim())
        .filter((v) => v !== "")
        .map((v) => Number(v))
        .filter((n) => !Number.isNaN(n))
    : [];

  const userId = userIdInput.value ? Number(userIdInput.value) : null;

  return {
    nombre: nombreInput.value.trim(),
    plataforma: plataformaInput.value.trim() || "Steam/PC",
    desarrollador: desarrolladorInput.value.trim() || null,
    genero_principal: generoPrincipalInput.value.trim() || null,
    categorias_ids: categoriasIds,
    user_id: userId,
  };
}

async function createGame(payload) {
  const res = await fetch(GAMES_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al crear el juego.");
  }

  return res.json();
}

async function updateGame(id, payload) {
  const url = `${GAMES_ENDPOINT}/${id}`;
  const res = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al actualizar el juego.");
  }

  return res.json();
}

async function deleteGame(id) {
  const url = `${GAMES_ENDPOINT}/${id}`;
  const res = await fetch(url, {
    method: "DELETE",
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al eliminar el juego.");
  }

  return true;
}


gameForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = gameIdInput.value || null;

  if (!nombreInput.value.trim()) {
    showToast("El nombre del juego es obligatorio.", "error");
    return;
  }

  const payload = buildGamePayload();

  btnSubmit.disabled = true;

  try {
    if (id) {
      await updateGame(id, payload);
      showToast("Juego actualizado correctamente.");
    } else {
      await createGame(payload);
      showToast("Juego creado correctamente.");
    }

    await fetchGames();
    clearForm();
  } catch (error) {
    console.error(error);
    showToast(error.message || "Ocurrió un error.", "error");
  } finally {
    btnSubmit.disabled = false;
  }
});

btnReload.addEventListener("click", () => {
  fetchGames();
});

btnClearForm.addEventListener("click", () => {
  clearForm();
});

gamesTableBody.addEventListener("click", async (e) => {
  const button = e.target.closest("button");
  if (!button) return;

  const action = button.dataset.action;
  const id = button.dataset.id;

  if (!action || !id) return;

  if (action === "edit") {
    handleEditClick(id);
  }

  if (action === "delete") {
    const confirmed = confirm("¿Seguro que deseas eliminar este juego?");
    if (!confirmed) return;

    try {
      await deleteGame(id);
      showToast("Juego eliminado correctamente.");
      await fetchGames();
    } catch (error) {
      console.error(error);
      showToast(error.message || "No se pudo eliminar el juego.", "error");
    }
  }
});

async function handleEditClick(id) {
  try {
    const res = await fetch(`${GAMES_ENDPOINT}/${id}`);
    if (!res.ok) {
      throw new Error("No se pudo cargar la información del juego.");
    }
    const game = await res.json();

    gameIdInput.value = game.id ?? "";
    nombreInput.value = game.nombre ?? "";
    plataformaInput.value = game.plataforma ?? "";
    desarrolladorInput.value = game.desarrollador ?? "";
    generoPrincipalInput.value = game.genero_principal ?? "";
    userIdInput.value = game.user_id ?? "";

    if (Array.isArray(game.categorias) && game.categorias.length > 0) {
      const ids = game.categorias
        .map((c) => c.id)
        .filter((id) => id != null);
      categoriasIdsInput.value = ids.join(", ");
    } else {
      categoriasIdsInput.value = "";
    }

    formModeLabel.textContent = "Modo: edición";
    formModeLabel.classList.remove("badge-pill");
    formModeLabel.classList.add("badge-soft");
    btnSubmit.textContent = "Actualizar juego";
    showToast("Editando juego. Modifica los campos y guarda.");
  } catch (error) {
    console.error(error);
    showToast(error.message || "No se pudo cargar el juego.", "error");
  }
}


document.addEventListener("DOMContentLoaded", () => {
  clearForm();
  fetchGames();
});
