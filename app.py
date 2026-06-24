# ============================================================
# OTOMA — Flask Backend
# Main application file handling routes and API endpoints
# ============================================================

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os, requests

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# ============================================================
# VEHICLE DATABASE
# Static list of luxury and high-performance vehicles
# Each vehicle contains: id, brand, model, version, type,
# price, mileage, fuel, year, color, horsepower,
# transmission and image filename
# ============================================================
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

# ============================================================
# PAGE ROUTES
# Each route renders the corresponding HTML template
# ============================================================

# Home page — passes the 3 most recently added vehicles
@app.route("/")
def home():
    newest = cars[-3:][::-1]
    return render_template("index.html", cars=newest)

# Catalogue page — passes all vehicles and sorted brand list
@app.route("/catalogue")
def catalogue():
    brands = sorted(list({c["brand"] for c in cars}))
    return render_template("catalogue.html", cars=cars, brands=brands)

# Services route redirects to catalogue page
@app.route("/services")
def services():
    return render_template("catalogue.html", cars=cars, brands=sorted(list({c["brand"] for c in cars})))

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# Test drive booking page
@app.route("/test_drive")
def test_drive():
    return render_template("test_drive.html")

# Appointment booking page
@app.route("/rdv")
def rdv():
    return render_template("rdv.html", title="Prendre rendez-vous")

# Sell your vehicle page
@app.route("/sell")
def sell():
    return render_template("sell.html")

# Cookie policy page
@app.route("/cookies")
def cookies():
    return render_template("cookies.html")

# Legal notices page
@app.route("/mentions_legales")
def mentions_legales():
    return render_template("mentions_legales.html")

# ============================================================
# VEHICLE DETAIL ROUTE
# Finds a vehicle by its ID and renders its detail page
# Returns 404 if the vehicle is not found
# ============================================================
@app.route("/car/<int:car_id>")
def car_detail(car_id):
    # Search for the vehicle matching the given ID
    car = next((c for c in cars if c["id"] == car_id), None)
    if not car:
        return "Véhicule introuvable", 404
    return render_template("car_detail.html", car=car)

# ============================================================
# RESERVATION ROUTE
# Calculates a 5% deposit based on the vehicle price
# and renders the reservation page
# ============================================================
@app.route("/reservation/<int:car_id>")
def reservation(car_id):
    # Search for the vehicle matching the given ID
    car = next((c for c in cars if c["id"] == car_id), None)
    if not car:
        return "Véhicule introuvable", 404
    # Calculate the deposit amount (5% of vehicle price)
    deposit = round(car["price"] * 0.05)
    return render_template("reservation.html", car=car, deposit=deposit)

# ============================================================
# API ENDPOINTS
# RESTful endpoints used by the frontend JavaScript
# ============================================================

# Returns a sorted list of all unique brands
@app.route("/get_brands")
def get_brands():
    brands = sorted(list({c["brand"] for c in cars}))
    return jsonify(brands)

# Returns a sorted list of models filtered by brand
@app.route("/get_models")
def get_models():
    brand = request.args.get("brand", "")
    models = sorted(list({c["model"] for c in cars if c["brand"] == brand}))
    return jsonify(models)

# Filters vehicles based on brand, model and budget criteria
@app.route("/filter_cars", methods=["POST"])
def filter_cars():
    # Parse JSON body from the request
    data = request.get_json() or {}
    brand = data.get("brand", "")
    model = data.get("model", "")
    budget = data.get("budget", "")

    filtered = cars

    # Apply brand filter if provided
    if brand:
        filtered = [c for c in filtered if c["brand"] == brand]

    # Apply model filter if provided
    if model:
        filtered = [c for c in filtered if c["model"] == model]

    # Apply budget filter based on price range
    if budget == "low":
        # Under 100,000 €
        filtered = [c for c in filtered if c["price"] < 100000]
    elif budget == "mid":
        # Between 100,000 € and 1,000,000 €
        filtered = [c for c in filtered if 100000 <= c["price"] <= 1000000]
    elif budget == "high":
        # Over 1,000,000 €
        filtered = [c for c in filtered if c["price"] > 1000000]

    return jsonify(filtered)

# ============================================================
# LICENSE PLATE API
# Calls the external immat-api.fr service to retrieve
# vehicle information from a French license plate number
# ============================================================
@app.route("/api/check_plate")
def check_plate():
    plate = request.args.get("plate", "")

    # Return an error if no plate number is provided
    if not plate:
        return jsonify({"error": "Aucune plaque fournie"}), 400

    try:
        # Call the external API with the plate number
        # API key is loaded from environment variables
        r = requests.get(
            "https://immat-api.fr/api/vehicles",
            params={"plate": plate},
            headers={"Authorization": f"Bearer {os.getenv('IMMAT_API_KEY')}"}
        )
        r.raise_for_status()
        data = r.json()

        # Return only the relevant vehicle fields
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
        # Return the error message if the API call fails
        return jsonify({"error": str(e)}), 500

# ============================================================
# ERROR HANDLERS
# ============================================================

# Custom 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ============================================================
# ENTRY POINT
# Run the Flask development server
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)