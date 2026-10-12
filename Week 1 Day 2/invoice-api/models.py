"""Pydantic schema describing an invoice request."""
from pydantic import BaseModel, Field

class Invoice(BaseModel):
    invoice_id: str = Field(min_length=1)
    vendor: str = Field(min_length=1)
    amount: float = Field(ge=0)
    status: str = Field(min_length=1)
