from collections import defaultdict
from copy import deepcopy

def _freeze(value):
    if isinstance(value, dict):
        return tuple(sorted((k, _freeze(v)) for k, v in value.items()))
    if isinstance(value, list):
        return tuple(_freeze(v) for v in value)
    return value

def reconcile(invoices, payments):
    # Work on a copy so the original JSON input remains unchanged.
    normalized = deepcopy(invoices)
    none_amount_rows = []
    for index, row in enumerate(normalized):
        vendor = row.get("vendor")
        row["vendor"] = vendor.strip().title() if isinstance(vendor, str) else ""
        status = row.get("status")
        row["status"] = status.strip().upper() if isinstance(status, str) else ""
        if row.get("amount") is None:
            none_amount_rows.append({"index": index, "invoice_id": row.get("invoice_id")})

    eligible = [(i, row) for i, row in enumerate(normalized) if row.get("amount") is not None]

    exact_groups = defaultdict(list)
    for index, row in eligible:
        key = tuple(sorted((k, _freeze(v)) for k, v in row.items()))
        exact_groups[key].append(index)
    exact_dupes = {str(key): indexes for key, indexes in exact_groups.items() if len(indexes) > 1}
    duplicate_indexes = {i for indexes in exact_dupes.values() for i in indexes[1:]}
    kept = [(i, row) for i, row in eligible if i not in duplicate_indexes]

    suspected_pairs = []
    for pos, (i, a) in enumerate(kept):
        for j, b in kept[pos + 1:]:
            if (a.get("vendor"), a.get("amount"), a.get("date")) == (
                b.get("vendor"), b.get("amount"), b.get("date")
            ) and a.get("invoice_id") != b.get("invoice_id"):
                suspected_pairs.append({
                    "indexes": [i, j],
                    "pair": f'{a.get("invoice_id")} ~ {b.get("invoice_id")}'
                })

    cancelled_indexes = set()
    credit_pairs = []
    unmatched_credit_notes = []
    for i, negative in kept:
        amount = negative.get("amount")
        if not isinstance(amount, (int, float)) or amount >= 0 or i in cancelled_indexes:
            continue
        partner = None
        # The supplied homework example pairs index 3 with index 6, even
        # though the positive invoice appears later in the list. Therefore,
        # search all eligible rows, not only rows earlier in the file.
        for j, positive in kept:
            if j == i or j in cancelled_indexes:
                continue
            pos_amount = positive.get("amount")
            if (isinstance(pos_amount, (int, float)) and pos_amount > 0
                and positive.get("vendor") == negative.get("vendor")
                and pos_amount == abs(amount)):
                partner = (j, positive)
                break
        if partner:
            j, positive = partner
            positive["status"] = "CANCELLED"
            negative["status"] = "CANCELLED"
            cancelled_indexes.update({i, j})
            credit_pairs.append({"indexes": [j, i], "invoice_ids": [positive.get("invoice_id"), negative.get("invoice_id")]})
        else:
            unmatched_credit_notes.append({"index": i, "invoice_id": negative.get("invoice_id"), "amount": amount})

    payment_sums = defaultdict(float)
    for payment in payments:
        paid = payment.get("paid")
        if isinstance(paid, (int, float)) and not isinstance(paid, bool):
            payment_sums[payment.get("invoice_id")] += paid

    invoice_by_id = {}
    for index, row in kept:
        invoice_by_id.setdefault(row.get("invoice_id"), row)

    payment_reconciliation = []
    for invoice_id, row in invoice_by_id.items():
        amount = row.get("amount")
        payment_total = round(payment_sums.get(invoice_id, 0), 2)
        payment_reconciliation.append({
            "invoice_id": invoice_id,
            "vendor": row.get("vendor"),
            "invoice_amount": amount,
            "total_paid": payment_total,
            "balance": None if amount is None else round(amount - payment_total, 2)
        })
    unmatched_payments = [
        {"invoice_id": p.get("invoice_id"), "paid": p.get("paid")}
        for p in payments if p.get("invoice_id") not in invoice_by_id
    ]

    totals = {
        "invoice_amount_total_excluding_null_duplicates_and_cancelled": round(sum(
            row["amount"] for i, row in kept
            if i not in cancelled_indexes and isinstance(row.get("amount"), (int, float))
        ), 2),
        "payments_total": round(sum(payment_sums.values()), 2)
    }
    return {
        "normalized_invoices": normalized,
        "none_amount_rows": none_amount_rows,
        "exact_dupes": exact_dupes,
        "removed_duplicate_indexes": sorted(duplicate_indexes),
        "invoices_after_exact_dedupe": [row for i, row in kept],
        "suspected_duplicate_pairs": suspected_pairs,
        "credit_note_pairs": credit_pairs,
        "unmatched_credit_notes": unmatched_credit_notes,
        "cancelled_indexes": sorted(cancelled_indexes),
        "payment_reconciliation": payment_reconciliation,
        "unmatched_payments": unmatched_payments,
        "totals": totals
    }
