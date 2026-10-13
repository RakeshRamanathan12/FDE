from fastapi import APIRouter, HTTPException
from app.storage import read_invoices, read_payments
from app.services.reconciliation import reconcile

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("/")
def list_invoices():
    return read_invoices()

@router.get("/reconciliation")
def invoice_reconciliation():
    return reconcile(read_invoices(), read_payments())

@router.get("/{invoice_id}")
def get_invoice(invoice_id: str):
    for invoice in read_invoices():
        if invoice.get("invoice_id") == invoice_id:
            return invoice
    raise HTTPException(status_code=404, detail="Invoice not found")
