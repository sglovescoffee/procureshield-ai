from app.database.db import get_connection


connection = get_connection()
cursor = connection.cursor()

tables = [
    "vendors",
    "purchase_orders",
    "invoices",
    "delivery_receipts",
    "exceptions",
    "actions",
    "audit_logs"
]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    print(f"{table}: {count}")

connection.close()