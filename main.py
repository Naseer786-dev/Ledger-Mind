from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io

app = FastAPI(title="LedgerMind API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LedgerMind API by Naseeruddin Mohammed", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/scan")
async def scan_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        transactions = []
        for idx, row in df.iterrows():
            amt = float(row.get('Amount', row.get('amount', 0)) or 0)
            transactions.append({
                "id": f"TX-{idx+1}",
                "date": str(row.get('Date', row.get('date', '2026-07-01'))),
                "description": str(row.get('Description', row.get('description', f"Transaction {idx+1}"))),
                "vendor": str(row.get('Vendor', row.get('vendor', ''))),
                "amount": amt,
                "type": "Revenue" if amt > 0 else "Expense"
            })

        # Categorize
        for tx in transactions:
            d = tx["description"].lower()
            v = tx["vendor"].lower()
            if tx["type"] == "Revenue":
                tx["category"] = "Revenue"
            elif "aws" in d or "server" in d or "aws" in v:
                tx["category"] = "Software"
            elif any(x in d for x in ["slack", "notion", "figma", "github", "zoom"]):
                tx["category"] = "Software"
            elif any(x in d for x in ["office", "paper", "toner"]):
                tx["category"] = "Office Supplies"
            elif any(x in d for x in ["uber", "trip", "travel"]):
                tx["category"] = "Travel"
            elif any(x in d for x in ["ads", "marketing"]):
                tx["category"] = "Marketing"
            elif "rent" in d or "landlord" in d:
                tx["category"] = "Rent"
            elif any(x in d for x in ["lunch", "restaurant", "meal"]):
                tx["category"] = "Meals"
            elif "wire" in d or "unknown" in d:
                tx["category"] = "Uncategorized"
            else:
                tx["category"] = "Other"

        # Fraud detection
        fraud_alerts = []
        seen = {}
        for tx in transactions:
            key = f"{tx['vendor']}-{abs(tx['amount'])}"
            if key in seen and tx["vendor"] and tx["vendor"] != "Unknown":
                fraud_alerts.append({
                    "transaction_id": tx["id"],
                    "type": "Duplicate Invoice",
                    "severity": "high",
                    "description": f"Duplicate from {tx['vendor']} for ${abs(tx['amount']):,.2f}",
                    "action": "Block Payment"
                })
            else:
                seen[key] = tx["id"]

            if abs(tx["amount"]) > 8000 and tx["vendor"] not in ["Acme Corp", "Beta LLC", "Gamma Inc", "Delta Co", "Epsilon Ltd", ""]:
                if not any(a["transaction_id"] == tx["id"] for a in fraud_alerts):
                    fraud_alerts.append({
                        "transaction_id": tx["id"],
                        "type": "Large Amount Alert",
                        "severity": "medium",
                        "description": f"${abs(tx['amount']):,.2f} to {tx['vendor']} is unusually large",
                        "action": "Verify by Phone"
                    })

            if tx["vendor"] == "Unknown" or "unknown" in tx["description"].lower():
                if not any(a["transaction_id"] == tx["id"] for a in fraud_alerts):
                    fraud_alerts.append({
                        "transaction_id": tx["id"],
                        "type": "Unknown Vendor",
                        "severity": "high",
                        "description": f"Wire of ${abs(tx['amount']):,.2f} to unknown recipient",
                        "action": "Hold for Review"
                    })

        # Tax deductions
        tax_deductions = []
        for tx in transactions:
            if tx["type"] == "Expense":
                amt = abs(tx["amount"])
                if tx["category"] == "Software":
                    tax_deductions.append({"category": "Software", "amount": amt, "description": tx["description"], "confidence": 0.95})
                elif tx["category"] == "Travel":
                    tax_deductions.append({"category": "Travel", "amount": amt, "description": tx["description"], "confidence": 0.90})
                elif tx["category"] == "Meals":
                    tax_deductions.append({"category": "Meals", "amount": amt * 0.5, "description": tx["description"], "confidence": 0.85})
                elif tx["category"] == "Marketing":
                    tax_deductions.append({"category": "Advertising", "amount": amt, "description": tx["description"], "confidence": 0.95})
                elif tx["category"] == "Office Supplies":
                    tax_deductions.append({"category": "Office", "amount": amt, "description": tx["description"], "confidence": 0.95})

        # Vendor scores
        vendor_data = {}
        for tx in transactions:
            v = tx["vendor"] or "Unknown"
            if v not in vendor_data:
                vendor_data[v] = {"total": 0, "count": 0}
            vendor_data[v]["total"] += abs(tx["amount"])
            vendor_data[v]["count"] += 1

        vendor_scores = []
        for name, data in vendor_data.items():
            has_fraud = any(a["transaction_id"] == tx["id"] for a in fraud_alerts for tx in transactions if tx["vendor"] == name)
            score = 25 if has_fraud else min(100, 70 + data["count"] * 5)
            vendor_scores.append({"name": name, "total_spent": data["total"], "count": data["count"], "health_score": score, "has_fraud": has_fraud})
        vendor_scores.sort(key=lambda x: x["total_spent"], reverse=True)

        total_revenue = sum(t["amount"] for t in transactions if t["amount"] > 0)
        total_expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
        total_deductions = sum(d["amount"] for d in tax_deductions)

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
            "transactions": transactions,
            "fraud_alerts": fraud_alerts,
            "tax_deductions": tax_deductions,
            "vendor_scores": vendor_scores
        }

    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

@app.post("/api/scan-sample")
def scan_sample():
    sample = [
        {"date": "2026-07-01", "description": "Stripe Payment", "vendor": "Stripe", "amount": 4500, "type": "Revenue"},
        {"date": "2026-07-02", "description": "AWS Bill", "vendor": "AWS", "amount": -342.50, "type": "Expense"},
        {"date": "2026-07-07", "description": "TechSupplies Invoice 4482", "vendor": "TechSupplies", "amount": -12500, "type": "Expense"},
        {"date": "2026-07-11", "description": "TechSupplies Invoice 4482", "vendor": "TechSupplies", "amount": -12500, "type": "Expense"},
        {"date": "2026-07-14", "description": "Wire Transfer Unknown", "vendor": "Unknown", "amount": -8750, "type": "Expense"},
    ]
    return {"success": True, "sample_data": sample, "message": "This is sample data. Upload a real Excel file for full analysis."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
