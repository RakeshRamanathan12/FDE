from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/").status_code == 200

def test_list_payments():
    response = client.get("/payments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_payment_not_found():
    assert client.get("/payments/999999").status_code == 404

def test_reconciliation_endpoint():
    response = client.get("/invoices/reconciliation")
    assert response.status_code == 200
    assert "exact_dupes" in response.json()
    assert "credit_note_pairs" in response.json()
