import pytest
import json
from app import app, cars

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_status(client):
    res = client.get("/")
    assert res.status_code == 200

def test_home_contient_voitures(client):
    res = client.get("/")
    assert b"Lamborghini" in res.data or b"Ferrari" in res.data or b"Porsche" in res.data

def test_catalogue_status(client):
    res = client.get("/catalogue")
    assert res.status_code == 200

def test_about_status(client):
    res = client.get("/about")
    assert res.status_code == 200

def test_rdv_status(client):
    res = client.get("/rdv")
    assert res.status_code == 200

def test_sell_status(client):
    res = client.get("/sell")
    assert res.status_code == 200

def test_cookies_status(client):
    res = client.get("/cookies")
    assert res.status_code == 200

def test_mentions_legales_status(client):
    res = client.get("/mentions_legales")
    assert res.status_code == 200

def test_test_drive_status(client):
    res = client.get("/test_drive")
    assert res.status_code == 200

def test_car_detail_valide(client):
    res = client.get("/car/1")
    assert res.status_code == 200

def test_car_detail_contenu(client):
    res = client.get("/car/1")
    assert b"Lamborghini" in res.data
    assert b"Urus" in res.data

def test_car_detail_404(client):
    res = client.get("/car/999")
    assert res.status_code == 404

def test_reservation_valide(client):
    res = client.get("/reservation/6")
    assert res.status_code == 200

def test_reservation_404(client):
    res = client.get("/reservation/999")
    assert res.status_code == 404

def test_reservation_contient_caution(client):
    res = client.get("/reservation/6")
    assert b"12" in res.data

def test_get_brands_status(client):
    res = client.get("/get_brands")
    assert res.status_code == 200

def test_get_brands_json(client):
    res = client.get("/get_brands")
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_brands_tries(client):
    res = client.get("/get_brands")
    data = json.loads(res.data)
    assert data == sorted(data)

def test_get_brands_sans_doublons(client):
    res = client.get("/get_brands")
    data = json.loads(res.data)
    assert len(data) == len(set(data))

def test_get_models_ferrari(client):
    res = client.get("/get_models?brand=Ferrari")
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_models_sans_doublons(client):
    res = client.get("/get_models?brand=Porsche")
    data = json.loads(res.data)
    assert len(data) == len(set(data))

def test_filter_par_marque(client):
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "BMW", "model": "", "budget": ""}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["brand"] == "BMW" for c in data)

def test_filter_budget_low(client):
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": "low"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["price"] < 100000 for c in data)

def test_filter_budget_mid(client):
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": "mid"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(100000 <= c["price"] <= 1000000 for c in data)

def test_filter_budget_high(client):
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": "high"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["price"] > 1000000 for c in data)
    assert len(data) > 0

def test_filter_combine_marque_modele(client):
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "Lamborghini", "model": "Urus", "budget": ""}),
        content_type="application/json")
    data = json.loads(res.data)
    assert all(c["brand"] == "Lamborghini" and c["model"] == "Urus" for c in data)
    assert len(data) == 2

def test_filter_aucun_resultat(client):
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "Ferrari", "model": "", "budget": "low"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert data == []

def test_filter_sans_critere(client):
    res = client.post("/filter_cars",
        data=json.dumps({"brand": "", "model": "", "budget": ""}),
        content_type="application/json")
    data = json.loads(res.data)
    assert len(data) == len(cars)

def test_caution_5_pourcent(client):
    car = next(c for c in cars if c["id"] == 26)
    deposit = round(car["price"] * 0.05)
    assert deposit == 150000

def test_caution_mclaren(client):
    car = next(c for c in cars if c["id"] == 6)
    deposit = round(car["price"] * 0.05)
    assert deposit == 12500

def test_404_page_personnalisee(client):
    res = client.get("/page-qui-nexiste-pas")
    assert res.status_code == 404
    assert "404" in res.data.decode("utf-8") or "OTOMA" in res.data.decode("utf-8")