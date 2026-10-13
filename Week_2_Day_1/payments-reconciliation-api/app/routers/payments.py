from fastapi import APIRouter, HTTPException, status
from app.models import PaymentCreate, PaymentUpdate
from app.storage import read_payments, write_payments

router = APIRouter(prefix="/payments", tags=["Payments"])

def next_payment_id(payments):
    return max((p.get("payment_id", 0) for p in payments), default=0) + 1

@router.get("/")
def list_payments():
    return read_payments()

@router.get("/{payment_id}")
def get_payment(payment_id: int):
    for payment in read_payments():
        if payment.get("payment_id") == payment_id:
            return payment
    raise HTTPException(status_code=404, detail="Payment not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate):
    payments = read_payments()
    payment = {"payment_id": next_payment_id(payments),
               "invoice_id": payload.invoice_id, "paid": payload.paid}
    payments.append(payment)
    write_payments(payments)
    return payment

@router.put("/{payment_id}")
def replace_payment(payment_id: int, payload: PaymentCreate):
    payments = read_payments()
    for i, payment in enumerate(payments):
        if payment.get("payment_id") == payment_id:
            updated = {"payment_id": payment_id,
                       "invoice_id": payload.invoice_id, "paid": payload.paid}
            payments[i] = updated
            write_payments(payments)
            return updated
    raise HTTPException(status_code=404, detail="Payment not found")

@router.patch("/{payment_id}")
def update_payment(payment_id: int, payload: PaymentUpdate):
    payments = read_payments()
    for i, payment in enumerate(payments):
        if payment.get("payment_id") == payment_id:
            updated = dict(payment)
            for key, value in payload.model_dump(exclude_unset=True).items():
                if value is not None:
                    updated[key] = value
            payments[i] = updated
            write_payments(payments)
            return updated
    raise HTTPException(status_code=404, detail="Payment not found")

@router.delete("/{payment_id}")
def delete_payment(payment_id: int):
    payments = read_payments()
    for i, payment in enumerate(payments):
        if payment.get("payment_id") == payment_id:
            deleted = payments.pop(i)
            write_payments(payments)
            return {"message": "Payment deleted", "payment": deleted}
    raise HTTPException(status_code=404, detail="Payment not found")
