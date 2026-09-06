# ============================================================
# OTOMA — Flask Backend
# Main application file handling routes and API endpoints
# ============================================================

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import os, requests, bcrypt, re
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "otoma_secret")

# ─── CONNEXION MONGODB ───────────────────────────────
client = MongoClient(os.getenv("MONGO_URI"))
db = client["otoma"]
users_col     = db["users"]
favorites_col = db["favorites"]
requests_col  = db["requests"]

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
    plate = request.args.get("plate", "").replace(" ", "")
    if not plate:
        return jsonify({"error": "Aucune plaque fournie"}), 400
    try:
        r = requests.get(
            "https://api-plaque-immatriculation-siv.p.rapidapi.com/get-vehicule-info",
            params={
                "token": os.getenv("RAPIDAPI_TOKEN"),
                "host_name": "https://apiplaqueimmatriculation.com",
                "immatriculation": plate
            },
            headers={
                "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
                "x-rapidapi-host": "api-plaque-immatriculation-siv.p.rapidapi.com",
                "Content-Type": "application/json"
            }
        )
        r.raise_for_status()
        data = r.json().get("data", {})

        # Puissance : "131 CH" → "131"
        puissance_raw = data.get("puisFiscReelCH", "")
        puissance = puissance_raw.replace("CH", "").strip() if puissance_raw else "N/A"

        # Année : "2009-04-18" → "2009"
        annee = data.get("date1erCir_fr", "")[:4] or "N/A"

        # Couleur : souvent vide dans le SIV
        couleur = data.get("couleur") or "Non renseignée"

        # Transmission : boite_vitesse M = Manuelle, A = Automatique
        boite = data.get("boite_vitesse", "")
        if boite == "M":
            transmission = "Manuelle"
        elif boite == "A":
            transmission = "Automatique"
        else:
            transmission = data.get("type_transmission", "N/A")

        return jsonify({
            "brand":        data.get("marque", "N/A"),
            "model":        data.get("modele", "N/A"),
            "version":      data.get("version", ""),
            "year":         annee,
            "fuel":         data.get("type_moteur", "N/A"),
            "color":        couleur,
            "hp":           puissance,
            "transmission": transmission,
            "carrosserie":  data.get("carrosserie", ""),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# ERROR HANDLERS
# ============================================================

# Custom 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



# ============================================================
# HELPERS AUTH
# ============================================================

def current_user():
    """Returns the current logged-in user document or None"""
    uid = session.get("user_id")
    if not uid:
        return None
    return users_col.find_one({"_id": ObjectId(uid)})

def login_required(f):
    """Decorator to protect routes that require authentication"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Connectez-vous pour accéder à cette page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ============================================================
# INSCRIPTION
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json() or request.form
        prenom  = data.get("prenom", "").strip()
        nom     = data.get("nom", "").strip()
        email   = data.get("email", "").strip().lower()
        mdp     = data.get("password", "")

        # Validations
        if not all([prenom, nom, email, mdp]):
            return jsonify({"error": "Tous les champs sont obligatoires"}), 400
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Email invalide"}), 400
        if len(mdp) < 8:
            return jsonify({"error": "Mot de passe trop court (8 caractères minimum)"}), 400
        if users_col.find_one({"email": email}):
            return jsonify({"error": "Un compte existe déjà avec cet email"}), 409

        # Hash mot de passe
        hashed = bcrypt.hashpw(mdp.encode(), bcrypt.gensalt())

        # Insertion en base
        user_id = users_col.insert_one({
            "prenom":      prenom,
            "nom":         nom,
            "email":       email,
            "password":    hashed,
            "created_at":  datetime.utcnow(),
        }).inserted_id

        # Connexion automatique après inscription
        session["user_id"]    = str(user_id)
        session["user_name"]  = prenom

        return jsonify({"success": True, "redirect": url_for("compte")}), 200

    return render_template("register.html")

# ============================================================
# CONNEXION
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data  = request.get_json() or request.form
        email = data.get("email", "").strip().lower()
        mdp   = data.get("password", "")

        user = users_col.find_one({"email": email})
        if not user or not bcrypt.checkpw(mdp.encode(), user["password"]):
            return jsonify({"error": "Email ou mot de passe incorrect"}), 401

        session["user_id"]   = str(user["_id"])
        session["user_name"] = user["prenom"]

        return jsonify({"success": True, "redirect": url_for("compte")}), 200

    return render_template("login.html")

# ============================================================
# DÉCONNEXION
# ============================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ============================================================
# ESPACE CLIENT
# ============================================================

@app.route("/compte")
@login_required
def compte():
    uid = session["user_id"]

    # Favorites
    favs = list(favorites_col.find({"user_id": uid}))
    fav_car_ids = [f["car_id"] for f in favs]
    fav_cars = [c for c in cars if c["id"] in fav_car_ids]

    # Only caution and vente requests
    demandes = list(requests_col.find({
        "user_id": uid,
        "type": {"$in": ["caution", "vente"]}
    }).sort("created_at", -1))

    return render_template("compte.html",
        user=current_user(),
        fav_cars=fav_cars,
        demandes=demandes
    )

# ============================================================
# FAVORIS
# ============================================================

@app.route("/api/favorite/<int:car_id>", methods=["POST"])
def toggle_favorite(car_id):
    if not session.get("user_id"):
        return jsonify({"error": "Non connecté"}), 401

    uid = session["user_id"]
    existing = favorites_col.find_one({"user_id": uid, "car_id": car_id})

    if existing:
        # Retirer des favoris
        favorites_col.delete_one({"_id": existing["_id"]})
        return jsonify({"status": "removed"})
    else:
        # Ajouter aux favoris
        favorites_col.insert_one({
            "user_id":    uid,
            "car_id":     car_id,
            "created_at": datetime.utcnow()
        })
        return jsonify({"status": "added"})

@app.route("/api/favorites")
def get_favorites():
    if not session.get("user_id"):
        return jsonify([])
    uid = session["user_id"]
    favs = list(favorites_col.find({"user_id": uid}))
    return jsonify([f["car_id"] for f in favs])

# ============================================================
# ENREGISTRER UNE DEMANDE
# ============================================================

@app.route("/api/save_request", methods=["POST"])
def save_request():
    if not session.get("user_id"):
        return jsonify({"error": "Non connecté"}), 401

    data = request.get_json() or {}
    requests_col.insert_one({
        "user_id":    session["user_id"],
        "type":       data.get("type"),
        "details":    data.get("details", {}),
        "statut":     "En attente",
        "created_at": datetime.utcnow()
    })
    return jsonify({"success": True})

# ============================================================
# ENTRY POINT
# Run the Flask development server
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)


# ============================================================
# DELETE ACCOUNT
# ============================================================
@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    """Deletes the user account and all associated data"""
    uid = session["user_id"]
    users_col.delete_one({"_id": ObjectId(uid)})
    favorites_col.delete_many({"user_id": uid})
    requests_col.delete_many({"user_id": uid})
    session.clear()
    return jsonify({"success": True})


# ============================================================
# UPDATE ACCOUNT INFO
# Allows the user to update their first name, last name and email
# ============================================================
@app.route("/api/update_account", methods=["POST"])
@login_required
def update_account():
    data   = request.get_json() or {}
    prenom = data.get("prenom", "").strip()
    nom    = data.get("nom", "").strip()
    email  = data.get("email", "").strip().lower()

    if not all([prenom, nom, email]):
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Email invalide"}), 400

    # Check email not taken by another user
    existing = users_col.find_one({"email": email, "_id": {"$ne": ObjectId(session["user_id"])}})
    if existing:
        return jsonify({"error": "Cet email est déjà utilisé"}), 409

    users_col.update_one(
        {"_id": ObjectId(session["user_id"])},
        {"$set": {"prenom": prenom, "nom": nom, "email": email}}
    )
    session["user_name"] = prenom
    return jsonify({"success": True})

# ============================================================
# UPDATE PASSWORD
# Verifies current password before updating to new one
# ============================================================
@app.route("/api/update_password", methods=["POST"])
@login_required
def update_password():
    data        = request.get_json() or {}
    current_pwd = data.get("current_password", "")
    new_pwd     = data.get("new_password", "")

    if len(new_pwd) < 8:
        return jsonify({"error": "Le mot de passe doit contenir au moins 8 caractères"}), 400

    user = users_col.find_one({"_id": ObjectId(session["user_id"])})

    # Verify current password
    if not bcrypt.checkpw(current_pwd.encode(), user["password"]):
        return jsonify({"error": "Mot de passe actuel incorrect"}), 401

    # Hash and save new password
    hashed = bcrypt.hashpw(new_pwd.encode(), bcrypt.gensalt())
    users_col.update_one(
        {"_id": ObjectId(session["user_id"])},
        {"$set": {"password": hashed}}
    )
    return jsonify({"success": True})