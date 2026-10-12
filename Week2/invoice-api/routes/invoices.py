"""Invoice endpoints backed by a JSON file."""
from fastapi import APIRouter, HTTPException, status
from models import Invoice
from storage import load_invoices, save_invoices

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("")
def get_invoices():
    """Read all invoices from disk."""
    return load_invoices()

@router.get("/{invoice_id}")
def get_invoice(invoice_id: str):
    """Read one invoice or return HTTP 404."""
    for invoice in load_invoices():
        if invoice["invoice_id"] == invoice_id:
            return invoice
    raise HTTPException(status_code=404, detail="Invoice not found")

@router.post("", status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: Invoice):
    """Add an invoice and persist it to disk."""
    invoices = load_invoices()
    if any(item["invoice_id"] == invoice.invoice_id for item in invoices):
        raise HTTPException(status_code=409, detail="Invoice already exists")
    new_invoice = invoice.model_dump()
    invoices.append(new_invoice)
    save_invoices(invoices)
    return new_invoice

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: str):
    """Remove an invoice and persist the deletion."""
    invoices = load_invoices()
    for index, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            invoices.pop(index)
            save_invoices(invoices)
            return {"message": "Invoice deleted"}
    raise HTTPException(status_code=404, detail="Invoice not found")

@router.put("/{invoice_id}")
def update_invoice(invoice_id: str, invoice: Invoice):
    """Optional: replace an existing invoice."""
    invoices = load_invoices()
    if invoice.invoice_id != invoice_id:
        raise HTTPException(status_code=400, detail="Invoice ID in URL and body must match")
    for index, existing in enumerate(invoices):
        if existing["invoice_id"] == invoice_id:
            updated = invoice.model_dump()
            invoices[index] = updated
            save_invoices(invoices)
            return updated
    raise HTTPException(status_code=404, detail="Invoice not found")
