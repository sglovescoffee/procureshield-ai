
from app.services.detection_engine import analyse_invoice


def decide_action(invoice_id):
    analysis = analyse_invoice(invoice_id)

    if "error" in analysis:
        return {
            "invoice_id": invoice_id,
            "decision": "ERROR",
            "reason": analysis["error"],
        }

    checks = analysis["checks"]
    risk_score = analysis["risk_score"]

    
    if risk_score >= 76:
        decision = "HOLD_PAYMENT"
        reason = "Critical risk requires investigation."

    elif checks["quantity_mismatch"] or checks["price_mismatch"]:
        decision = "HOLD_PAYMENT"
        reason = "Invoice does not match the purchase order."

    elif checks["missing_receipt"]:
        decision = "REQUEST_EVIDENCE"
        reason = "Delivery receipt is missing."

    elif risk_score >= 26:
        decision = "ESCALATE"
        reason = "Elevated risk requires human review."

    else:
        decision = "APPROVE"
        reason = "No configured anomalies were detected."


    return {
        "invoice_id": invoice_id,
        "risk_score": risk_score,
        "risk_level": analysis["risk_level"],
        "decision": decision,
        "reason": reason,
    }


if __name__ == "__main__":
    result = decide_action("INV-1098")

    for key, value in result.items():
        print(f"{key}: {value}")

