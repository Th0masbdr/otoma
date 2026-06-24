from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os, requests

load_dotenv()

app = Flask(__name__)

cars = [
    {"id": 1, "brand": "Lamborghini", "model": "Urus", "modelVersion": "4.0 V8 650", "type": "SUV",
     "price": 250900, "km": 19900, "fuel": "Essence", "year": 2021, "color": "Noir", "hp": 650, "transmission": "Automatique", "image": "urus1.png"},
    {"id": 2, "brand": "Lamborghini", "model": "Urus", "modelVersion": "4.0 V8 650", "type": "SUV",
     "price": 200500, "km": 39950, "fuel": "Essence", "year": 2020, "color": "Vert", "hp": 650, "transmission": "Automatique", "image": "urus2.png"},
    {"id": 3, "brand": "Ferrari", "model": "488", "modelVersion": "GTB", "type": "Sportive",
     "price": 229000, "km": 21245, "fuel": "Essence", "year": 2017, "color": "Nero Daytona", "hp": 670, "transmission": "Automatique", "image": "ferrari488.png"},
    {"id": 4, "brand": "Porsche", "model": "911", "modelVersion": "Turbo S", "type": "Sportive",
     "price": 200000, "km": 4000, "fuel": "Essence", "year": 2022, "color": "Argent", "hp": 650, "transmission": "Automatique", "image": "porsche911ts.png"},
    {"id": 5, "brand": "Porsche", "model": "Cayenne", "modelVersion": "Turbo", "type": "SUV",
     "price": 120000, "km": 15000, "fuel": "Essence", "year": 2021, "color": "Blanc", "hp": 550, "transmission": "Automatique", "image": "cayenne_turbo.png"},
    {"id": 6, "brand": "McLaren", "model": "720S", "modelVersion": "", "type": "Sportive",
     "price": 250000, "km": 8000, "fuel": "Essence", "year": 2021, "color": "Bleu", "hp": 710, "transmission": "Automatique", "image": "mclaren720s.png"},
    {"id": 7, "brand": "Aston Martin", "model": "DB11", "modelVersion": "", "type": "Coupé",
     "price": 180000, "km": 12000, "fuel": "Essence", "year": 2020, "color": "Gris", "hp": 630, "transmission": "Automatique", "image": "db11.png"},
    {"id": 8, "brand": "Bentley", "model": "Continental GT", "modelVersion": "W12", "type": "Coupé",
     "price": 200000, "km": 18000, "fuel": "Essence", "year": 2019, "color": "Noir", "hp": 635, "transmission": "Automatique", "image": "bentley_gt.png"},
    {"id": 9, "brand": "Rolls-Royce", "model": "Ghost", "modelVersion": "", "type": "Berline",
     "price": 300000, "km": 25000, "fuel": "Essence", "year": 2018, "color": "Blanc Perl", "hp": 563, "transmission": "Automatique", "image": "rr_ghost.png"},
    {"id": 10, "brand": "Mercedes", "model": "AMG GT", "modelVersion": "R", "type": "Sportive",
     "price": 150000, "km": 3000, "fuel": "Essence", "year": 2022, "color": "Gris", "hp": 585, "transmission": "Automatique", "image": "amg_gt_r.png"},
    {"id": 11, "brand": "Mercedes", "model": "G63", "modelVersion": "AMG", "type": "SUV",
     "price": 180000, "km": 20000, "fuel": "Essence", "year": 2021, "color": "Noir", "hp": 585, "transmission": "Automatique", "image": "g63.png"},
    {"id": 12, "brand": "BMW", "model": "M5", "modelVersion": "Competition", "type": "Berline",
     "price": 120000, "km": 15000, "fuel": "Essence", "year": 2020, "color": "Bleu", "hp": 625, "transmission": "Automatique", "image": "bmw_m5.png"},
    {"id": 13, "brand": "BMW", "model": "X5", "modelVersion": "M50i", "type": "SUV",
     "price": 90000, "km": 30000, "fuel": "Essence", "year": 2019, "color": "Blanc", "hp": 530, "transmission": "Automatique", "image": "x5m50i.png"},
    {"id": 14, "brand": "Audi", "model": "R8", "modelVersion": "V10 Plus", "type": "Sportive",
     "price": 160000, "km": 10000, "fuel": "Essence", "year": 2021, "color": "Rouge", "hp": 610, "transmission": "Automatique", "image": "audi_r8.png"},
    {"id": 15, "brand": "Audi", "model": "RS7", "modelVersion": "Sportback", "type": "Berline",
     "price": 120000, "km": 18000, "fuel": "Essence", "year": 2020, "color": "Gris", "hp": 600, "transmission": "Automatique", "image": "rs7.png"},
    {"id": 16, "brand": "Porsche", "model": "Taycan", "modelVersion": "Turbo S", "type": "Berline",
     "price": 220000, "km": 8000, "fuel": "Electrique", "year": 2022, "color": "Vert", "hp": 761, "transmission": "Automatique", "image": "taycan_ts.png"},
    {"id": 17, "brand": "Tesla", "model": "Model S", "modelVersion": "Plaid", "type": "Berline",
     "price": 130000, "km": 12000, "fuel": "Electrique", "year": 2023, "color": "Noir", "hp": 1020, "transmission": "Automatique", "image": "tesla_model_s_plaid.png"},
    {"id": 18, "brand": "McLaren", "model": "Artura", "modelVersion": "", "type": "Sportive",
     "price": 210000, "km": 5000, "fuel": "Hybride", "year": 2022, "color": "Jaune", "hp": 671, "transmission": "Automatique", "image": "mclaren_artura.png"},
    {"id": 19, "brand": "Aston Martin", "model": "DBS", "modelVersion": "Superleggera", "type": "Sportive",
     "price": 250000, "km": 7000, "fuel": "Essence", "year": 2021, "color": "Vert British", "hp": 725, "transmission": "Automatique", "image": "dbs_superleggera.png"},
    {"id": 20, "brand": "Bentley", "model": "Flying Spur", "modelVersion": "", "type": "Berline",
     "price": 180000, "km": 22000, "fuel": "Essence", "year": 2020, "color": "Gris", "hp": 626, "transmission": "Automatique", "image": "flying_spur.png"},
    {"id": 21, "brand": "Rolls-Royce", "model": "Wraith", "modelVersion": "", "type": "Coupé",
     "price": 280000, "km": 15000, "fuel": "Essence", "year": 2019, "color": "Bleu Nuit", "hp": 624, "transmission": "Automatique", "image": "wraith.png"},
    {"id": 22, "brand": "Lamborghini", "model": "Huracán", "modelVersion": "Evo", "type": "Sportive",
     "price": 300000, "km": 8000, "fuel": "Essence", "year": 2022, "color": "Orange", "hp": 640, "transmission": "Automatique", "image": "huracan_evo.png"},
    {"id": 23, "brand": "Ferrari", "model": "F8", "modelVersion": "Tributo", "type": "Sportive",
     "price": 270000, "km": 5000, "fuel": "Essence", "year": 2022, "color": "Rosso", "hp": 720, "transmission": "Automatique", "image": "f8_tributo.png"},
    {"id": 24, "brand": "Ferrari", "model": "Roma", "modelVersion": "Spyder", "type": "Coupé",
     "price": 200000, "km": 6000, "fuel": "Essence", "year": 2021, "color": "Blanc", "hp": 620, "transmission": "Automatique", "image": "roma.png"},
    {"id": 25, "brand": "Maserati", "model": "MC20", "modelVersion": "PrimaSerie", "type": "Sportive",
     "price": 240000, "km": 4000, "fuel": "Essence", "year": 2022, "color": "Bleu", "hp": 630, "transmission": "Automatique", "image": "mc20.png"},
    {"id": 26, "brand": "Bugatti", "model": "Chiron", "modelVersion": "SuperSport", "type": "Sportive",
     "price": 3000000, "km": 500, "fuel": "Essence", "year": 2020, "color": "Noir", "hp": 1500, "transmission": "Automatique", "image": "chiron.png"},
    {"id": 27, "brand": "Pagani", "model": "Huayra", "modelVersion": "R", "type": "Sportive",
     "price": 2000000, "km": 800, "fuel": "Essence", "year": 2019, "color": "Gris", "hp": 800, "transmission": "Automatique", "image": "huayra.png"},
    {"id": 28, "brand": "Koenigsegg", "model": "Agera RS", "modelVersion": "RS", "type": "Sportive",
     "price": 2500000, "km": 2000, "fuel": "Essence", "year": 2018, "color": "Rouge", "hp": 1160, "transmission": "Automatique", "image": "agera_rs.png"},
    {"id": 29, "brand": "McLaren", "model": "Senna", "modelVersion": "LM", "type": "Sportive",
     "price": 1500000, "km": 1000, "fuel": "Essence", "year": 2021, "color": "Orange", "hp": 789, "transmission": "Automatique", "image": "senna.png"},
    {"id": 30, "brand": "Lamborghini", "model": "Aventador", "modelVersion": "SVJ", "type": "Sportive",
     "price": 600000, "km": 4000, "fuel": "Essence", "year": 2021, "color": "Jaune", "hp": 770, "transmission": "Automatique", "image": "aventador_svj.png"}
]

