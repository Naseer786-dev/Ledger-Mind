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
2. Run the API Server
bash
python main.py
The server starts at: http://localhost:8000
3. Test the API
Open your browser and go to:
Health check: http://localhost:8000/health
Sample scan: http://localhost:8000/api/scan-sample
4. Upload Your Excel File
bash
curl -X POST "http://localhost:8000/api/scan" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_transactions.xlsx"
Excel File Format
Your Excel/CSV file should have these columns:
Table
Date	Description	Vendor	Amount
2026-07-01	Stripe Payment	Stripe	4500
2026-07-02	AWS Bill	AWS	-342.50
Positive amounts = Revenue/Income
Negative amounts = Expenses
