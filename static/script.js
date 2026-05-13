// -------------------------------
// DOM ELEMENTS
// -------------------------------
const brandSelect = document.getElementById("brand-filter");
const modelSelect = document.getElementById("model-filter");
const budgetSelect = document.getElementById("budget-filter");
const searchBtn = document.getElementById("search-btn");

const carTrack = document.getElementById("cars-page-container");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
const dotsContainer = document.getElementById("carousel-dots");
const counterEl = document.getElementById("carousel-counter");

// Carrousel state
let pages = [];
let currentPage = 0;
const PAGE_SIZE = 3;
let autoTimer = null;
const AUTO_DELAY = 7000;

// ------------------------------------------------
// CHUNK ARRAY
// ------------------------------------------------
function chunkArray(arr, size) {
    const result = [];
    for (let i = 0; i < arr.length; i += size) {
        result.push(arr.slice(i, i + size));
    }
    return result;
}

// ------------------------------------------------
// INITIAL LOAD
// ------------------------------------------------
async function loadBrands() {
    const res = await fetch("/get_brands");
    const brands = await res.json();
    brandSelect.innerHTML = `<option value="">Toutes les marques</option>`;
    brands.forEach(b => {
        const opt = document.createElement("option");
        opt.value = b;
        opt.textContent = b;
        brandSelect.appendChild(opt);
    });
}

function getInitialCarsFromPage() {
    try {
        return JSON.parse(document.getElementById("carsJson").textContent);
    } catch (e) {
        return [];
    }
}

// ------------------------------------------------
// BUILD CAROUSEL
// ------------------------------------------------
function buildCarouselWithCars(carArray) {
    pages = chunkArray(carArray, PAGE_SIZE);
    if (pages.length === 0) pages = [[]];
    currentPage = 0;
    buildDots();
    renderCurrentPage(true);
    startAutoPlay();
}

// ------------------------------------------------
// DOTS
// ------------------------------------------------
function buildDots() {
    dotsContainer.innerHTML = "";
    pages.forEach((_, i) => {
        const dot = document.createElement("button");
        dot.className = "carousel-dot" + (i === 0 ? " active" : "");
        dot.setAttribute("aria-label", `Page ${i + 1}`);
        dot.addEventListener("click", () => goToPage(i));
        dotsContainer.appendChild(dot);
    });
}

function updateDots() {
    document.querySelectorAll(".carousel-dot").forEach((dot, i) => {
        dot.classList.toggle("active", i === currentPage);
    });
}

function updateCounter() {
    if (counterEl) {
        counterEl.textContent = `${currentPage + 1} / ${pages.length}`;
    }
}

// ------------------------------------------------
// RENDER PAGE WITH SLIDE ANIMATION
// ------------------------------------------------
function renderCurrentPage(instant = false) {
    const pageCars = pages[currentPage];

    if (pageCars.length === 0) {
        carTrack.innerHTML = "<p style='text-align:center;font-size:1.2rem;padding:40px;'>Aucun véhicule trouvé.</p>";
        updateDots();
        updateCounter();
        return;
    }

    const typeBadgeConfig = {
        "SUV":       { label: "SUV",       color: "#2F6B4A" },
        "Sportive":  { label: "Sportive",  color: "#A63A3A" },
        "Berline":   { label: "Berline",   color: "#2F4A6B" },
        "Coupé":     { label: "Coupé",     color: "#6B4A2F" },
        "Cabriolet": { label: "Cabriolet", color: "#7A4A8B" },
    };

    const fuelIcons = {
        "Essence":    "🔴",
        "Electrique": "🔋",
        "Hybride":    "🌿",
        "Diesel":     "⚫",
    };

    const hpIcons = ["⚡", "💨", "🏎️", "🔥", "⚡"];

    const newGrid = document.createElement("div");
    newGrid.className = "carousel-grid";

    pageCars.forEach((car, index) => {
        const badge = typeBadgeConfig[car.type] || { label: car.type, color: "#555" };
        const fuelIcon = fuelIcons[car.fuel] || "⛽";
        const hpIcon = hpIcons[index % hpIcons.length];

        const card = document.createElement("div");
        card.className = "car-card";

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

        card.addEventListener("click", () => {
            window.location.href = "/car/" + car.id;
        });

        newGrid.appendChild(card);
    });

    if (instant) {
        carTrack.innerHTML = "";
        carTrack.appendChild(newGrid);
    } else {
        const direction = (carTrack._lastDirection || 1);
        const oldGrid = carTrack.firstChild;
        if (oldGrid) {
            oldGrid.style.transition = "transform 0.45s cubic-bezier(0.4,0,0.2,1), opacity 0.45s";
            oldGrid.style.transform = `translateX(${direction === 1 ? '-100%' : '100%'})`;
            oldGrid.style.opacity = "0";
        }
        newGrid.style.transform = `translateX(${direction === 1 ? '100%' : '-100%'})`;
        newGrid.style.opacity = "0";
        carTrack.appendChild(newGrid);
        newGrid.getBoundingClientRect();
        newGrid.style.transition = "transform 0.45s cubic-bezier(0.4,0,0.2,1), opacity 0.45s";
        newGrid.style.transform = "translateX(0)";
        newGrid.style.opacity = "1";
        setTimeout(() => {
            if (oldGrid && oldGrid.parentNode === carTrack) {
                carTrack.removeChild(oldGrid);
            }
        }, 460);
    }

    updateDots();
    updateCounter();
}

// ------------------------------------------------
// NAVIGATION
// ------------------------------------------------
function goToPage(index, direction = null) {
    if (index === currentPage) return;
    carTrack._lastDirection = direction !== null ? direction : (index > currentPage ? 1 : -1);
    currentPage = index;
    renderCurrentPage();
    resetAutoPlay();
}

nextBtn.addEventListener("click", () => {
    const next = (currentPage + 1) % pages.length;
    goToPage(next, 1);
});

prevBtn.addEventListener("click", () => {
    const prev = (currentPage - 1 + pages.length) % pages.length;
    goToPage(prev, -1);
});

// ------------------------------------------------
// AUTOPLAY
// ------------------------------------------------
function startAutoPlay() {
    stopAutoPlay();
    autoTimer = setInterval(() => {
        const next = (currentPage + 1) % pages.length;
        goToPage(next, 1);
    }, AUTO_DELAY);
}

function stopAutoPlay() {
    if (autoTimer) {
        clearInterval(autoTimer);
        autoTimer = null;
    }
}

function resetAutoPlay() {
    startAutoPlay();
}

// Pause au survol
document.querySelector(".carousel-wrapper")?.addEventListener("mouseenter", stopAutoPlay);
document.querySelector(".carousel-wrapper")?.addEventListener("mouseleave", startAutoPlay);

// ------------------------------------------------
// FILTRES
// ------------------------------------------------
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

modelSelect.addEventListener("mousedown", (e) => {
    if (!brandSelect.value) {
        alert("Veuillez choisir une marque avant un modèle.");
        e.preventDefault();
    }
});

searchBtn.addEventListener("click", async () => {
    const filters = {
        brand: brandSelect.value,
        model: modelSelect.value,
        budget: budgetSelect.value,
    };
    const res = await fetch("/filter_cars", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters)
    });
    const filteredCars = await res.json();
    buildCarouselWithCars(filteredCars);
});

// ------------------------------------------------
// ON PAGE LOAD
// ------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadBrands();
    const initialCars = getInitialCarsFromPage();
    buildCarouselWithCars(initialCars);
});