const brandSelect = document.getElementById("brand-filter");
const modelSelect = document.getElementById("model-filter");
const budgetSelect = document.getElementById("budget-filter");
const searchBtn = document.getElementById("search-btn");
const resetBtn = document.getElementById("reset-btn");
const grid = document.getElementById("catalogue-grid");
const noResults = document.getElementById("no-results");
const resultsCount = document.getElementById("results-count");

const typeBadgeConfig = {
    "SUV":       { label: "SUV",       color: "#2F6B4A" },
    "Sportive":  { label: "Sportive",  color: "#A63A3A" },
    "Berline":   { label: "Berline",   color: "#2F4A6B" },
    "Coupé":     { label: "Coupé",     color: "#6B4A2F" },
    "Cabriolet": { label: "Cabriolet", color: "#7A4A8B" },
};

const fuelIcons = { "Essence": "🔴", "Electrique": "🔋", "Hybride": "🌿", "Diesel": "⚫" };
const hpIcons = ["⚡", "💨", "🏎️", "🔥", "⚡"];

function getAllCars() {
    try { return JSON.parse(document.getElementById("carsJson").textContent); }
    catch(e) { return []; }
}

function renderGrid(carArray) {
    grid.innerHTML = "";
    noResults.style.display = "none";

    if (carArray.length === 0) {
        noResults.style.display = "block";
        resultsCount.textContent = "";
        return;
    }

    resultsCount.textContent = `${carArray.length} véhicule${carArray.length > 1 ? "s" : ""} disponible${carArray.length > 1 ? "s" : ""}`;

    carArray.forEach((car, index) => {
        const badge = typeBadgeConfig[car.type] || { label: car.type, color: "#555" };
        const fuelIcon = fuelIcons[car.fuel] || "⛽";
        const hpIcon = hpIcons[index % hpIcons.length];

        const card = document.createElement("div");
        card.className = "car-card catalogue-card animate-in";

        card.innerHTML = `
            <div class="car-img">
                <img src="/static/${car.image}" alt="${car.brand} ${car.model}" loading="lazy">
                <span class="car-type-badge" style="background:${badge.color}">${badge.label}</span>
            </div>
            <div class="car-card-body">
                <h3 class="car-title">${car.brand} ${car.model}</h3>
                <p class="car-version">${car.modelVersion || ""}</p>
                <div class="car-card-specs">
                    <span class="car-spec-pill">${hpIcon} ${car.hp} ch</span>
                    <span class="car-spec-pill">${fuelIcon} ${car.fuel}</span>
                    <span class="car-spec-pill">📅 ${car.year}</span>
                </div>
                <div class="car-card-footer">
                    <span class="car-price-tag">${car.price.toLocaleString('fr-FR')} €</span>
                    <span class="car-card-cta">Voir →</span>
                </div>
            </div>
        `;

        card.addEventListener("click", () => { window.location.href = "/car/" + car.id; });
        grid.appendChild(card);
    });

    // Rafraîchir curseur et animations sur les nouvelles cartes
    window.refreshCursorEvents?.();
    window.refreshAnimations?.();
}

brandSelect.addEventListener("change", async () => {
    if (!brandSelect.value) {
        modelSelect.innerHTML = `<option value="">Tous les modèles</option>`;
        modelSelect.disabled = true;
        return;
    }
    const res = await fetch("/get_models?brand=" + encodeURIComponent(brandSelect.value));
    const models = await res.json();
    modelSelect.disabled = false;
    modelSelect.innerHTML = `<option value="">Tous les modèles</option>`;
    models.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m; opt.textContent = m;
        modelSelect.appendChild(opt);
    });
});

searchBtn.addEventListener("click", async () => {
    const res = await fetch("/filter_cars", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ brand: brandSelect.value, model: modelSelect.value, budget: budgetSelect.value })
    });
    renderGrid(await res.json());
});

resetBtn.addEventListener("click", () => {
    brandSelect.value = "";
    modelSelect.innerHTML = `<option value="">Tous les modèles</option>`;
    modelSelect.disabled = true;
    budgetSelect.value = "";
    renderGrid(getAllCars());
});

document.addEventListener("DOMContentLoaded", () => { renderGrid(getAllCars()); });