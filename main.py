"""
LedgerMind AI Bookkeeping System
by Naseeruddin Mohammed
A simple, working Python backend for the Excel scanner.
"""

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Optional
import io

app = FastAPI(
    title="LedgerMind API",
    description="AI Bookkeeping with Fraud Detection & Tax Deductions",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== DATA MODELS ======
class Transaction:
    def __init__(self, id, date, description, vendor, amount, category="", tx_type="Expense"):
        self.id = id
        self.date = date
        self.description = description
        self.vendor = vendor
        self.amount = amount
        self.category = category
        self.type = tx_type

class FraudAlert:
    def __init__(self, tx_id, alert_type, severity, description, action):
        self.transaction_id = tx_id
        self.alert_type = alert_type
        self.severity = severity
        self.description = description
        self.recommended_action = action

class TaxDeduction:
    def __init__(self, category, amount, description, confidence):
        self.category = category
        self.amount = amount
        self.description = description
        self.confidence = confidence

# ====== AI AGENTS ======
class DataAgent:
    """Categorizes transactions automatically."""

    def categorize(self, transactions: List[Transaction]):
        for tx in transactions:
            desc = tx.description.lower()
            vendor = (tx.vendor or "").lower()

            if tx.type == "Revenue" or tx.amount > 0:
                tx.category = "Revenue"
            elif "aws" in desc or "server" in desc or "aws" in vendor:
                tx.category = "Software"
            elif any(x in desc for x in ["slack", "notion", "figma", "github", "zoom"]):
                tx.category = "Software"
            elif any(x in desc for x in ["office", "paper", "toner"]):
                tx.category = "Office Supplies"
            elif any(x in desc for x in ["uber", "trip", "travel", "flight"]):
                tx.category = "Travel"
            elif any(x in desc for x in ["ads", "google ads", "marketing", "facebook"]):
                tx.category = "Marketing"
            elif "rent" in desc or "landlord" in desc:
                tx.category = "Rent"
            elif any(x in desc for x in ["lunch", "restaurant", "meal", "dinner"]):
                tx.category = "Meals"
            elif "wire" in desc or "unknown" in desc:
                tx.category = "Uncategorized"
            else:
                tx.category = "Other"
        return transactions

class FraudAgent:
    """Detects suspicious transactions."""

    def scan(self, transactions: List[Transaction]) -> List[FraudAlert]:
        alerts = []
        seen = {}

        for tx in transactions:
            # Duplicate detection
            key = f"{tx.vendor}-{abs(tx.amount)}"
            if key in seen and tx.vendor and tx.vendor != "Unknown":
                alerts.append(FraudAlert(
                    tx.id, "Duplicate Invoice", "high",
                    f'Invoice from "{tx.vendor}" for ${abs(tx.amount):,.2f} appears to be a duplicate of {seen[key]}',
                    "Block Payment"
                ))
            else:
                seen[key] = tx.id

            # Large amount check
            if abs(tx.amount) > 8000 and tx.vendor not in ["Acme Corp", "Beta LLC", "Gamma Inc", "Delta Co", "Epsilon Ltd", ""]:
                if not any(a.transaction_id == tx.id for a in alerts):
                    alerts.append(FraudAlert(
                        tx.id, "Large Amount Alert", "medium",
                        f'Transaction of ${abs(tx.amount):,.2f} to "{tx.vendor}" is unusually large',
                        "Verify by Phone"
                    ))

            # Unknown vendor
            if tx.vendor == "Unknown" or "unknown" in tx.description.lower():
                alerts.append(FraudAlert(
                    tx.id, "Unknown Vendor", "high",
                    f'Wire transfer of ${abs(tx.amount):,.2f} to unknown recipient',
                    "Hold for Review"
                ))

        return alerts

class TaxAgent:
    """Finds tax deductions."""

    def scan(self, transactions: List[Transaction]) -> List[TaxDeduction]:
        deductions = []

        for tx in transactions:
            if tx.type == "Expense" or tx.amount < 0:
                amt = abs(tx.amount)
                if tx.category == "Software":
                    deductions.append(TaxDeduction("Software & Technology", amt, f"{tx.description} - Business software", 0.95))
                elif tx.category == "Travel":
                    deductions.append(TaxDeduction("Travel & Transportation", amt, f"{tx.description} - Business travel", 0.90))
                elif tx.category == "Meals":
                    deductions.append(TaxDeduction("Meals & Entertainment", amt * 0.5, f"{tx.description} - Business meal (50%)", 0.85))
                elif tx.category == "Marketing":
                    deductions.append(TaxDeduction("Advertising", amt, f"{tx.description} - Business advertising", 0.95))
                elif tx.category == "Office Supplies":
                    deductions.append(TaxDeduction("Office Expenses", amt, f"{tx.description} - Office supplies", 0.95))
                elif tx.category == "Rent":
                    deductions.append(TaxDeduction("Rent", amt, f"{tx.description} - Business rent", 0.98))

        return deductions

class ForecastAgent:
    """Predicts cash flow."""

    def predict(self, transactions: List[Transaction], days: int = 30):
        balance = 50000
        predictions = []

        for tx in transactions:
            balance += tx.amount

        for i in range(days):
            balance += (sum(t.amount for t in transactions) / max(len(transactions), 1))
            predictions.append({
                "day": i + 1,
                "balance": round(balance, 2),
                "risk": "low" if balance > 30000 else "medium" if balance > 15000 else "high"
            })

        return predictions

class VendorAgent:
    """Analyzes vendor relationships."""

    def analyze(self, transactions: List[Transaction], fraud_alerts: List[FraudAlert]):
        vendor_data = {}

        for tx in transactions:
            v = tx.vendor or "Unknown"
            if v not in vendor_data:
                vendor_data[v] = {"total": 0, "count": 0}
            vendor_data[v]["total"] += abs(tx.amount)
            vendor_data[v]["count"] += 1

        scores = []
        for name, data in vendor_data.items():
            has_fraud = any(
                next((t for t in transactions if t.id == a.transaction_id), None) and 
                next((t for t in transactions if t.id == a.transaction_id), None).vendor == name
                for a in fraud_alerts
            )
            score = 25 if has_fraud else min(100, 70 + data["count"] * 5)
            scores.append({
                "name": name,
                "total_spent": round(data["total"], 2),
                "transactions": data["count"],
                "health_score": score,
                "has_fraud": has_fraud
            })

        return sorted(scores, key=lambda x: x["total_spent"], reverse=True)

# ====== API ENDPOINTS ======

@app.get("/")
def root():
    return {
        "message": "LedgerMind API by Naseeruddin Mohammed",
        "version": "1.0.0",
        "agents": ["Data", "Fraud", "Forecast", "Tax", "Vendor"],
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/scan")
async def scan_file(file: UploadFile = File(...)):
    """Upload Excel/CSV and get full AI analysis."""
    try:
        # Read file
        contents = await file.read()

        # Parse based on file type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        # Convert to transactions
        transactions = []
        for idx, row in df.iterrows():
            amt = float(row.get('Amount', row.get('amount', row.get('Debit', 0))) or 0)
            if amt == 0:
                amt = float(row.get('Credit', 0))

            tx = Transaction(
                id=f"TX-{idx+1}",
                date=str(row.get('Date', row.get('date', datetime.now().date()))),
                description=str(row.get('Description', row.get('description', f"Transaction {idx+1}"))),
                vendor=str(row.get('Vendor', row.get('vendor', row.get('Payee', '')))),
                amount=amt,
                tx_type="Revenue" if amt > 0 else "Expense"
            )
            transactions.append(tx)

        # Run AI agents
        data_agent = DataAgent()
        fraud_agent = FraudAgent()
        tax_agent = TaxAgent()
        forecast_agent = ForecastAgent()
        vendor_agent = VendorAgent()

        transactions = data_agent.categorize(transactions)
        fraud_alerts = fraud_agent.scan(transactions)
        tax_deductions = tax_agent.scan(transactions)
        cash_flow = forecast_agent.predict(transactions)
        vendor_scores = vendor_agent.analyze(transactions, fraud_alerts)

        # Calculate totals
        total_revenue = sum(t.amount for t in transactions if t.amount > 0)
        total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
        total_deductions = sum(d.amount for d in tax_deductions)

        return {
            "success": True,
            "summary": {
                "total_transactions": len(transactions),
                "total_revenue": round(total_revenue, 2),
                "total_expenses": round(total_expenses, 2),
                "net_income": round(total_revenue - total_expenses, 2),
                "fraud_alerts_count": len(fraud_alerts),
                "tax_deductions_found": round(total_deductions, 2),
                "risk_level": "Critical" if len(fraud_alerts) >= 3 else "Medium" if len(fraud_alerts) >= 1 else "Low"
            },
            "transactions": [
                {
                    "id": t.id,
                    "date": t.date,
                    "description": t.description,
                    "vendor": t.vendor,
                    "amount": t.amount,
                    "category": t.category,
                    "type": t.type
                } for t in transactions
            ],
            "fraud_alerts": [
                {
                    "transaction_id": a.transaction_id,
                    "type": a.alert_type,
                    "severity": a.severity,
                    "description": a.description,
                    "action": a.recommended_action
                } for a in fraud_alerts
            ],
            "tax_deductions": [
                {
                    "category": d.category,
                    "amount": round(d.amount, 2),
                    "description": d.description,
                    "confidence": d.confidence
                } for d in tax_deductions
            ],
            "cash_flow_prediction": cash_flow[:10],
            "vendor_scores": vendor_scores
        }

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/scan-sample")
def scan_sample():
    """Demo endpoint with sample data."""
    sample_data = [
        {"Date": "2026-07-01", "Description": "Stripe Payment", "Vendor": "Stripe", "Amount": 4500},
        {"Date": "2026-07-02", "Description": "AWS Bill", "Vendor": "AWS", "Amount": -342.50},
        {"Date": "2026-07-03", "Description": "Office Paper", "Vendor": "OfficeMax", "Amount": -125},
        {"Date": "2026-07-05", "Description": "Client Invoice", "Vendor": "Acme Corp", "Amount": 8200},
        {"Date": "2026-07-06", "Description": "Slack", "Vendor": "Slack", "Amount": -15},
        {"Date": "2026-07-07", "Description": "TechSupplies Invoice 4482", "Vendor": "TechSupplies", "Amount": -12500},
        {"Date": "2026-07-08", "Description": "Uber Trip", "Vendor": "Uber", "Amount": -47.30},
        {"Date": "2026-07-09", "Description": "Google Ads", "Vendor": "Google", "Amount": -850},
        {"Date": "2026-07-10", "Description": "Client Invoice", "Vendor": "Beta LLC", "Amount": 3200},
        {"Date": "2026-07-11", "Description": "TechSupplies Invoice 4482", "Vendor": "TechSupplies", "Amount": -12500},
        {"Date": "2026-07-12", "Description": "Office Rent", "Vendor": "Landlord", "Amount": -2500},
        {"Date": "2026-07-13", "Description": "Notion", "Vendor": "Notion", "Amount": -10},
        {"Date": "2026-07-14", "Description": "Wire Transfer Unknown", "Vendor": "Unknown", "Amount": -8750},
        {"Date": "2026-07-15", "Description": "Client Invoice", "Vendor": "Gamma Inc", "Amount": 5600},
        {"Date": "2026-07-16", "Description": "Figma", "Vendor": "Figma", "Amount": -15},
        {"Date": "2026-07-17", "Description": "GitHub Pro", "Vendor": "GitHub", "Amount": -21},
        {"Date": "2026-07-18", "Description": "OfficeMax Toner", "Vendor": "OfficeMax", "Amount": -189},
        {"Date": "2026-07-19", "Description": "Client Invoice", "Vendor": "Delta Co", "Amount": 7800},
        {"Date": "2026-07-20", "Description": "Zoom", "Vendor": "Zoom", "Amount": -19.99},
        {"Date": "2026-07-21", "Description": "Business Lunch", "Vendor": "Restaurant", "Amount": -87.50},
        {"Date": "2026-07-22", "Description": "Client Invoice", "Vendor": "Epsilon Ltd", "Amount": 4300},
        {"Date": "2026-07-23", "Description": "AWS Server", "Vendor": "AWS", "Amount": -520},
    ]

    transactions = []
    for idx, row in enumerate(sample_data):
        tx = Transaction(
            id=f"TX-{idx+1}",
            date=row["Date"],
            description=row["Description"],
            vendor=row["Vendor"],
            amount=row["Amount"],
            tx_type="Revenue" if row["Amount"] > 0 else "Expense"
        )
        transactions.append(tx)

    data_agent = DataAgent()
    fraud_agent = FraudAgent()
    tax_agent = TaxAgent()
    forecast_agent = ForecastAgent()
    vendor_agent = VendorAgent()

    transactions = data_agent.categorize(transactions)
    fraud_alerts = fraud_agent.scan(transactions)
    tax_deductions = tax_agent.scan(transactions)
    cash_flow = forecast_agent.predict(transactions)
    vendor_scores = vendor_agent.analyze(transactions, fraud_alerts)

    total_revenue = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    total_deductions = sum(d.amount for d in tax_deductions)

    return {
        "success": True,
        "summary": {
            "total_transactions": len(transactions),
            "total_revenue": round(total_revenue, 2),
            "total_expenses": round(total_expenses, 2),
            "net_income": round(total_revenue - total_expenses, 2),
            "fraud_alerts_count": len(fraud_alerts),
            "tax_deductions_found": round(total_deductions, 2),
            "risk_level": "Critical" if len(fraud_alerts) >= 3 else "Medium" if len(fraud_alerts) >= 1 else "Low"
        },
        "transactions": [{"id": t.id, "date": t.date, "description": t.description, "vendor": t.vendor, "amount": t.amount, "category": t.category, "type": t.type} for t in transactions],
        "fraud_alerts": [{"transaction_id": a.transaction_id, "type": a.alert_type, "severity": a.severity, "description": a.description, "action": a.recommended_action} for a in fraud_alerts],
        "tax_deductions": [{"category": d.category, "amount": round(d.amount, 2), "description": d.description, "confidence": d.confidence} for d in tax_deductions],
        "cash_flow_prediction": cash_flow[:10],
        "vendor_scores": vendor_scores
    }

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
