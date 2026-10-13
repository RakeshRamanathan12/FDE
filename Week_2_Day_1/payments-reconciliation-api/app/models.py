from typing import Optional
from pydantic import BaseModel, Field, field_validator

class PaymentCreate(BaseModel):
    invoice_id: str = Field(min_length=1, max_length=100)
    paid: float = Field(gt=0, allow_inf_nan=False)

    @field_validator("invoice_id")
    @classmethod
    def normalize_invoice_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("invoice_id cannot be blank")
        return value

class PaymentUpdate(BaseModel):
    invoice_id: Optional[str] = Field(default=None, min_length=1, max_length=100)
    paid: Optional[float] = Field(default=None, gt=0, allow_inf_nan=False)

    @field_validator("invoice_id")
    @classmethod
    def normalize_invoice_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("invoice_id cannot be blank")
        return value
