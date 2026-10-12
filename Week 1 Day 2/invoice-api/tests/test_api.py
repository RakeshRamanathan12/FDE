"""Tests use a temporary JSON file so the example data stays unchanged."""
import json
from fastapi.testclient import TestClient
import storage
from main import app


def test_invoice_crud_and_persistence(tmp_path, monkeypatch):
    file_path = tmp_path / "invoices.json"
    file_path.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(storage, "DATA_FILE", file_path)
    client = TestClient(app)
    payload = {"invoice_id": "INV-103", "vendor": "Nova Inc", "amount": 250000, "status": "PENDING"}

    assert client.get("/invoices").json() == []
    assert client.post("/invoices", json=payload).status_code == 201
    assert client.post("/invoices", json=payload).status_code == 409
    assert client.get("/invoices/INV-103").json() == payload
    assert json.loads(file_path.read_text(encoding="utf-8")) == [payload]

    updated = {**payload, "status": "PAID"}
    assert client.put("/invoices/INV-103", json=updated).json() == updated
    assert client.delete("/invoices/INV-103").status_code == 200
    assert client.get("/invoices/INV-103").status_code == 404
    assert json.loads(file_path.read_text(encoding="utf-8")) == []
