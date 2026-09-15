import pytest
from app import app, cars
import json

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
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



# ============================================================
# INTEGRATION TESTS
# Verify that Flask routes, Jinja2 templates and static files
# work correctly together end to end
# ============================================================

def test_catalogue_contient_voitures(client):
    """Integration test — catalogue page renders vehicle cards"""
    response = client.get('/catalogue')
    assert response.status_code == 200
    assert b'Ferrari' in response.data or b'Lamborghini' in response.data

def test_car_detail_contient_specs(client):
    """Integration test — car detail page renders specs correctly"""
    response = client.get('/car/1')
    assert response.status_code == 200
    assert b'ch' in response.data  # horsepower
    assert b'km' in response.data  # mileage

def test_reservation_contient_caution(client):
    """Integration test — reservation page renders deposit amount"""
    response = client.get('/reservation/1')
    assert response.status_code == 200
    assert b'Caution' in response.data or b'caution' in response.data

def test_filter_cars_retourne_json(client):
    """Integration test — /filter_cars returns valid JSON"""
    response = client.post('/filter_cars',
        json={"brand": "Ferrari", "model": "", "budget": ""},
        content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)

def test_get_brands_retourne_json(client):
    """Integration test — /get_brands returns sorted JSON list"""
    response = client.get('/get_brands')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_models_retourne_json(client):
    """Integration test — /get_models returns models for a given brand"""
    response = client.get('/get_models?brand=Ferrari')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_static_css_accessible(client):
    """Integration test — main CSS file is served correctly"""
    response = client.get('/static/style.css')
    assert response.status_code == 200
    assert b'color' in response.data or b'font' in response.data

def test_static_js_accessible(client):
    """Integration test — main JS file is served correctly"""
    response = client.get('/static/script.js')
    assert response.status_code == 200

def test_catalogue_js_accessible(client):
    """Integration test — catalogue JS file is served correctly"""
    response = client.get('/static/catalogue.js')
    assert response.status_code == 200

def test_index_contient_titre(client):
    """Integration test — home page contains OTOMA brand name"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'OTOMA' in response.data


# ============================================================
# SECURITY TESTS
# Verify that the application handles malicious input,
# unauthorized access and sensitive data correctly
# ============================================================

def test_injection_sql_filtre(client):
    """Security test — SQL injection attempt in filter is handled safely"""
    response = client.post('/filter_cars',
        json={"brand": "' OR '1'='1", "model": "", "budget": ""},
        content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    # Should return empty list, not all cars
    assert isinstance(data, list)
    assert len(data) == 0

def test_injection_sql_car_id(client):
    """Security test — SQL injection attempt in car ID is rejected"""
    response = client.get('/car/1 OR 1=1')
    assert response.status_code in [400, 404]

def test_xss_filtre_marque(client):
    """Security test — XSS attempt in brand filter is handled safely"""
    response = client.post('/filter_cars',
        json={"brand": "<script>alert('xss')</script>", "model": "", "budget": ""},
        content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_page_inexistante_retourne_404(client):
    """Security test — unknown route returns 404 not 500"""
    response = client.get('/admin')
    assert response.status_code == 404

def test_page_admin_inexistante(client):
    """Security test — /admin route does not exist"""
    response = client.get('/admin/dashboard')
    assert response.status_code == 404

def test_car_id_negatif(client):
    """Security test — negative car ID returns 404"""
    response = client.get('/car/-1')
    assert response.status_code == 404

def test_car_id_texte(client):
    """Security test — non-numeric car ID returns 404"""
    response = client.get('/car/abc')
    assert response.status_code == 404

def test_reservation_id_invalide(client):
    """Security test — invalid reservation ID returns 404"""
    response = client.get('/reservation/99999')
    assert response.status_code == 404

def test_filter_cars_sans_body(client):
    """Security test — /filter_cars with empty body returns valid response"""
    response = client.post('/filter_cars',
        json={},
        content_type='application/json')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_filter_cars_methode_get_refusee(client):
    """Security test — /filter_cars GET method is not allowed"""
    response = client.get('/filter_cars')
    assert response.status_code == 405

def test_compte_sans_session(client):
    """Security test — /compte redirects to login if not authenticated"""
    response = client.get('/compte')
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location', '')

def test_delete_account_sans_session(client):
    """Security test — /delete_account blocked if not authenticated"""
    response = client.post('/delete_account')
    assert response.status_code == 302

def test_favorite_sans_session(client):
    """Security test — /api/favorite blocked if not authenticated"""
    response = client.post('/api/favorite/1')
    assert response.status_code == 401

def test_save_request_sans_session(client):
    """Security test — /api/save_request blocked if not authenticated"""
    response = client.post('/api/save_request',
        json={"type": "caution", "details": {}},
        content_type='application/json')
    assert response.status_code == 401