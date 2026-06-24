// ============================================================
// SCRIPT.JS — Home Page Carousel
// Handles the vehicle carousel on the home page
// Includes slide animations, autoplay, dot navigation
// and filter functionality via the Flask API
// ============================================================

// ============================================================
// DOM ELEMENT REFERENCES
// ============================================================
const brandSelect = document.getElementById("brand-filter");
const modelSelect = document.getElementById("model-filter");
const budgetSelect = document.getElementById("budget-filter");
const searchBtn = document.getElementById("search-btn");

const carTrack = document.getElementById("cars-page-container");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
const dotsContainer = document.getElementById("carousel-dots");
const counterEl = document.getElementById("carousel-counter");

// ============================================================
// CAROUSEL STATE
// pages — array of page arrays, each containing PAGE_SIZE cars
// currentPage — index of the currently displayed page
// PAGE_SIZE — number of cars visible per page (1 row of 3)
// autoTimer — reference to the autoplay interval
// AUTO_DELAY — milliseconds between automatic page transitions
// ============================================================
let pages = [];
let currentPage = 0;
const PAGE_SIZE = 3;
let autoTimer = null;
const AUTO_DELAY = 7000;

// ============================================================
// CHUNK ARRAY
// Splits a flat array into an array of pages of a given size
// Example: chunkArray([1,2,3,4,5,6], 3) → [[1,2,3],[4,5,6]]
// ============================================================
function chunkArray(arr, size) {
    const result = [];
    for (let i = 0; i < arr.length; i += size) {
        result.push(arr.slice(i, i + size));
    }
    return result;
}

// ============================================================
// INITIAL DATA LOAD
// Fetches the brand list from the Flask API on page load
// and populates the brand filter dropdown
// ============================================================
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

// Reads the initial car list from the JSON script tag
// injected into the page by Flask via Jinja2
function getInitialCarsFromPage() {
    try {
        return JSON.parse(document.getElementById("carsJson").textContent);
    } catch (e) {
        return [];
    }
}

// ============================================================
// BUILD CAROUSEL
// Initializes the carousel with a given array of vehicles
// Resets the page index, rebuilds dots and starts autoplay
// ============================================================
function buildCarouselWithCars(carArray) {
    pages = chunkArray(carArray, PAGE_SIZE);
    // Ensure at least one empty page to avoid errors
    if (pages.length === 0) pages = [[]];
    currentPage = 0;
    buildDots();
    renderCurrentPage(true);
    startAutoPlay();
}

// ============================================================
// NAVIGATION DOTS
// Creates one dot button per page and appends them to the
// dots container — clicking a dot navigates to that page
// ============================================================
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

// Updates the active state of all dots to match the current page
function updateDots() {
    document.querySelectorAll(".carousel-dot").forEach((dot, i) => {
        dot.classList.toggle("active", i === currentPage);
    });
}

// Updates the page counter text (e.g. "2 / 4")
function updateCounter() {
    if (counterEl) {
        counterEl.textContent = `${currentPage + 1} / ${pages.length}`;
    }
}

