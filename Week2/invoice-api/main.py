"""Entry point for the persistent Invoice API."""
from fastapi import FastAPI
from routes.invoices import router as invoices_router

app = FastAPI(title="Persistent Invoice API", description="Invoice API Week1 Day2", version="1.0.0")
app.include_router(invoices_router)

@app.get("/", tags=["Health"])
def home():
    return {"message": "Invoice API is running", "swagger": "/docs"}
