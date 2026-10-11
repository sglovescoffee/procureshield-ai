
from app.database.db import get_connection


def verify_actions(invoice_id):
    connection = get_connection()
    cursor = connection.cursor()

    rows = cursor.execute(
        """
        SELECT action_type, action_status
        FROM actions
        WHERE invoice_id = ?
        ORDER BY action_id
        """,
        (invoice_id,),
    ).fetchall()

    connection.close()

    if not rows:
        return {
            "invoice_id": invoice_id,
            "verified": False,
            "message": "No actions found for this invoice.",
        }

    actions = [dict(row) for row in rows]

    successful = all(
        action["action_status"] == "SIMULATED"
        for action in actions
    )

    return {
        "invoice_id": invoice_id,
        "actions_found": len(actions),
        "actions": actions,
        "verified": successful,
        "message": (
            "All simulated actions are recorded."
            if successful
            else "One or more actions are not recorded successfully."
        ),
    }


if __name__ == "__main__":
    result = verify_actions("INV-1098")

    for key, value in result.items():
        print(f"{key}: {value}")
