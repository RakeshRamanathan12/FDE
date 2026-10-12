"""Simple JSON persistence helpers.

Designed for a single-process homework demo. A database is recommended for
concurrent writers or production workloads.
"""
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "invoices.json"

def load_invoices():
    """Read the saved list of invoices from disk."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_invoices(invoices):
    """Write the current list of invoices to disk."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(invoices, file, indent=4)
        file.write("\n")
