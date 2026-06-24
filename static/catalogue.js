// ============================================================
// CATALOGUE.JS — Catalogue Page
// Handles the vehicle grid rendering and filter functionality
// on the catalogue page — no carousel, no autoplay
// Cards are injected dynamically into the DOM after filtering
// ============================================================

// ============================================================
// DOM ELEMENT REFERENCES
// ============================================================
const brandSelect = document.getElementById("brand-filter");
const modelSelect = document.getElementById("model-filter");
const budgetSelect = document.getElementById("budget-filter");
const searchBtn = document.getElementById("search-btn");
const resetBtn = document.getElementById("reset-btn");
const grid = document.getElementById("catalogue-grid");
const noResults = document.getElementById("no-results");
const resultsCount = document.getElementById("results-count");

// ============================================================
// BADGE CONFIGURATION
// Color-coded badges for each vehicle type
// ============================================================
const typeBadgeConfig = {
    "SUV":       { label: "SUV",       color: "#2F6B4A" },
    "Sportive":  { label: "Sportive",  color: "#A63A3A" },
    "Berline":   { label: "Berline",   color: "#2F4A6B" },
    "Coupé":     { label: "Coupé",     color: "#6B4A2F" },
    "Cabriolet": { label: "Cabriolet", color: "#7A4A8B" },
};

// ============================================================
// GET ALL CARS FROM PAGE
// Reads the full vehicle list from the JSON script tag
// injected into the catalogue page by Flask via Jinja2
// Returns an empty array if parsing fails
// ============================================================
function getAllCars() {
    try {
        return JSON.parse(document.getElementById("carsJson").textContent);
    } catch(e) {
        return [];
    }
}

// ============================================================
// RENDER GRID
// Clears the grid and injects a card for each vehicle
// Shows a no-results message if the array is empty
// Updates the result counter with the number of vehicles found
// ============================================================
function renderGrid(carArray) {
    grid.innerHTML = "";
    noResults.style.display = "none";

    if (carArray.length === 0) {
        noResults.style.display = "block";
        resultsCount.textContent = "";
        return;
    }

    // Update result counter with correct singular/plural form
    resultsCount.textContent = `${carArray.length} véhicule${carArray.length > 1 ? "s" : ""} disponible${carArray.length > 1 ? "s" : ""}`;

    carArray.forEach((car) => {
        // Get badge config or fall back to a default grey badge
        const badge = typeBadgeConfig[car.type] || { label: car.type, color: "#555" };

        const card = document.createElement("div");
        card.className = "car-card catalogue-card animate-in";

        // Build card HTML — no emojis, clean text only
        card.innerHTML = `
            <div class="car-img">
                <img src="/static/${car.image}" alt="${car.brand} ${car.model}" loading="lazy">
                <span class="car-type-badge" style="background:${badge.color}">${badge.label}</span>
            </div>
            <div class="car-card-body">
                <h3 class="car-title">${car.brand} ${car.model}</h3>
                <p class="car-version">${car.modelVersion || ""}</p>
                <div class="car-card-specs">
                    <span class="car-spec-pill">${car.hp} ch</span>
                    <span class="car-spec-pill">${car.fuel}</span>
                    <span class="car-spec-pill">${car.year}</span>
                </div>
                <div class="car-card-footer">
                    <span class="car-price-tag">${car.price.toLocaleString('fr-FR')} €</span>
                    <span class="car-card-cta">Voir →</span>
                </div>
            </div>
        `;

        // Navigate to the vehicle detail page on card click
        card.addEventListener("click", () => {
            window.location.href = "/car/" + car.id;
        });

        grid.appendChild(card);
    });

    // Refresh cursor hover events on the newly injected cards
    window.refreshCursorEvents?.();
    // Re-trigger scroll animations on the newly injected cards
    window.refreshAnimations?.();
}

// ============================================================
// BRAND FILTER — onChange
// Fetches models from Flask API when a brand is selected
// Resets and disables model select if no brand is chosen
// ============================================================
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
        opt.value = m;
        opt.textContent = m;
        modelSelect.appendChild(opt);
    });
});

// ============================================================
// SEARCH BUTTON — onClick
// Sends filter values to Flask API and re-renders the grid
// ============================================================
searchBtn.addEventListener("click", async () => {
    const res = await fetch("/filter_cars", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            brand: brandSelect.value,
            model: modelSelect.value,
            budget: budgetSelect.value
        })
    });
    renderGrid(await res.json());
});

// ============================================================
// RESET BUTTON — onClick
// Clears all filters and restores the full vehicle list
// ============================================================
resetBtn.addEventListener("click", () => {
    brandSelect.value = "";
    modelSelect.innerHTML = `<option value="">Tous les modèles</option>`;
    modelSelect.disabled = true;
    budgetSelect.value = "";
    renderGrid(getAllCars());
});

// ============================================================
// PAGE LOAD
// Renders the full vehicle grid on initial page load
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    renderGrid(getAllCars());
});