from fastapi import FastAPI
from app.routers.invoices import router as invoices_router
from app.routers.payments import router as payments_router

app = FastAPI(
    title="Invoice and Payments Reconciliation API",
    description="Invoice data-quality checks and JSON-backed payments CRUD.",
    version="1.0.0",
)
app.include_router(invoices_router)
app.include_router(payments_router)

@app.get("/", tags=["Health"])
def health():
    return {"message": "Invoice and Payments API is running", "docs": "/docs"}
