from app.database.db import get_connection


connection = get_connection()
cursor = connection.cursor()

query = """
SELECT
    i.invoice_id,
    i.quantity,
    po.quantity AS po_quantity,
    i.unit_price,
    po.unit_price AS po_unit_price
FROM invoices i
JOIN purchase_orders po
    ON i.po_id = po.po_id
WHERE i.invoice_id = 'INV-1098'
"""

result = cursor.execute(query).fetchone()

print(dict(result))

connection.close()