// ============================================================
// RENDER CURRENT PAGE WITH SLIDE ANIMATION
// Builds a new grid of car cards and animates it into view
// instant=true skips the animation (used on first load)
// ============================================================
function renderCurrentPage(instant = false) {
    const pageCars = pages[currentPage];

    // Show an empty state message if no vehicles are found
    if (pageCars.length === 0) {
        carTrack.innerHTML = "<p style='text-align:center;font-size:1.2rem;padding:40px;'>Aucun véhicule trouvé.</p>";
        updateDots();
        updateCounter();
        return;
    }

    // Color configuration for each vehicle type badge
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
        "Diesel":     "⚫",
    };

    // Rotating icons for the horsepower pill to add visual variety
    const hpIcons = ["⚡", "💨", "🏎️", "🔥", "⚡"];

    // Create a new grid element to hold the car cards
    const newGrid = document.createElement("div");
    newGrid.className = "carousel-grid";

    // Build a card for each vehicle on the current page
    pageCars.forEach((car, index) => {
        // Get badge config or fall back to a default grey badge
        const badge = typeBadgeConfig[car.type] || { label: car.type, color: "#555" };
        // Get fuel icon or fall back to a generic fuel pump emoji
        const fuelIcon = fuelIcons[car.fuel] || "⛽";
        // Cycle through HP icons using modulo
        const hpIcon = hpIcons[index % hpIcons.length];

        const card = document.createElement("div");
        card.className = "car-card";

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

        newGrid.appendChild(card);
    });

    if (instant) {
        // Skip animation — directly replace the content
        carTrack.innerHTML = "";
        carTrack.appendChild(newGrid);
    } else {
        // Slide animation — 1 = slide left, -1 = slide right
        const direction = (carTrack._lastDirection || 1);
        const oldGrid = carTrack.firstChild;

        // Slide the old grid out of view
        if (oldGrid) {
            oldGrid.style.transition = "transform 0.45s cubic-bezier(0.4,0,0.2,1), opacity 0.45s";
            oldGrid.style.transform = `translateX(${direction === 1 ? '-100%' : '100%'})`;
            oldGrid.style.opacity = "0";
        }

        // Position the new grid off-screen before animating it in
        newGrid.style.transform = `translateX(${direction === 1 ? '100%' : '-100%'})`;
        newGrid.style.opacity = "0";
        carTrack.appendChild(newGrid);

        // Force a reflow to ensure the initial position is applied
        newGrid.getBoundingClientRect();

        // Animate the new grid into view
        newGrid.style.transition = "transform 0.45s cubic-bezier(0.4,0,0.2,1), opacity 0.45s";
        newGrid.style.transform = "translateX(0)";
        newGrid.style.opacity = "1";

        // Remove the old grid after the animation completes
        setTimeout(() => {
            if (oldGrid && oldGrid.parentNode === carTrack) {
                carTrack.removeChild(oldGrid);
            }
        }, 460);
    }

    updateDots();
    updateCounter();
}

// ============================================================
// PAGE NAVIGATION
// Navigates to a specific page index with optional direction
// Direction: 1 = forward (slide left), -1 = backward (slide right)
// ============================================================
function goToPage(index, direction = null) {
    // Do nothing if already on the requested page
    if (index === currentPage) return;
    // Infer direction from page index if not explicitly provided
    carTrack._lastDirection = direction !== null ? direction : (index > currentPage ? 1 : -1);
    currentPage = index;
    renderCurrentPage();
    resetAutoPlay();
}

// Navigate to the next page (wraps around to the first page)
nextBtn.addEventListener("click", () => {
    const next = (currentPage + 1) % pages.length;
    goToPage(next, 1);
});

// Navigate to the previous page (wraps around to the last page)
prevBtn.addEventListener("click", () => {
    const prev = (currentPage - 1 + pages.length) % pages.length;
    goToPage(prev, -1);
});

// ============================================================
// AUTOPLAY
// Automatically advances to the next page every AUTO_DELAY ms
// Stops when the user interacts and restarts after interaction
// ============================================================
function startAutoPlay() {
    stopAutoPlay();
    autoTimer = setInterval(() => {
        const next = (currentPage + 1) % pages.length;
        goToPage(next, 1);
    }, AUTO_DELAY);
}

// Clears the autoplay interval
function stopAutoPlay() {
    if (autoTimer) {
        clearInterval(autoTimer);
        autoTimer = null;
    }
}

// Restarts autoplay after user interaction
function resetAutoPlay() {
    startAutoPlay();
}

// Pause autoplay when the user hovers over the carousel
document.querySelector(".carousel-wrapper")?.addEventListener("mouseenter", stopAutoPlay);
// Resume autoplay when the user moves away from the carousel
document.querySelector(".carousel-wrapper")?.addEventListener("mouseleave", startAutoPlay);

// ============================================================
// FILTER INTERACTIONS
// ============================================================

// When a brand is selected, fetch its models from the Flask API
// and populate the model dropdown
brandSelect.addEventListener("change", async () => {
    if (!brandSelect.value) {
        // Reset and disable the model select if no brand is chosen
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

// Prevent opening the model dropdown if no brand has been selected
modelSelect.addEventListener("mousedown", (e) => {
    if (!brandSelect.value) {
        alert("Veuillez choisir une marque avant un modèle.");
        e.preventDefault();
    }
});

// Send filter criteria to the Flask API and rebuild the carousel
// with the returned filtered vehicle list
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

// ============================================================
// PAGE LOAD
// Initializes the brand dropdown and builds the carousel
// with the vehicle data embedded in the page by Flask
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    loadBrands();
    const initialCars = getInitialCarsFromPage();
    buildCarouselWithCars(initialCars);
});