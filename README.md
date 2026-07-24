AI Bookkeeping Agent with Fraud Detection & Tax Deductions
Built by Naseeruddin Mohammed
What is LedgerMind?
LedgerMind is a 5-agent AI system that:
Data Agent - Auto-categorizes transactions
Fraud Agent - Detects duplicate invoices & suspicious transactions
Forecast Agent - Predicts cash flow 30 days ahead
Tax Agent - Finds hidden tax deductions
Vendor Agent - Scores supplier relationships
Quick Start
1. Install Dependencies
bash
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
Deploy to Render (Free Hosting)
Push code to GitHub
Go to render.com
Click "New Web Service"
Connect your GitHub repo
Set:
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Click "Create Web Service"
Deploy Frontend to GitHub Pages
Upload index.html to your GitHub repo
Go to repo Settings > Pages
Select "Deploy from a branch"
Select "main" branch and "/ (root)" folder
Click Save
Your site will be live at: https://yourusername.github.io/Ledger-Mind/
API Endpoints
Table
Endpoint	Method	Description
/	GET	API info
/health	GET	Health check
/api/scan	POST	Upload Excel/CSV file
/api/scan-sample	POST	Demo with sample data
Response Format
JSON
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
Support
For questions, contact: Naseeruddin Mohammed
Built with FastAPI + Pandas + Love
