import json
from pathlib import Path
from threading import RLock

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
INVOICES_FILE = DATA_DIR / "invoices.json"
PAYMENTS_FILE = DATA_DIR / "payments.json"
_lock = RLock()

def _read(path, default):
    with _lock:
        if not path.exists():
            _write(path, default)
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {path.name}: {exc.msg}") from exc

def _write(path, value):
    with _lock:
        temp = path.with_suffix(path.suffix + ".tmp")
        with temp.open("w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        temp.replace(path)

def read_invoices():
    return _read(INVOICES_FILE, [])

def write_invoices(invoices):
    _write(INVOICES_FILE, invoices)

def read_payments():
    return _read(PAYMENTS_FILE, [])

def write_payments(payments):
    _write(PAYMENTS_FILE, payments)
