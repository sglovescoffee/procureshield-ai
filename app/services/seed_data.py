from app.database.db import get_connection, initialize_database


def seed_data():
    initialize_database()

    connection = get_connection()
    cursor = connection.cursor()

    # Clear existing demo data
    cursor.execute("DELETE FROM audit_logs")
    cursor.execute("DELETE FROM actions")
    cursor.execute("DELETE FROM exceptions")
    cursor.execute("DELETE FROM delivery_receipts")
    cursor.execute("DELETE FROM invoices")
    cursor.execute("DELETE FROM purchase_orders")
    cursor.execute("DELETE FROM vendors")

    # -------------------------
    # VENDORS
    # -------------------------

    vendors = [
        ("V001", "Alpha Industrial Supplies", "Industrial", 12, 48),
        ("V002", "Beta Electronics Pvt Ltd", "Electronics", 18, 73),
        ("V003", "Gamma Office Solutions", "Office Supplies", 8, 31),
        ("V004", "Delta Components", "Components", 35, 19),
    ]

    cursor.executemany("""
        INSERT INTO vendors
        (vendor_id, vendor_name, category, risk_score, total_transactions)
        VALUES (?, ?, ?, ?, ?)
    """, vendors)

    # -------------------------
    # PURCHASE ORDERS
    # -------------------------

    purchase_orders = [
        ("PO-1001", "V001", "Industrial Bearings", 100, 1250, 125000, "OPEN"),
        ("PO-1002", "V002", "Network Switches", 20, 8500, 170000, "OPEN"),
        ("PO-1050", "V003", "Office Chairs", 50, 8000, 400000, "OPEN"),
        ("PO-1067", "V001", "Safety Helmets", 100, 950, 95000, "OPEN"),
        ("PO-1098", "V002", "Industrial Sensors", 100, 1250, 125000, "OPEN"),
        ("PO-1102", "V003", "Laser Printers", 10, 22000, 220000, "OPEN"),
    ]

    cursor.executemany("""
        INSERT INTO purchase_orders
        (po_id, vendor_id, item_name, quantity, unit_price, total_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, purchase_orders)

    # -------------------------
    # INVOICES
    # -------------------------

    invoices = [
        ("INV-1001", "PO-1001", "V001", 100, 1250, 125000, "2026-10-08", "PENDING"),

        ("INV-1002", "PO-1002", "V002", 20, 8500, 170000, "2026-10-08", "PENDING"),

        ("INV-1050", "PO-1050", "V003", 50, 9500, 475000, "2026-10-08", "PENDING"),

        ("INV-1067", "PO-1067", "V001", 100, 950, 95000, "2026-10-08", "PENDING"),

        ("INV-1098", "PO-1098", "V002", 118, 1420, 167560, "2026-10-08", "PENDING"),

        ("INV-1102", "PO-1102", "V003", 10, 22000, 220000, "2026-10-08", "PENDING"),
    ]

    cursor.executemany("""
        INSERT INTO invoices
        (invoice_id, po_id, vendor_id, quantity, unit_price,
         total_amount, invoice_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, invoices)

    # -------------------------
    # DELIVERY RECEIPTS
    # -------------------------

    receipts = [
        ("GRN-1001", "PO-1001", 100, "2026-10-07", 1),
        ("GRN-1002", "PO-1002", 20, "2026-10-07", 1),
        ("GRN-1050", "PO-1050", 50, "2026-10-07", 1),
        # PO-1067 deliberately has NO receipt
        # PO-1098 deliberately has NO receipt
        ("GRN-1102", "PO-1102", 10, "2026-10-07", 1),
    ]

    cursor.executemany("""
        INSERT INTO delivery_receipts
        (receipt_id, po_id, quantity_received, receipt_date, verified)
        VALUES (?, ?, ?, ?, ?)
    """, receipts)

    connection.commit()
    connection.close()

    print("ProcureShield demo data seeded successfully.")


if __name__ == "__main__":
    seed_data()