@app.route("/")
def home():
    stats = [
        {"value": "400+", "name": "Véhicules vendus"},
        {"value": "96 %", "name": "Clients satisfaits"},
        {"value": "15 ans", "name": "d'expérience dans le luxe"},
    ]
    newest = cars[-3:][::-1]
    return render_template("index.html", cars=newest)

@app.route("/catalogue")
def catalogue():
    brands = sorted(list({c["brand"] for c in cars}))
    return render_template("catalogue.html", cars=cars, brands=brands)

@app.route("/services")
def services():
    return render_template("catalogue.html", cars=cars, brands=sorted(list({c["brand"] for c in cars})))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/test_drive")
def test_drive():
    return render_template("test_drive.html")

@app.route("/rdv")
def rdv():
    return render_template("rdv.html", title="Prendre rendez-vous")

@app.route("/sell")
def sell():
    return render_template("sell.html")

@app.route("/cookies")
def cookies():
    return render_template("cookies.html")

@app.route("/mentions_legales")
def mentions_legales():
    return render_template("mentions_legales.html")

@app.route("/car/<int:car_id>")
def car_detail(car_id):
    car = next((c for c in cars if c["id"] == car_id), None)
    if not car:
        return "Véhicule introuvable", 404
    return render_template("car_detail.html", car=car)

