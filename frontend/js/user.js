const API_BASE_URL = "https://gameingtop-proyecto-1.onrender.com";
const USERS_ENDPOINT = `${API_BASE_URL}/usuarios`;
const userForm = document.getElementById("user-form");
const userIdInput = document.getElementById("user-id");
const userNombreInput = document.getElementById("user-nombre");
const userNicknameInput = document.getElementById("user-nickname");
const userEmailInput = document.getElementById("user-email");
const userPaisInput = document.getElementById("user-pais");
const userEdadInput = document.getElementById("user-edad");
const userNivelInput = document.getElementById("user-nivel");
const userFormModeLabel = document.getElementById("user-form-mode-label");
const userFormToastContainer = document.getElementById("user-form-toast-container");
const usersTableBody = document.getElementById("users-table-body");
const usersEmptyText = document.getElementById("users-empty-text");
const btnReloadUsers = document.getElementById("btn-reload-users");
const btnClearFormUser = document.getElementById("btn-clear-form-user");
const btnSubmitUser = document.getElementById("btn-submit-user");


function showUserToast(message, type = "success") {
  if (!userFormToastContainer) return;

  userFormToastContainer.innerHTML = "";

  const toast = document.createElement("div");
  toast.classList.add("toast");
  if (type === "success") toast.classList.add("toast-success");
  if (type === "error") toast.classList.add("toast-error");

  toast.textContent = message;
  userFormToastContainer.appendChild(toast);

  setTimeout(() => {
    if (userFormToastContainer.contains(toast)) {
      userFormToastContainer.removeChild(toast);
    }
  }, 3500);
}


function setFormToCreateMode() {
  if (!userFormModeLabel || !btnSubmitUser) return;

  userFormModeLabel.textContent = "Modo: creación";
  userFormModeLabel.classList.remove("badge-soft");
  userFormModeLabel.classList.add("badge-pill");

  btnSubmitUser.textContent = "Guardar usuario";
  btnSubmitUser.classList.remove("btn-edit-mode");
}

function setFormToEditMode() {
  if (!userFormModeLabel || !btnSubmitUser) return;

  userFormModeLabel.textContent = "Modo: edición";
  userFormModeLabel.classList.remove("badge-pill");
  userFormModeLabel.classList.add("badge-soft");

  btnSubmitUser.textContent = "Actualizar usuario";
  btnSubmitUser.classList.add("btn-edit-mode");
}

function clearUserForm() {
  if (userIdInput) userIdInput.value = "";
  if (userNombreInput) userNombreInput.value = "";
  if (userNicknameInput) userNicknameInput.value = "";
  if (userEmailInput) userEmailInput.value = "";
  if (userPaisInput) userPaisInput.value = "";
  if (userEdadInput) userEdadInput.value = "";
  if (userNivelInput) userNivelInput.value = "";

  setFormToCreateMode();
}


async function fetchUsers() {
  if (!usersTableBody) return;

  try {
    const res = await fetch(USERS_ENDPOINT);
    if (!res.ok) {
      throw new Error(`Error al obtener usuarios: ${res.status}`);
    }
    const data = await res.json();
    renderUsers(data);
  } catch (error) {
    console.error(error);
    showUserToast("No se pudo cargar la lista de usuarios.", "error");
  }
}

