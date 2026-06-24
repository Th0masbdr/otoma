import pytest
import json
from app import app, cars

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# -------------------------------------------------------
# TESTS FONCTIONNELS — Routes
# -------------------------------------------------------

def test_home_status(client):
    """TF-01 — La page d'accueil répond avec un code 200"""
    res = client.get("/")
    assert res.status_code == 200

def test_home_contient_voitures(client):
    """TF-01 — La page d'accueil contient des voitures"""
    res = client.get("/")
    assert b"Lamborghini" in res.data or b"Ferrari" in res.data or b"Porsche" in res.data

def test_catalogue_status(client):
    """TF-02 — La page catalogue répond avec un code 200"""
    res = client.get("/catalogue")
    assert res.status_code == 200

def test_about_status(client):
    """TF-03 — La page À propos répond avec un code 200"""
    res = client.get("/about")
    assert res.status_code == 200

def test_rdv_status(client):
    """TF-04 — La page RDV répond avec un code 200"""
    res = client.get("/rdv")
    assert res.status_code == 200

def test_sell_status(client):
    """Page vendre répond avec un code 200"""
    res = client.get("/sell")
    assert res.status_code == 200

def test_cookies_status(client):
    """TF-05 — La page cookies répond avec un code 200"""
    res = client.get("/cookies")
    assert res.status_code == 200

def test_mentions_legales_status(client):
    """TF-06 — La page mentions légales répond avec un code 200"""
    res = client.get("/mentions_legales")
    assert res.status_code == 200

def test_test_drive_status(client):
    """La page test drive répond avec un code 200"""
    res = client.get("/test_drive")
    assert res.status_code == 200

# -------------------------------------------------------
# TESTS FONCTIONNELS — Fiche véhicule
# -------------------------------------------------------

def test_car_detail_valide(client):
    """TF-13 — La fiche d'un véhicule existant répond avec un code 200"""
    res = client.get("/car/1")
    assert res.status_code == 200

def test_car_detail_contenu(client):
    """TF-14 — La fiche contient les informations du véhicule"""
    res = client.get("/car/1")
    assert b"Lamborghini" in res.data
    assert b"Urus" in res.data

def test_car_detail_404(client):
    """TF-22 — Un ID inexistant retourne une 404"""
    res = client.get("/car/999")
    assert res.status_code == 404

# -------------------------------------------------------
# TESTS FONCTIONNELS — Réservation
# -------------------------------------------------------

def test_reservation_valide(client):
    """TF-17 — La page réservation d'un véhicule existant répond 200"""
    res = client.get("/reservation/6")
    assert res.status_code == 200

def test_reservation_404(client):
    """TF-17 — La réservation d'un véhicule inexistant retourne 404"""
    res = client.get("/reservation/999")
    assert res.status_code == 404

def test_reservation_contient_caution(client):
    """TF-18 — La page affiche le bon montant de caution (5%)"""
    res = client.get("/reservation/6")  # McLaren 720S à 250 000 €
    assert b"12" in res.data  # 12 500 €

# -------------------------------------------------------
# TESTS UNITAIRES — API Flask
# -------------------------------------------------------

def test_get_brands_status(client):
    """TU-07 — L'endpoint /get_brands répond 200"""
    res = client.get("/get_brands")
    assert res.status_code == 200

def test_get_brands_json(client):
    """TU-07 — /get_brands retourne du JSON valide"""
    res = client.get("/get_brands")
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_brands_tries(client):
    """TU-07 — Les marques sont triées alphabétiquement"""
    res = client.get("/get_brands")
    data = json.loads(res.data)
    assert data == sorted(data)

def test_get_brands_sans_doublons(client):
    """TU-07 — Pas de doublons dans les marques"""
    res = client.get("/get_brands")
    data = json.loads(res.data)
    assert len(data) == len(set(data))

def test_get_models_ferrari(client):
    """TU-08 — /get_models retourne les modèles Ferrari"""
    res = client.get("/get_models?brand=Ferrari")
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "488" in data or "F8" in data or "Roma" in data

def test_get_models_sans_doublons(client):
    """TU-08 — Pas de doublons dans les modèles"""
    res = client.get("/get_models?brand=Porsche")
    data = json.loads(res.data)
    assert len(data) == len(set(data))

# -------------------------------------------------------
# TESTS UNITAIRES — Filtre voitures
# -------------------------------------------------------

def test_filter_par_marque(client):
    """TU-01 — Filtre par marque retourne uniquement les véhicules de cette marque"""
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "BMW", "model": "", "budget": ""}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["brand"] == "BMW" for c in data)

def test_filter_budget_low(client):
    """TU-02 — Budget 'low' retourne uniquement les véhicules < 100 000 €"""
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": "low"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["price"] < 100000 for c in data)

def test_filter_budget_mid(client):
    """TU-03 — Budget 'mid' retourne les véhicules entre 100k et 1M€"""
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": "mid"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(100000 <= c["price"] <= 1000000 for c in data)

def test_filter_budget_high(client):
    """TU-04 — Budget 'high' retourne les véhicules > 1 000 000 €"""
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": "high"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["price"] > 1000000 for c in data)
    assert len(data) > 0

def test_filter_combine_marque_modele(client):
    """TU-05 — Filtre combiné marque + modèle"""
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "Lamborghini", "model": "Urus", "budget": ""}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["brand"] == "Lamborghini" and c["model"] == "Urus" for c in data)
    assert len(data) == 2

def test_filter_aucun_resultat(client):
    """TU-06 — Filtre sans résultat retourne une liste vide"""
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "Ferrari", "model": "", "budget": "low"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert data == []

def test_filter_sans_critere(client):
    """Filtre sans critère retourne tous les véhicules"""
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": ""}),
        content_type="application/json")
    data = json.loads(res.data)
    assert len(data) == len(cars)

# -------------------------------------------------------
# TESTS UNITAIRES — Calcul caution
# -------------------------------------------------------

def test_caution_5_pourcent(client):
    """TU-11 — La caution est bien calculée à 5% du prix"""
    from app import cars
    car = next(c for c in cars if c["id"] == 26)  # Bugatti 3 000 000 €
    deposit = round(car["price"] * 0.05)
    assert deposit == 150000

def test_caution_mclaren(client):
    """TU-11 — Caution McLaren 720S à 250 000 € = 12 500 €"""
    from app import cars
    car = next(c for c in cars if c["id"] == 6)
    deposit = round(car["price"] * 0.05)
    assert deposit == 12500

# -------------------------------------------------------
# TESTS D'INTÉGRATION — 404 personnalisée
# -------------------------------------------------------

def test_404_page_personnalisee(client):
    """TF-22 — Une URL inexistante retourne la page 404 personnalisée"""
    res = client.get("/page-qui-nexiste-pas")
    assert res.status_code == 404
    assert "404" in res.data.decode("utf-8") or "OTOMA" in res.data.decode("utf-8")