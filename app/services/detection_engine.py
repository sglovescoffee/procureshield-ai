
from app.database.db import get_connection


def analyse_invoice(invoice_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        i.invoice_id,
        i.vendor_id,
        i.po_id,
        i.quantity AS invoice_quantity,
        i.unit_price AS invoice_price,
        po.quantity AS po_quantity,
        po.unit_price AS po_price,
        v.risk_score AS vendor_risk,
        dr.receipt_id,
        dr.quantity_received,
        dr.verified AS receipt_verified
    FROM invoices i
    JOIN purchase_orders po ON i.po_id = po.po_id
    JOIN vendors v ON i.vendor_id = v.vendor_id
    LEFT JOIN delivery_receipts dr ON po.po_id = dr.po_id
    WHERE i.invoice_id = ?
    """

    row = cursor.execute(query, (invoice_id,)).fetchone()

    if row is None:
        connection.close()
        return {"error": f"Invoice {invoice_id} not found"}

    invoice = dict(row)

    quantity_mismatch = (
        invoice["invoice_quantity"] != invoice["po_quantity"]
    )

    price_mismatch = (
        invoice["invoice_price"] != invoice["po_price"]
    )

    missing_receipt = invoice["receipt_id"] is None

    unverified_receipt = (
        not missing_receipt and not invoice["receipt_verified"]
    )

    received_quantity_mismatch = (
        not missing_receipt
        and invoice["quantity_received"] != invoice["po_quantity"]
    )

    # Current schema prevents duplicate invoice IDs via primary key.
    # This check is reserved for future duplicate-detection improvements.
    duplicate_invoice = False

    vendor_anomaly = invoice["vendor_risk"] >= 30

    risk_score = 0

    if quantity_mismatch:
        risk_score += 25

    if price_mismatch:
        risk_score += 25

    if (
        missing_receipt
        or unverified_receipt
        or received_quantity_mismatch
    ):
        risk_score += 20

    if duplicate_invoice:
        risk_score += 20

    if vendor_anomaly:
        risk_score += 10

    if risk_score <= 25:
        risk_level = "LOW"
    elif risk_score <= 50:
        risk_level = "MEDIUM"
    elif risk_score <= 75:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    detected_exceptions = []

    if quantity_mismatch:
        detected_exceptions.append((
            "QUANTITY_MISMATCH",
            "HIGH",
            f"Invoice quantity {invoice['invoice_quantity']} "
            f"differs from PO quantity {invoice['po_quantity']}"
        ))

    if price_mismatch:
        detected_exceptions.append((
            "PRICE_MISMATCH",
            "HIGH",
            f"Invoice price {invoice['invoice_price']} "
            f"differs from PO price {invoice['po_price']}"
        ))

    if missing_receipt:
        detected_exceptions.append((
            "MISSING_RECEIPT",
            "HIGH",
            "No delivery receipt found for this purchase order"
        ))

    if unverified_receipt:
        detected_exceptions.append((
            "UNVERIFIED_RECEIPT",
            "MEDIUM",
            "Delivery receipt has not been verified"
        ))

    if received_quantity_mismatch:
        detected_exceptions.append((
            "RECEIVED_QUANTITY_MISMATCH",
            "HIGH",
            "Received quantity differs from PO quantity"
        ))

    if vendor_anomaly:
        detected_exceptions.append((
            "VENDOR_ANOMALY",
            "MEDIUM",
            f"Vendor risk score is {invoice['vendor_risk']}"
        ))

    # Replace existing OPEN exceptions for this invoice.
    # Previously resolved exceptions remain as history.
    cursor.execute(
        """
        DELETE FROM exceptions
        WHERE invoice_id = ? AND status = 'OPEN'
        """,
        (invoice_id,)
    )

    for exception_type, severity, description in detected_exceptions:
        cursor.execute(
            """
            INSERT INTO exceptions
                (invoice_id, exception_type, severity, description, status)
            VALUES (?, ?, ?, ?, 'OPEN')
            """,
            (invoice_id, exception_type, severity, description)
        )

    connection.commit()
    connection.close()

    return {
        "invoice_id": invoice_id,
        "checks": {
            "quantity_mismatch": quantity_mismatch,
            "price_mismatch": price_mismatch,
            "missing_receipt": missing_receipt,
            "unverified_receipt": unverified_receipt,
            "received_quantity_mismatch": received_quantity_mismatch,
            "duplicate_invoice": duplicate_invoice,
            "vendor_anomaly": vendor_anomaly,
        },
        "risk_score": risk_score,
        "risk_level": risk_level,
        "exceptions_detected": len(detected_exceptions),
    }


if __name__ == "__main__":
    result = analyse_invoice("INV-1098")

    for key, value in result.items():
        print(f"{key}: {value}")