function renderUsers(users) {
  if (!usersTableBody) return;

  usersTableBody.innerHTML = "";

  if (!users || users.length === 0) {
    if (usersEmptyText) usersEmptyText.style.display = "block";
    return;
  }

  if (usersEmptyText) usersEmptyText.style.display = "none";

  users.forEach((user) => {
    const {
      id,
      nombre,
      nickname,
      email,
      pais,
      edad,
      nivel_rol,
    } = user;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${id ?? "-"}</td>
      <td>${nombre ?? "-"}</td>
      <td>${nickname ?? "-"}</td>
      <td>${email ?? "-"}</td>
      <td>${pais ?? "-"}</td>
      <td>${edad ?? "-"}</td>
      <td>${nivel_rol ?? "-"}</td>
      <td>
        <div class="table-actions">
          <button class="btn btn-sm btn-outline" data-action="edit-user" data-id="${id}">
            Editar
          </button>
          <button class="btn btn-sm btn-ghost" data-action="delete-user" data-id="${id}">
            Eliminar
          </button>
        </div>
      </td>
    `;
    usersTableBody.appendChild(tr);
  });
}

function buildUserPayload() {
  return {
    nombre: userNombreInput ? userNombreInput.value.trim() : "",
    nickname: userNicknameInput && userNicknameInput.value.trim()
      ? userNicknameInput.value.trim()
      : null,
    email: userEmailInput && userEmailInput.value.trim()
      ? userEmailInput.value.trim()
      : null,
    pais: userPaisInput && userPaisInput.value.trim()
      ? userPaisInput.value.trim()
      : null,
    edad: userEdadInput && userEdadInput.value
      ? Number(userEdadInput.value)
      : null,
    nivel_rol: userNivelInput && userNivelInput.value.trim()
      ? userNivelInput.value.trim()
      : null,
  };
}

async function createUser(payload) {
  const res = await fetch(USERS_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al crear el usuario.");
  }

  return res.json();
}

async function updateUser(id, payload) {
  const url = `${USERS_ENDPOINT}/${id}`;
  const res = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al actualizar el usuario.");
  }

  return res.json();
}

async function deleteUser(id) {
  const url = `${USERS_ENDPOINT}/${id}`;
  const res = await fetch(url, {
    method: "DELETE",
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || "Error al eliminar el usuario.");
  }

  return true;
}


if (userForm) {
  userForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = userIdInput && userIdInput.value ? userIdInput.value : null;

    if (!userNombreInput || !userNombreInput.value.trim()) {
      showUserToast("El nombre del usuario es obligatorio.", "error");
      return;
    }

    const payload = buildUserPayload();
    if (btnSubmitUser) btnSubmitUser.disabled = true;

    try {
      if (id) {
        await updateUser(id, payload);
        showUserToast("Usuario actualizado correctamente.");
      } else {
        await createUser(payload);
        showUserToast("Usuario creado correctamente.");
      }

      await fetchUsers();
      clearUserForm();
    } catch (error) {
      console.error(error);
      showUserToast(error.message || "Ocurrió un error.", "error");
    } finally {
      if (btnSubmitUser) btnSubmitUser.disabled = false;
    }
  });
}

if (btnReloadUsers) {
  btnReloadUsers.addEventListener("click", () => {
    fetchUsers();
  });
}

if (btnClearFormUser) {
  btnClearFormUser.addEventListener("click", () => {
    clearUserForm();
  });
}

if (usersTableBody) {
  usersTableBody.addEventListener("click", async (e) => {
    const button = e.target.closest("button");
    if (!button) return;

    const action = button.dataset.action;
    const id = button.dataset.id;

    if (!action || !id) return;

    if (action === "edit-user") {
      handleEditUserClick(id);
    }

    if (action === "delete-user") {
      const confirmed = confirm("¿Seguro que deseas eliminar este usuario?");
      if (!confirmed) return;

      try {
        await deleteUser(id);
        showUserToast("Usuario eliminado correctamente.");
        await fetchUsers();
      } catch (error) {
        console.error(error);
        showUserToast(error.message || "No se pudo eliminar el usuario.", "error");
      }
    }
  });
}


async function handleEditUserClick(id) {
  try {
    const res = await fetch(`${USERS_ENDPOINT}/${id}`);
    if (!res.ok) {
      throw new Error("No se pudo cargar la información del usuario.");
    }
    const user = await res.json();

    if (userIdInput) userIdInput.value = user.id ?? "";
    if (userNombreInput) userNombreInput.value = user.nombre ?? "";
    if (userNicknameInput) userNicknameInput.value = user.nickname ?? "";
    if (userEmailInput) userEmailInput.value = user.email ?? "";
    if (userPaisInput) userPaisInput.value = user.pais ?? "";
    if (userEdadInput) userEdadInput.value = user.edad ?? "";
    if (userNivelInput) userNivelInput.value = user.nivel_rol ?? "";

    setFormToEditMode();
    showUserToast("Editando usuario. Modifica los campos y guarda.");
  } catch (error) {
    console.error(error);
    showUserToast(error.message || "No se pudo cargar el usuario.", "error");
  }
}


document.addEventListener("DOMContentLoaded", () => {
  clearUserForm();
  fetchUsers();
});
