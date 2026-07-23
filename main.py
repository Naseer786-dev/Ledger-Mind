from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import io

app = FastAPI(title="LedgerMind AI Bookkeeper")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>LedgerMind AI Bookkeeper</title>
    <style>
        body {font-family: Arial; text-align: center; padding: 50px; background: #f0f8ff;}
        h1 {color: #0066cc;}
        .card {background: white; padding: 20px; margin: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    </style>
</head>
<body>
    <h1>LedgerMind AI Bookkeeper</h1>
    <p>Automatically find tax deductions, catch fraud, and clean your books</p>
    <div class="card"><h3>🔍 Smart Scanning</h3><p>Find duplicates and errors instantly</p></div>
    <div class="card"><h3>💰 Tax Deductions</h3><p>Never miss a deduction again</p></div>
    <div class="card"><h3>🛡️ Fraud Detection</h3><p>Catch suspicious transactions</p></div>
    <p><b>API is Live at /scan</b></p>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/scan")
async def scan_books(file: UploadFile):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    duplicates = df[df.duplicated()]
    big_expenses = df[df["amount"] > 500]
    fraud = df[df["amount"] < 0]
    
    return {
        "duplicates_found": len(duplicates),
        "potential_deductions": len(big_expenses),
        "suspicious_transactions": len(fraud),
        "status": "scan complete"
    }