@app.route("/reservation/<int:car_id>")
def reservation(car_id):
    car = next((c for c in cars if c["id"] == car_id), None)
    if not car:
        return "Véhicule introuvable", 404
    deposit = round(car["price"] * 0.05)
    return render_template("reservation.html", car=car, deposit=deposit)

@app.route("/get_brands")
def get_brands():
    brands = sorted(list({c["brand"] for c in cars}))
    return jsonify(brands)

@app.route("/get_models")
def get_models():
    brand = request.args.get("brand", "")
    models = sorted(list({c["model"] for c in cars if c["brand"] == brand}))
    return jsonify(models)

@app.route("/filter_cars", methods=["POST"])
def filter_cars():
    data = request.get_json() or {}
    brand = data.get("brand", "")
    model = data.get("model", "")
    budget = data.get("budget", "")
    filtered = cars
    if brand:
        filtered = [c for c in filtered if c["brand"] == brand]
    if model:
        filtered = [c for c in filtered if c["model"] == model]
    if budget == "low":
        filtered = [c for c in filtered if c["price"] < 100000]
    elif budget == "mid":
        filtered = [c for c in filtered if 100000 <= c["price"] <= 1000000]
    elif budget == "high":
        filtered = [c for c in filtered if c["price"] > 1000000]
    return jsonify(filtered)

@app.route("/api/check_plate")
def check_plate():
    plate = request.args.get("plate", "")
    if not plate:
        return jsonify({"error": "Aucune plaque fournie"}), 400
    try:
        r = requests.get(
            "https://immat-api.fr/api/vehicles",
            params={"plate": plate},
            headers={"Authorization": f"Bearer {os.getenv('IMMAT_API_KEY')}"}
        )
        r.raise_for_status()
        data = r.json()
        return jsonify({
            "brand": data.get("brand"),
            "model": data.get("model"),
            "year": data.get("year"),
            "fuel": data.get("fuel"),
            "color": data.get("color"),
            "hp": data.get("hp"),
            "transmission": data.get("transmission")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)