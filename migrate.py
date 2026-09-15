from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Connexion Supabase
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

# Tes données de app.py — copie ta liste cars ici
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

# Insertion dans Supabase
for car in cars:
    result = supabase.table('cars').insert(car).execute()
    print(f"Inséré : {car['brand']} {car['model']}")

print(f"\n✅ {len(cars)} véhicules insérés avec succès !")