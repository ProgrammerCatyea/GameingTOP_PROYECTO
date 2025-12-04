const API_BASE_URL = "https://gameingtop-proyecto.onrender.com";
const STEAM_TOP_ENDPOINT = `${API_BASE_URL}/steam/top-games`;
const STEAM_DETAILS_ENDPOINT = (appid) => `${API_BASE_URL}/steam/details/${appid}`;
const btnLoadTopSteam = document.getElementById("btn-load-top-steam");
const btnReloadTopSteam = document.getElementById("btn-reload-top-steam");
const steamTopTableBody = document.getElementById("steam-top-table-body");
const steamTopEmptyText = document.getElementById("steam-top-empty-text");
const steamToastContainer = document.getElementById("steam-toast-container");
const steamGameDetailContainer = document.getElementById("steam-game-detail");
const steamSearchForm = document.getElementById("steam-search-form");
const steamAppidInput = document.getElementById("steam-appid-input");
const btnSearchAppid = document.getElementById("btn-search-appid");


function showSteamToast(message, type = "success") {
  steamToastContainer.innerHTML = "";

  const toast = document.createElement("div");
  toast.classList.add("toast");
  if (type === "success") toast.classList.add("toast-success");
  if (type === "error") toast.classList.add("toast-error");

  toast.textContent = message;
  steamToastContainer.appendChild(toast);

  setTimeout(() => {
    if (steamToastContainer.contains(toast)) {
      steamToastContainer.removeChild(toast);
    }
  }, 3500);
}

function renderSteamDetail(detail) {
  if (!detail) {
    steamGameDetailContainer.innerHTML = `
      <p class="text-muted">
        No se encontraron detalles para este juego. Intenta con otro AppID.
      </p>
    `;
    return;
  }

  const {
    id,
    nombre,
    descripcion,
    generos,
    precio,
    desarrollador,
    editora,
    imagen,
  } = detail;

  let generosText = "-";
  if (Array.isArray(generos) && generos.length > 0) {

    if (typeof generos[0] === "object") {
      generosText = generos.map((g) => g.description || g.name || "").join(", ");
    } else {
      generosText = generos.join(", ");
    }
  }

  let devText = "-";
  if (Array.isArray(desarrollador)) {
    devText = desarrollador.join(", ");
  } else if (typeof desarrollador === "string") {
    devText = desarrollador;
  }

  let pubText = "-";
  if (Array.isArray(editora)) {
    pubText = editora.join(", ");
  } else if (typeof editora === "string") {
    pubText = editora;
  }

  const safePrecio = precio || "Gratis";

  steamGameDetailContainer.innerHTML = `
    <div class="card" style="margin-top: 8px;">
      <div class="card-body">
        <div style="display:flex; gap:16px; align-items:flex-start; flex-wrap:wrap;">
          ${imagen ? `
          <div>
            <img src="${imagen}" alt="Portada de ${nombre ?? "Juego"}"
              style="max-width:220px; border-radius:16px; display:block;" />
          </div>` : ""}
          <div style="flex:1; min-width:220px;">
            <h3 style="margin:0 0 6px 0; font-size:1.05rem;">${nombre ?? "Juego sin nombre"}</h3>
            <p class="text-muted" style="margin:0 0 8px 0;">
              AppID: <strong>${id ?? "-"}</strong> · Precio: <strong>${safePrecio}</strong>
            </p>
            <p style="margin:0 0 8px 0; font-size:0.9rem;">
              ${descripcion ?? "Este juego no tiene una descripción breve disponible."}
            </p>
            <p style="margin:0 0 4px 0; font-size:0.85rem;">
              <strong>Géneros:</strong> ${generosText || "-"}
            </p>
            <p style="margin:0 0 4px 0; font-size:0.85rem;">
              <strong>Desarrollador(es):</strong> ${devText}
            </p>
            <p style="margin:0; font-size:0.85rem;">
              <strong>Editora(s):</strong> ${pubText}
            </p>
          </div>
        </div>
      </div>
    </div>
  `;
}



async function loadSteamTopGames() {
  btnLoadTopSteam.disabled = true;
  btnReloadTopSteam.disabled = true;

  try {
    const res = await fetch(STEAM_TOP_ENDPOINT);
    if (!res.ok) {
      throw new Error("Error al obtener el Top de Steam.");
    }

    const data = await res.json();
    const games = data.games || data; 

    renderSteamTopTable(games);
    showSteamToast("Top de Steam cargado correctamente.");
  } catch (error) {
    console.error(error);
    showSteamToast(error.message || "No se pudo cargar el Top de Steam.", "error");
  } finally {
    btnLoadTopSteam.disabled = false;
    btnReloadTopSteam.disabled = false;
  }
}

function renderSteamTopTable(games) {
  steamTopTableBody.innerHTML = "";

  if (!games || games.length === 0) {
    steamTopEmptyText.style.display = "block";
    return;
  }

  steamTopEmptyText.style.display = "none";

  games.forEach((g, index) => {
    const appid = g.appid ?? g.appID ?? g.steam_appid ?? "-";
    const rank =
      g.rank ??
      g.score ??
      (typeof g["rank"] !== "undefined" ? g["rank"] : index + 1);
    const name =
      g.name ??
      g.title ??
      g["name"] ??
      `Juego #${appid}`;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${rank ?? index + 1}</td>
      <td>${appid}</td>
      <td>${name}</td>
      <td>
        <div class="table-actions">
          <button
            class="btn btn-sm btn-outline"
            data-action="steam-detail"
            data-appid="${appid}"
          >
            Detalle
          </button>
        </div>
      </td>
    `;
    steamTopTableBody.appendChild(tr);
  });
}


async function loadGameDetailsByAppId(appid) {
  if (!appid) {
    showSteamToast("Debes ingresar un AppID válido.", "error");
    return;
  }

  btnSearchAppid.disabled = true;

  try {
    const res = await fetch(STEAM_DETAILS_ENDPOINT(appid));
    if (!res.ok) {
      if (res.status === 404) {
        showSteamToast("Juego no encontrado en la API de Steam.", "error");
      } else {
        showSteamToast("Error al consultar detalles del juego.", "error");
      }
      steamGameDetailContainer.innerHTML = `
        <p class="text-muted">
          No se pudieron obtener los detalles para AppID=${appid}.
        </p>
      `;
      return;
    }

    const detail = await res.json();
    renderSteamDetail(detail);
    showSteamToast(`Detalles cargados para AppID ${appid}.`);
  } catch (error) {
    console.error(error);
    showSteamToast(error.message || "No se pudieron cargar los detalles.", "error");
  } finally {
    btnSearchAppid.disabled = false;
  }
}


btnLoadTopSteam.addEventListener("click", () => {
  loadSteamTopGames();
});

btnReloadTopSteam.addEventListener("click", () => {
  loadSteamTopGames();
});

steamSearchForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const appidValue = steamAppidInput.value ? Number(steamAppidInput.value) : null;
  loadGameDetailsByAppId(appidValue);
});

steamTopTableBody.addEventListener("click", (e) => {
  const button = e.target.closest("button");
  if (!button) return;

  const action = button.dataset.action;
  const appid = button.dataset.appid;

  if (action === "steam-detail" && appid) {
    loadGameDetailsByAppId(appid);
  }
});


document.addEventListener("DOMContentLoaded", () => {
  steamTopEmptyText.style.display = "block";
});
