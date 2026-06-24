function chunkArray(arr, size) {
    const result = [];
    for (let i = 0; i < arr.length; i += size) {
        result.push(arr.slice(i, i + size));
    }
    return result;
}
function calculerCaution(prix) { return Math.round(prix * 0.05); }
function filterCars(cars, { brand = "", model = "", budget = "" } = {}) {
    let f = cars;
    if (brand) f = f.filter(c => c.brand === brand);
    if (model) f = f.filter(c => c.model === model);
    if (budget === "low") f = f.filter(c => c.price < 100000);
    if (budget === "mid") f = f.filter(c => c.price >= 100000 && c.price <= 1000000);
    if (budget === "high") f = f.filter(c => c.price > 1000000);
    return f;
}
function getBrands(cars) { return [...new Set(cars.map(c => c.brand))].sort(); }
function getModels(cars, brand) { return [...new Set(cars.filter(c => c.brand === brand).map(c => c.model))].sort(); }
const mockCars = [
    { id:1, brand:"Lamborghini", model:"Urus",    price:250900, year:2021 },
    { id:2, brand:"Lamborghini", model:"Urus",    price:200500, year:2020 },
    { id:3, brand:"Ferrari",     model:"488",     price:229000, year:2017 },
    { id:4, brand:"Porsche",     model:"911",     price:200000, year:2022 },
    { id:5, brand:"Porsche",     model:"Cayenne", price:120000, year:2021 },
    { id:6, brand:"McLaren",     model:"720S",    price:250000, year:2021 },
    { id:7, brand:"BMW",         model:"X5",      price:90000,  year:2019 },
    { id:8, brand:"Bugatti",     model:"Chiron",  price:3000000,year:2020 },
    { id:9, brand:"Porsche",     model:"Taycan",  price:220000, year:2022 },
];
describe("chunkArray", () => {
    test("pages egales", () => { expect(chunkArray([1,2,3,4,5,6],3)).toEqual([[1,2,3],[4,5,6]]); });
    test("reste derniere page", () => { expect(chunkArray([1,2,3,4,5,6,7],3)).toEqual([[1,2,3],[4,5,6],[7]]); });
    test("tableau vide", () => { expect(chunkArray([],3)).toEqual([]); });
    test("taille 1", () => { expect(chunkArray([1,2,3],1)).toEqual([[1],[2],[3]]); });
});
describe("calculerCaution", () => {
    test("Bugatti 150000", () => { expect(calculerCaution(3000000)).toBe(150000); });
    test("McLaren 12500", () => { expect(calculerCaution(250000)).toBe(12500); });
    test("Porsche 10000", () => { expect(calculerCaution(200000)).toBe(10000); });
    test("toujours 5 pourcent", () => { mockCars.forEach(c => { expect(calculerCaution(c.price)).toBe(Math.round(c.price*0.05)); }); });
});
describe("filterCars", () => {
    test("par marque", () => { const r = filterCars(mockCars,{brand:"Porsche"}); expect(r.every(c=>c.brand==="Porsche")).toBe(true); expect(r.length).toBe(3); });
    test("budget low", () => { const r = filterCars(mockCars,{budget:"low"}); expect(r.every(c=>c.price<100000)).toBe(true); });
    test("budget mid", () => { const r = filterCars(mockCars,{budget:"mid"}); expect(r.every(c=>c.price>=100000&&c.price<=1000000)).toBe(true); });
    test("budget high", () => { const r = filterCars(mockCars,{budget:"high"}); expect(r.every(c=>c.price>1000000)).toBe(true); });
    test("combine marque modele", () => { const r = filterCars(mockCars,{brand:"Lamborghini",model:"Urus"}); expect(r.length).toBe(2); });
    test("aucun resultat", () => { expect(filterCars(mockCars,{brand:"Ferrari",budget:"low"})).toEqual([]); });
    test("sans critere tout", () => { expect(filterCars(mockCars).length).toBe(mockCars.length); });
});
describe("getBrands", () => {
    test("sans doublons", () => { const b = getBrands(mockCars); expect(b.length).toBe(new Set(b).size); });
    test("tries", () => { const b = getBrands(mockCars); expect(b).toEqual([...b].sort()); });
    test("contient Ferrari", () => { expect(getBrands(mockCars)).toContain("Ferrari"); });
});
describe("getModels", () => {
    test("sans doublons", () => { const m = getModels(mockCars,"Lamborghini"); expect(m.length).toBe(new Set(m).size); });
    test("tries", () => { const m = getModels(mockCars,"Porsche"); expect(m).toEqual([...m].sort()); });
    test("marque inexistante", () => { expect(getModels(mockCars,"Pagani")).toEqual([]); });
});
