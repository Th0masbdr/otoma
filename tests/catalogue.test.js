function chunkArray(arr, size) {
    const result = [];
    for (let i = 0; i < arr.length; i += size) {
        result.push(arr.slice(i, i + size));
    }
    return result;
}

function calculerCaution(prix) {
    return Math.round(prix * 0.05);
}

function filterCars(cars, { brand = "", model = "", budget = "" } = {}) {
    let filtered = cars;
    if (brand) filtered = filtered.filter(c => c.brand === brand);
    if (model) filtered = filtered.filter(c => c.model === model);
    if (budget === "low")  filtered = filtered.filter(c => c.price < 100000);
    if (budget === "mid")  filtered = filtered.filter(c => c.price >= 100000 && c.price <= 1000000);
    if (budget === "high") filtered = filtered.filter(c => c.price > 1000000);
    return filtered;
}

function getBrands(cars) {
    return [...new Set(cars.map(c => c.brand))].sort();
}

function getModels(cars, brand) {
    return [...new Set(cars.filter(c => c.brand === brand).map(c => c.model))].sort();
}

function formatPrice(price) {
    return price.toLocaleString("fr-FR") + " €";
}

const mockCars = [
    { id: 1, brand: "Lamborghini", model: "Urus",    type: "SUV",      price: 250900, hp: 650, fuel: "Essence",    year: 2021 },
    { id: 2, brand: "Lamborghini", model: "Urus",    type: "SUV",      price: 200500, hp: 650, fuel: "Essence",    year: 2020 },
    { id: 3, brand: "Ferrari",     model: "488",     type: "Sportive", price: 229000, hp: 670, fuel: "Essence",    year: 2017 },
    { id: 4, brand: "Porsche",     model: "911",     type: "Sportive", price: 200000, hp: 650, fuel: "Essence",    year: 2022 },
    { id: 5, brand: "Porsche",     model: "Cayenne", type: "SUV",      price: 120000, hp: 550, fuel: "Essence",    year: 2021 },
    { id: 6, brand: "McLaren",     model: "720S",    type: "Sportive", price: 250000, hp: 710, fuel: "Essence",    year: 2021 },
    { id: 7, brand: "BMW",         model: "X5",      type: "SUV",      price: 90000,  hp: 530, fuel: "Essence",    year: 2019 },
    { id: 8, brand: "Bugatti",     model: "Chiron",  type: "Sportive", price: 3000000,hp: 1500,fuel: "Essence",    year: 2020 },
    { id: 9, brand: "Porsche",     model: "Taycan",  type: "Berline",  price: 220000, hp: 761, fuel: "Electrique", year: 2022 },
];

describe("chunkArray()", () => {
    test("decoupe un tableau en pages egales", () => {
        expect(chunkArray([1,2,3,4,5,6], 3)).toEqual([[1,2,3],[4,5,6]]);
    });
    test("gere un reste en derniere page", () => {
        expect(chunkArray([1,2,3,4,5,6,7], 3)).toEqual([[1,2,3],[4,5,6],[7]]);
    });
    test("retourne un tableau vide si entree vide", () => {
        expect(chunkArray([], 3)).toEqual([]);
    });
    test("fonctionne avec taille 1", () => {
        expect(chunkArray([1,2,3], 1)).toEqual([[1],[2],[3]]);
    });
});

describe("calculerCaution()", () => {
    test("Bugatti 3000000 caution 150000", () => {
        expect(calculerCaution(3000000)).toBe(150000);
    });
    test("McLaren 720S 250000 caution 12500", () => {
        expect(calculerCaution(250000)).toBe(12500);
    });
    test("Porsche 200000 caution 10000", () => {
        expect(calculerCaution(200000)).toBe(10000);
    });
    test("caution est toujours 5 pourcent du prix", () => {
        mockCars.forEach(car => {
            expect(calculerCaution(car.price)).toBe(Math.round(car.price * 0.05));
        });
    });
});

describe("filterCars()", () => {
    test("filtre par marque retourne uniquement cette marque", () => {
        const result = filterCars(mockCars, { brand: "Porsche" });
        expect(result.every(c => c.brand === "Porsche")).toBe(true);
        expect(result.length).toBe(3);
    });
    test("budget low retourne prix inferieur a 100000", () => {
        const result = filterCars(mockCars, { budget: "low" });
        expect(result.every(c => c.price < 100000)).toBe(true);
        expect(result.length).toBe(1);
    });
    test("budget mid retourne 100k a 1M", () => {
        const result = filterCars(mockCars, { budget: "mid" });
        expect(result.every(c => c.price >= 100000 && c.price <= 1000000)).toBe(true);
    });
    test("budget high retourne prix superieur a 1000000", () => {
        const result = filterCars(mockCars, { budget: "high" });
        expect(result.every(c => c.price > 1000000)).toBe(true);
        expect(result.length).toBe(1);
    });
    test("filtre combine marque et modele", () => {
        const result = filterCars(mockCars, { brand: "Lamborghini", model: "Urus" });
        expect(result.every(c => c.brand === "Lamborghini" && c.model === "Urus")).toBe(true);
        expect(result.length).toBe(2);
    });
    test("retourne liste vide si aucun resultat", () => {
        const result = filterCars(mockCars, { brand: "Ferrari", budget: "low" });
        expect(result).toEqual([]);
    });
    test("sans critere retourne tous les vehicules", () => {
        const result = filterCars(mockCars);
        expect(result.length).toBe(mockCars.length);
    });
});

describe("getBrands()", () => {
    test("retourne les marques sans doublons", () => {
        const brands = getBrands(mockCars);
        expect(brands.length).toBe(new Set(brands).size);
    });
    test("retourne les marques triees alphabetiquement", () => {
        const brands = getBrands(mockCars);
        expect(brands).toEqual([...brands].sort());
    });
    test("contient toutes les marques attendues", () => {
        const brands = getBrands(mockCars);
        expect(brands).toContain("Ferrari");
        expect(brands).toContain("Lamborghini");
        expect(brands).toContain("Porsche");
    });
});

describe("getModels()", () => {
    test("retourne les modeles sans doublons", () => {
        const models = getModels(mockCars, "Lamborghini");
        expect(models.length).toBe(new Set(models).size);
    });
    test("retourne les modeles tries", () => {
        const models = getModels(mockCars, "Porsche");
        expect(models).toEqual([...models].sort());
    });
    test("retourne liste vide pour marque inexistante", () => {
        const models = getModels(mockCars, "Pagani");
        expect(models).toEqual([]);
    });
});

describe("formatPrice()", () => {
    test("formate correctement un prix en euros", () => {
        expect(formatPrice(250000)).toContain("€");
    });
    test("le prix contient les chiffres corrects", () => {
        const result = formatPrice(1000000);
        expect(result.replace(/\s/g, "")).toContain("1000000");
    });
});