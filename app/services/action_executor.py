
from app.database.db import get_connection
from app.services.decision_agent import decide_action
from app.services.detection_engine import analyse_invoice


def execute_actions(invoice_id):
    # Step 1: Analyse invoice and decide what to do
    decision_result = decide_action(invoice_id)

    if decision_result.get("decision") == "ERROR":
        return decision_result

    # Step 2: Determine the actions to record
    decision = decision_result["decision"]
    reason = decision_result["reason"]

    actions_to_record = [decision]

    # Request evidence as well when the receipt is missing
    analysis = analyse_invoice(invoice_id)

    if (
        analysis.get("checks", {}).get("missing_receipt", False)
        and "REQUEST_EVIDENCE" not in actions_to_record
    ):
        actions_to_record.append("REQUEST_EVIDENCE")

    # Step 3: Connect to the database
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Step 4: Find actions already recorded for this invoice
        existing_actions = cursor.execute(
            """
            SELECT action_type
            FROM actions
            WHERE invoice_id = ?
              AND action_status = 'SIMULATED'
            """,
            (invoice_id,),
        ).fetchall()

        existing_types = {
            row["action_type"] for row in existing_actions
        }

        # Step 5: Only record actions that do not already exist
        new_actions = [
            action
            for action in actions_to_record
            if action not in existing_types
        ]

        for action_type in new_actions:
            cursor.execute(
                """
                INSERT INTO actions
                    (invoice_id, action_type, action_status, details)
                VALUES (?, ?, ?, ?)
                """,
                (
                    invoice_id,
                    action_type,
                    "SIMULATED",
                    reason,
                ),
            )

            cursor.execute(
                """
                INSERT INTO audit_logs
                    (invoice_id, event_type, message)
                VALUES (?, ?, ?)
                """,
                (
                    invoice_id,
                    action_type,
                    f"Simulated action recorded: {reason}",
                ),
            )

        # Step 6: Save all new records
        connection.commit()

        return {
            **decision_result,
            "actions_recorded": actions_to_record,
            "new_actions_saved": new_actions,
            "execution_mode": "SIMULATED",
            "message": (
                "New simulated actions recorded."
                if new_actions
                else "All requested simulated actions were already recorded."
            ),
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    result = execute_actions("INV-1098")

    for key, value in result.items():
        print(f"{key}: {value}")
