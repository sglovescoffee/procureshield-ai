
from app.services.detection_engine import analyse_invoice

invoice_ids = [
    "INV-1001",
    "INV-1002",
    "INV-1050",
    "INV-1067",
    "INV-1098",
    "INV-1102",
]

for invoice_id in invoice_ids:
    result = analyse_invoice(invoice_id)

    print("-" * 40)
    print("Invoice:", invoice_id)
    print("Risk Score:", result.get("risk_score"))
    print("Risk Level:", result.get("risk_level"))
    print("Exceptions Detected:", result.get("exceptions_detected"))
