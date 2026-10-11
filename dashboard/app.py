
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent

# Ensure the project root is searched first
sys.path.insert(0, str(ROOT))

# Remove a conflicting "app" module if Python loaded one
if "app" in sys.modules:
    loaded_app = sys.modules["app"]
    loaded_file = getattr(loaded_app, "__file__", None)
    if loaded_file and not str(Path(loaded_file).resolve()).startswith(
        str(ROOT.resolve())
    ):
        del sys.modules["app"]

from app.database.db import get_connection
from app.services.detection_engine import analyse_invoice
from app.services.decision_agent import decide_action
from app.services.action_executor import execute_actions
from app.services.verify_actions import verify_actions



st.set_page_config(
    page_title="ProcureShield AI",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ ProcureShield AI")
st.caption("Autonomous Procurement Exception Resolution")
st.info("Prototype mode: all actions are simulated. No real payments are affected.")


def get_invoices():
    connection = get_connection()
    try:
        rows = connection.execute(
            """
            SELECT invoice_id, vendor_id, quantity, unit_price
            FROM invoices
            ORDER BY invoice_id
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def get_counts():
    connection = get_connection()
    try:
        tables = ["invoices", "exceptions", "actions", "audit_logs"]
        return {
            table: connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            for table in tables
        }
    finally:
        connection.close()


counts = get_counts()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Invoices", counts["invoices"])
c2.metric("Exceptions", counts["exceptions"])
c3.metric("Recorded Actions", counts["actions"])
c4.metric("Audit Events", counts["audit_logs"])

st.divider()

invoices = get_invoices()

if not invoices:
    st.warning("No invoices found. Seed the database first.")
    st.stop()

invoice_ids = [invoice["invoice_id"] for invoice in invoices]

selected_id = st.selectbox(
    "Select an invoice to investigate",
    invoice_ids,
    index=invoice_ids.index("INV-1098")
    if "INV-1098" in invoice_ids else 0,
)

invoice = next(
    item for item in invoices
    if item["invoice_id"] == selected_id
)

left, right = st.columns([1, 2])

with left:
    st.subheader("Invoice details")
    st.write("**Invoice ID:**", invoice["invoice_id"])
    st.write("**Vendor ID:**", invoice["vendor_id"])
    st.write("**Quantity:**", invoice["quantity"])
    st.write("**Unit price:**", f"₹{invoice['unit_price']:,.2f}")

    analyse_clicked = st.button(
        "Analyse invoice",
        type="primary",
        use_container_width=True,
    )

    execute_clicked = st.button(
        "Execute simulated actions",
        use_container_width=True,
    )

    verify_clicked = st.button(
        "Verify recorded actions",
        use_container_width=True,
    )

    if analyse_clicked:
        st.session_state["analysis_result"] = analyse_invoice(selected_id)
        st.session_state["decision_result"] = decide_action(selected_id)
        st.session_state["analysis_invoice_id"] = selected_id

    if execute_clicked:
        result = execute_actions(selected_id)
        st.session_state["execution_result"] = result
        st.session_state["execution_invoice_id"] = selected_id

    if verify_clicked:
        result = verify_actions(selected_id)
        st.session_state["verification_result"] = result
        st.session_state["verification_invoice_id"] = selected_id

with right:
    st.subheader("Risk analysis")

    analysis = st.session_state.get("analysis_result")
    decision = st.session_state.get("decision_result")

    if st.session_state.get("analysis_invoice_id") == selected_id and analysis:
        if "error" in analysis:
            st.error(analysis["error"])
        else:
            m1, m2 = st.columns(2)
            m1.metric("Risk score", f"{analysis['risk_score']}/100")
            m2.metric("Risk level", analysis["risk_level"])

            st.progress(analysis["risk_score"] / 100)

            st.markdown("#### Detection results")
            for name, detected in analysis["checks"].items():
                icon = "🔴" if detected else "🟢"
                label = "Detected" if detected else "Not detected"
                st.write(f"{icon} {name.replace('_', ' ').title()}: {label}")

            st.markdown("#### Recommended decision")
            if decision and st.session_state.get("analysis_invoice_id") == selected_id:
                st.code(decision["decision"])
                st.write(decision["reason"])

    execution = st.session_state.get("execution_result")
    if st.session_state.get("execution_invoice_id") == selected_id and execution:
        st.markdown("#### Action execution")
        st.write("**Mode:**", execution.get("execution_mode", "SIMULATED"))
        st.write("**Decision:**", execution.get("decision"))
        st.write("**Requested actions:**", execution.get("actions_recorded", []))
        st.write("**New actions saved:**", execution.get("new_actions_saved", []))
        st.caption(execution.get("message", ""))

    verification = st.session_state.get("verification_result")
    if (
        st.session_state.get("verification_invoice_id") == selected_id
        and verification
    ):
        st.markdown("#### Verification")
        st.write("**Actions found:**", verification.get("actions_found", 0))

        if verification.get("verified"):
            st.success(verification["message"])
        else:
            st.warning(verification["message"])

st.divider()
st.subheader("How the system works")
st.write(
    "Invoice → Detection → Risk score → Decision → "
    "Simulated action → Verification → Audit trail"
)
st.caption(
    "Verification checks the recorded database state. "
    "It does not verify an external payment system."
)
