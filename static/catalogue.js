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
// BADGE AND ICON CONFIGURATION
// Color-coded badges for each vehicle type
// ============================================================
const typeBadgeConfig = {
    "SUV":       { label: "SUV",       color: "#2F6B4A" },
    "Sportive":  { label: "Sportive",  color: "#A63A3A" },
    "Berline":   { label: "Berline",   color: "#2F4A6B" },
    "Coupé":     { label: "Coupé",     color: "#6B4A2F" },
    "Cabriolet": { label: "Cabriolet", color: "#7A4A8B" },
};

// Emoji icons mapped to fuel types
const fuelIcons = {
    "Essence":    "🔴",
    "Electrique": "🔋",
    "Hybride":    "🌿",
    "Diesel":     "⚫"
};

// Rotating icons for the horsepower pill to add visual variety
const hpIcons = ["⚡", "💨", "🏎️", "🔥", "⚡"];

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
    // Clear the existing grid content
    grid.innerHTML = "";
    noResults.style.display = "none";

    // Show the no-results message if the filtered list is empty
    if (carArray.length === 0) {
        noResults.style.display = "block";
        resultsCount.textContent = "";
        return;
    }

    // Update the result counter with correct singular/plural form
    resultsCount.textContent = `${carArray.length} véhicule${carArray.length > 1 ? "s" : ""} disponible${carArray.length > 1 ? "s" : ""}`;

    // Build and append a card for each vehicle
    carArray.forEach((car, index) => {
        // Get badge config or fall back to a default grey badge
        const badge = typeBadgeConfig[car.type] || { label: car.type, color: "#555" };
        // Get fuel icon or fall back to a generic fuel pump emoji
        const fuelIcon = fuelIcons[car.fuel] || "⛽";
        // Cycle through HP icons using modulo to avoid repetition
        const hpIcon = hpIcons[index % hpIcons.length];

        const card = document.createElement("div");
        // animate-in class triggers the scroll-based fade-in animation
        card.className = "car-card catalogue-card animate-in";

        // Inject the card HTML with vehicle data
        card.innerHTML = `
            <div class="car-img">
                <img src="/static/${car.image}" alt="${car.brand} ${car.model}" loading="lazy">
                <!-- Color-coded type badge positioned over the image -->
                <span class="car-type-badge" style="background:${badge.color}">${badge.label}</span>
            </div>
            <div class="car-card-body">
                <h3 class="car-title">${car.brand} ${car.model}</h3>
                <p class="car-version">${car.modelVersion || ""}</p>
                <!-- Spec pills showing horsepower, fuel type and year -->
                <div class="car-card-specs">
                    <span class="car-spec-pill">${hpIcon} ${car.hp} ch</span>
                    <span class="car-spec-pill">${fuelIcon} ${car.fuel}</span>
                    <span class="car-spec-pill">📅 ${car.year}</span>
                </div>
                <!-- Footer with price and arrow CTA -->
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
    // refreshCursorEvents is defined globally in base.html
    window.refreshCursorEvents?.();

    // Re-trigger scroll animations on the newly injected cards
    // refreshAnimations is defined globally in base.html
    window.refreshAnimations?.();
}

// ============================================================
// BRAND FILTER — onChange
// When a brand is selected, fetch its models from the Flask API
// and populate the model dropdown
// Resets and disables the model select if no brand is chosen
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
// Sends the current filter values to the Flask /filter_cars
// endpoint via POST and re-renders the grid with the results
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
// Clears all filter selections and restores the full vehicle list
// ============================================================
resetBtn.addEventListener("click", () => {
    // Reset all filter dropdowns to their default values
    brandSelect.value = "";
    modelSelect.innerHTML = `<option value="">Tous les modèles</option>`;
    modelSelect.disabled = true;
    budgetSelect.value = "";
    // Re-render the grid with the complete unfiltered vehicle list
    renderGrid(getAllCars());
});

// ============================================================
// PAGE LOAD
// Renders the full vehicle grid on initial page load
// using the data embedded in the page by Flask
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    renderGrid(getAllCars());
});