# LedgerMind

**AI Bookkeeping Agent with Fraud Detection & Tax Deductions**

Built by **Naseeruddin Mohammed**

## What is LedgerMind?

LedgerMind is a 5-agent AI system that:
- **Data Agent** - Auto-categorizes transactions
- **Fraud Agent** - Detects duplicate invoices & suspicious transactions
- **Forecast Agent** - Predicts cash flow 30 days ahead
- **Tax Agent** - Finds hidden tax deductions
- **Vendor Agent** - Scores supplier relationships

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python main.py
curl -X POST "http://localhost:8000/api/scan" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_transactions.xlsx"
| Date       | Description    | Vendor | Amount  |
| ---------- | -------------- | ------ | ------- |
| 2026-07-01 | Stripe Payment | Stripe | 4500    |
| 2026-07-02 | AWS Bill       | AWS    | -342.50 |
| Endpoint           | Method | Description           |
| ------------------ | ------ | --------------------- |
| `/`                | GET    | API info              |
| `/health`          | GET    | Health check          |
| `/api/scan`        | POST   | Upload Excel/CSV file |
| `/api/scan-sample` | POST   | Demo with sample data |
{
  "success": true,
  "summary": {
    "total_transactions": 22,
    "total_revenue": 25600.00,
    "total_expenses": 24906.29,
    "net_income": 693.71,
    "fraud_alerts_count": 3,
    "tax_deductions_found": 4850.50,
    "risk_level": "Critical"
  },
  "transactions": [...],
  "fraud_alerts": [...],
  "tax_deductions": [...],
  "cash_flow_prediction": [...],
  "vendor_scores": [...]
}
---


