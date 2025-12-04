const API_BASE_URL = "https://gameingtop-proyecto-1.onrender.com";
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
  if (!rankingFormToastContainer) return;

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
  if (!rankingFormModeLabel || !btnSubmitRanking) return;

  rankingFormModeLabel.textContent = "Modo: creación";
  rankingFormModeLabel.classList.remove("badge-soft");
  rankingFormModeLabel.classList.add("badge-pill");
  btnSubmitRanking.textContent = "Guardar ranking";
  btnSubmitRanking.classList.remove("btn-edit-mode");
}

function setRankingFormEditMode() {
  if (!rankingFormModeLabel || !btnSubmitRanking) return;

  rankingFormModeLabel.textContent = "Modo: edición";
  rankingFormModeLabel.classList.remove("badge-pill");
  rankingFormModeLabel.classList.add("badge-soft");
  btnSubmitRanking.textContent = "Actualizar ranking";
  btnSubmitRanking.classList.add("btn-edit-mode");
}

function clearRankingForm() {
  if (rankingIdInput) rankingIdInput.value = "";
  if (rankingNombreInput) rankingNombreInput.value = "";
  if (rankingDescripcionInput) rankingDescripcionInput.value = "";
  if (rankingTipoSelect) rankingTipoSelect.value = "global";
  if (rankingUserSelect) rankingUserSelect.value = "";
  setRankingFormCreateMode();
}



async function fetchUsersForSelect() {
  if (!rankingUserSelect) return;

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
  if (!rankingsTableBody) return;

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
  if (!rankingsTableBody) return;

  rankingsTableBody.innerHTML = "";

  if (!rankings || rankings.length === 0) {
    if (rankingsEmptyText) rankingsEmptyText.style.display = "block";
    return;
  }

  if (rankingsEmptyText) rankingsEmptyText.style.display = "none";

  rankings.forEach((rk) => {
    const {
      id,
      nombre,
      tipo,
      user_id,
      games,
      image_url,  
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

        <div class="ranking-image-section" style="margin-top: 0.5rem;">
          <div class="ranking-image-preview-wrapper" style="margin-bottom: 0.25rem;">
            ${
              image_url
                ? `<img src="${image_url}" alt="Imagen ranking ${nombre ?? ""}" class="ranking-image-preview" style="max-width: 120px; border-radius: 4px;">`
                : `<span class="no-image-text" style="font-size: 0.8rem; color: #888;">Sin imagen</span>`
            }
          </div>
          <div class="ranking-image-actions">
            <input 
              type="file" 
              accept="image/*" 
              data-role="ranking-image-input" 
              data-id="${id}"
              style="display: none;"
            >
            <button 
              type="button" 
              class="btn btn-sm btn-secondary" 
              data-action="open-upload-image" 
              data-id="${id}"
            >
              ${image_url ? "Cambiar imagen" : "Subir imagen"}
            </button>
          </div>
        </div>
      </td>
    `;

    const fileInput = tr.querySelector('input[data-role="ranking-image-input"]');
    const uploadBtn = tr.querySelector('button[data-action="open-upload-image"]');

    if (uploadBtn && fileInput) {
      uploadBtn.addEventListener("click", () => {
        fileInput.click();
      });

      fileInput.addEventListener("change", async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        try {
          await uploadRankingImage(id, file);
          showRankingToast("Imagen subida correctamente.");
          await fetchRankings();
        } catch (error) {
          console.error(error);
          showRankingToast(error.message || "No se pudo subir la imagen.", "error");
        } finally {
          e.target.value = "";
        }
      });
    }

    rankingsTableBody.appendChild(tr);
  });
}



function buildRankingPayload() {
  const nombre = rankingNombreInput ? rankingNombreInput.value.trim() : "";
  const descripcion = rankingDescripcionInput && rankingDescripcionInput.value.trim()
    ? rankingDescripcionInput.value.trim()
    : null;
  const tipo = rankingTipoSelect && rankingTipoSelect.value
    ? rankingTipoSelect.value
    : "global";
  const userId = rankingUserSelect && rankingUserSelect.value
    ? Number(rankingUserSelect.value)
    : null;

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



async function uploadRankingImage(id, file) {
  const url = `${RANKINGS_ENDPOINT}/${id}/image`;

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(url, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al subir la imagen del ranking.");
  }

  return res.json();
}


if (rankingForm) {
  rankingForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = rankingIdInput && rankingIdInput.value ? rankingIdInput.value : null;

    if (!rankingNombreInput || !rankingNombreInput.value.trim()) {
      showRankingToast("El nombre del ranking es obligatorio.", "error");
      return;
    }

    const payload = buildRankingPayload();
    if (btnSubmitRanking) btnSubmitRanking.disabled = true;

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
      if (btnSubmitRanking) btnSubmitRanking.disabled = false;
    }
  });
}


if (btnReloadRankings) {
  btnReloadRankings.addEventListener("click", () => {
    fetchRankings();
  });
}

if (btnClearFormRanking) {
  btnClearFormRanking.addEventListener("click", () => {
    clearRankingForm();
  });
}

if (rankingsTableBody) {
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
}

async function handleEditRankingClick(id) {
  try {
    const res = await fetch(`${RANKINGS_ENDPOINT}/${id}`);
    if (!res.ok) {
      throw new Error("No se pudo cargar la información del ranking.");
    }

    const rk = await res.json();

    if (rankingIdInput) rankingIdInput.value = rk.id ?? "";
    if (rankingNombreInput) rankingNombreInput.value = rk.nombre ?? "";
    if (rankingDescripcionInput) rankingDescripcionInput.value = rk.descripcion ?? "";
    if (rankingTipoSelect) rankingTipoSelect.value = rk.tipo ?? "global";

    if (rankingUserSelect) {
      if (rk.user_id) {
        rankingUserSelect.value = rk.user_id.toString();
      } else {
        rankingUserSelect.value = "";
      }
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
