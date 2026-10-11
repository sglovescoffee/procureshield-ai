
# ProcureShield AI 🛡️

### Autonomous Procurement Exception Resolution

**Detect. Decide. Act. Verify. Automatically.**

ProcureShield AI is a prototype system designed to identify procurement invoice exceptions, calculate risk scores, recommend decisions, record simulated actions, and verify that those actions have been logged.

Traditional invoice-processing workflows often require procurement teams to manually compare invoices against purchase orders and delivery records. ProcureShield demonstrates how rule-based detection and an auditable decision workflow can help streamline this process.

## 🚀 Key Features

- **Invoice analysis:** Compares invoice quantities and unit prices against purchase orders.
- **Exception detection:** Identifies quantity mismatches, price mismatches, missing delivery receipts, unverified receipts, and received-quantity discrepancies.
- **Risk scoring:** Calculates a weighted risk score from 0 to 100.
- **Risk classification:** Classifies invoices as LOW, MEDIUM, HIGH, or CRITICAL.
- **Decision engine:** Recommends actions such as HOLD_PAYMENT, REQUEST_EVIDENCE, ESCALATE, or APPROVE.
- **Simulated action execution:** Records proposed actions in a SQLite database without affecting real payments.
- **Audit trail:** Stores action events for traceability.
- **Action verification:** Checks whether simulated actions have been recorded.
- **Interactive dashboard:** Uses Streamlit to display invoice details, risk scores, detected anomalies, decisions, and verification results.
- **Demo dataset:** Includes sample vendors, purchase orders, invoices, and delivery receipts.

## 🧠 How It Works

1. **Receive:** Select an invoice from the available demo dataset.
2. **Investigate:** Retrieve related purchase order, vendor, and delivery receipt data.
3. **Detect:** Run configured anomaly checks.
4. **Score:** Calculate a weighted risk score.
5. **Decide:** Apply decision rules to recommend an action.
6. **Act:** Record simulated actions and audit events.
7. **Verify:** Confirm that the expected action records exist in the database.

## 🏗️ Architecture

```text
Invoice and Procurement Records
              |
              v
       Detection Engine
              |
              v
        Risk Scoring
              |
              v
        Decision Agent
              |
              v
      Simulated Actions
              |
              v
       SQLite Database
              |
              v
      Action Verification
              |
              v
          Audit Trail

      Streamlit Dashboard
     Displays the workflow
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| SQLite | Local database and audit records |
| Streamlit | Interactive dashboard |
| Pandas | Data handling dependency |
| scikit-learn | Machine learning dependency for planned extensions |
| FastAPI | API framework dependency for planned extensions |
| Pydantic | Data validation dependency |
| PyMuPDF | PDF processing dependency for planned extensions |

The current working prototype primarily uses Python, SQLite, and Streamlit. A dependency being installed does not mean that its planned integration is already implemented.

## 📂 Project Structure

```text
procureshield-ai/
├── app/
│   ├── database/
│   │   ├── db.py
│   │   ├── check_db.py
│   │   ├── check_invoice.py
│   │   └── seed_data.py
│   └── services/
│       ├── detection_engine.py
│       ├── test_detection.py
│       ├── decision_agent.py
│       ├── action_executor.py
│       └── verify_actions.py
├── dashboard/
│   └── app.py
├── data/
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Getting Started

### Prerequisites

- Python installed
- Git installed
- A terminal such as PowerShell
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/sglovesscoffee/procureshield-ai.git
cd procureshield-ai
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

If Streamlit is missing from the dependency file, add `streamlit` to `requirements.txt` and reinstall.

### 4. Initialise the database

```powershell
python -m app.database.db
```

If this command does not initialise the database in your version, run the project's database initialisation entry point as configured in `app/database/db.py`.

### 5. Seed the demo data

```powershell
python -m app.services.seed_data
```

Run the seed step only when appropriate for your database state; do not assume repeated seeding is safe.

### 6. Launch the dashboard

```powershell
python -m streamlit run dashboard/app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

## 🧪 Demo Scenario

The main demonstration uses invoice `INV-1098`.

Sample values:

- Invoice quantity: 118
- Purchase order quantity: 100
- Invoice unit price: ₹1,420
- Purchase order unit price: ₹1,250
- Delivery receipt: Missing

Expected prototype result:

- Quantity mismatch: Detected
- Price mismatch: Detected
- Missing delivery receipt: Detected
- Risk score: 70/100
- Risk level: HIGH
- Recommended decision: HOLD_PAYMENT
- Simulated actions: HOLD_PAYMENT and REQUEST_EVIDENCE

The database records simulated actions and audit events. The verification function checks the recorded action state.

## 📊 Risk Scoring

The prototype uses configurable heuristic weights:

| Signal | Weight |
|---|---:|
| Quantity mismatch | 25 |
| Price mismatch | 25 |
| Missing or inconsistent delivery evidence | 20 |
| Duplicate invoice | 20 |
| Vendor anomaly | 10 |
| **Maximum score** | **100** |

Risk bands:

- LOW: 0–25
- MEDIUM: 26–50
- HIGH: 51–75
- CRITICAL: 76–100

These weights and thresholds are demonstration heuristics, not a validated fraud-detection model. The current duplicate-invoice check is limited by the database schema and requires further development.

## 🔐 Safety and Limitations

- All actions are simulated.
- No real payment is approved, held, or released.
- No actual vendor email or evidence request is sent.
- Verification checks local database records, not an external financial system.
- Risk scores are rule-based and have not been calibrated against real procurement outcomes.
- The demo data is synthetic and must not be treated as evidence of real-world accuracy.
- Human review would be required before any production financial action.
- Production deployment would require authentication, access control, secure secrets management, stronger duplicate detection, monitoring, and integration testing.

## 🗺️ Future Scope

- PDF invoice extraction
- Stronger duplicate and near-duplicate detection
- ML-assisted anomaly scoring
- LLM-generated explanations using structured outputs
- Human approval workflows
- Procurement-system integrations
- Email or ticketing automation
- External-system verification
- Authentication and role-based access control
- Comprehensive automated testing

## 🎯 Project Goal

ProcureShield AI aims to demonstrate a closed-loop approach to procurement exception handling: identifying an issue, recommending a decision, recording the action, and verifying the resulting system state.

**ProcureShield AI — More than detecting exceptions. A prototype for resolving them.**
