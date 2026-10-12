# Persistent Invoice API — Week 1, Day 2

A beginner-friendly Python FastAPI project that stores invoice records in a JSON file. Records survive normal Uvicorn restarts.

## 1. Requirements

- Python 3.10 or newer
- VS Code or another editor
- Terminal / Command Prompt

## 2. Project files

```text
invoice-api/
├── main.py                 # Creates the FastAPI app
├── models.py               # Invoice request model and validation
├── storage.py              # json.load / json.dump helpers
├── routes/
│   ├── __init__.py
│   └── invoices.py         # GET, POST, DELETE and PUT
├── data/
│   └── invoices.json       # Saved invoice records
├── tests/
│   └── test_api.py         # Automated API tests
├── requirements.txt
├── .gitignore
└── README.md
```

## 3. Install and run

Open a terminal **inside the invoice-api folder**.

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m uvicorn main:app --reload --port 8000
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Open Swagger UI: **http://127.0.0.1:8000/docs**

> If you have already installed the dependencies, you can also run `uvicorn main:app --reload --port 8000`.

## 4. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/invoices` | Return all invoices |
| GET | `/invoices/{invoice_id}` | Return one invoice or 404 |
| POST | `/invoices` | Create and save an invoice |
| DELETE | `/invoices/{invoice_id}` | Delete and save the change, or 404 |
| PUT | `/invoices/{invoice_id}` | Bonus: update an existing invoice |

## 5. Test with Swagger

1. Open `/docs` and expand **GET /invoices**.
2. Click **Try it out** then **Execute**. You should see `INV-101` and `INV-102`.
3. Expand **POST /invoices**, click **Try it out**, and submit:

```json
{
  "invoice_id": "INV-103",
  "vendor": "Nova Inc",
  "amount": 250000,
  "status": "PENDING"
}
```

4. Execute **GET /invoices** again. `INV-103` should appear.
5. Stop the server with **Ctrl+C**. Restart it using the Uvicorn command above.
6. Execute **GET /invoices**. `INV-103` should **still exist**: it was saved to `data/invoices.json`.
7. Execute **DELETE /invoices/INV-103**, then GET again to confirm it is gone.
8. Try deleting a nonexistent ID; the API returns **404 Invoice not found**.

## 6. Bonus: PUT

Use **PUT /invoices/INV-101** with the full invoice body:

```json
{
  "invoice_id": "INV-101",
  "vendor": "ABC Ltd",
  "amount": 85000,
  "status": "PAID"
}
```

The invoice ID in the URL and JSON body must match.

## 7. Automated tests

From the project folder:

```bash
python -m pytest -q
```

The tests use a temporary JSON file and will not change your sample invoice data.

## 8. How persistence works

- `json.load(file)` reads JSON from disk into Python data.
- `json.dump(invoices, file, indent=4)` saves Python data as JSON.
- Every GET loads current file contents; POST/DELETE/PUT save the changed list.
- Unlike a Python list held only in memory, a disk file survives a server restart.
